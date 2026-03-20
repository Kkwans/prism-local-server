/// 数据共享层 - 实现跨进程服务列表同步
/// 
/// 使用文件系统实现多个应用实例间的服务列表共享
/// 通过文件锁机制防止并发写入冲突

use crate::models::ServerInfo;
use crate::errors::ServerError;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use std::fs::{File, OpenOptions};
use std::io::{Read, Write};
use tokio::time::{sleep, Duration};
use uuid::Uuid;

/// 共享数据结构
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SharedData {
    /// 所有运行中的服务列表
    pub servers: Vec<ServerInfo>,
    /// 最后更新时间戳（毫秒）
    pub last_update: i64,
    /// 当前实例 ID
    pub instance_id: String,
}

/// 数据共享层
pub struct DataShareLayer {
    /// 共享数据文件路径
    shared_file_path: PathBuf,
    /// 文件锁路径
    lock_file_path: PathBuf,
    /// 当前实例 ID
    instance_id: String,
}

/// 文件锁 RAII 包装器
struct FileLock {
    #[allow(dead_code)]
    file: File,
}

impl Drop for FileLock {
    fn drop(&mut self) {
        // 文件关闭时自动释放锁
    }
}

impl DataShareLayer {
    /// 创建新的数据共享层实例
    pub fn new() -> Result<Self, ServerError> {
        // 获取临时目录路径
        let temp_dir = std::env::temp_dir().join("prism-local-server");
        
        // 确保目录存在
        std::fs::create_dir_all(&temp_dir)
            .map_err(|e| ServerError::IoError(e))?;
        
        let shared_file_path = temp_dir.join("shared_data.json");
        let lock_file_path = temp_dir.join("shared_data.lock");
        let instance_id = Uuid::new_v4().to_string();
        
        Ok(Self {
            shared_file_path,
            lock_file_path,
            instance_id,
        })
    }
    
    /// 获取文件锁（最多等待 500ms）
    async fn acquire_lock(&self) -> Result<FileLock, ServerError> {
        let lock_file = OpenOptions::new()
            .create(true)
            .write(true)
            .open(&self.lock_file_path)
            .map_err(|e| ServerError::IoError(e))?;
        
        // 尝试获取独占锁，最多等待 500ms
        for _ in 0..10 {
            #[cfg(windows)]
            {
                use std::os::windows::io::AsRawHandle;
                use winapi::um::fileapi::LockFileEx;
                use winapi::um::minwinbase::{LOCKFILE_EXCLUSIVE_LOCK, LOCKFILE_FAIL_IMMEDIATELY};
                
                let handle = lock_file.as_raw_handle();
                let mut overlapped: winapi::um::minwinbase::OVERLAPPED = unsafe { std::mem::zeroed() };
                
                unsafe {
                    let result = LockFileEx(
                        handle as _,
                        LOCKFILE_EXCLUSIVE_LOCK | LOCKFILE_FAIL_IMMEDIATELY,
                        0,
                        u32::MAX,
                        u32::MAX,
                        &mut overlapped,
                    );
                    
                    if result != 0 {
                        return Ok(FileLock { file: lock_file });
                    }
                }
            }
            
            #[cfg(not(windows))]
            {
                // 非 Windows 平台的简单实现
                return Ok(FileLock { file: lock_file });
            }
            
            // 等待 50ms 后重试
            sleep(Duration::from_millis(50)).await;
        }
        
        Err(ServerError::DataShareError("无法获取文件锁".to_string()))
    }
    
    /// 读取共享数据
    pub async fn read_shared_data(&self) -> Result<SharedData, ServerError> {
        // 获取文件锁
        let _lock = self.acquire_lock().await?;
        
        // 如果文件不存在，返回空数据
        if !self.shared_file_path.exists() {
            return Ok(SharedData {
                servers: Vec::new(),
                last_update: chrono::Utc::now().timestamp_millis(),
                instance_id: self.instance_id.clone(),
            });
        }
        
        // 读取文件内容
        let mut file = File::open(&self.shared_file_path)
            .map_err(|e| ServerError::IoError(e))?;
        
        let mut contents = String::new();
        file.read_to_string(&mut contents)
            .map_err(|e| ServerError::IoError(e))?;
        
        // 解析 JSON
        match serde_json::from_str::<SharedData>(&contents) {
            Ok(data) => Ok(data),
            Err(e) => {
                // 数据损坏，记录警告并返回空数据
                log::warn!("共享数据文件损坏: {}, 将重建数据", e);
                Ok(SharedData {
                    servers: Vec::new(),
                    last_update: chrono::Utc::now().timestamp_millis(),
                    instance_id: self.instance_id.clone(),
                })
            }
        }
    }
    
    /// 写入共享数据
    pub async fn write_shared_data(&self, data: &SharedData) -> Result<(), ServerError> {
        // 获取文件锁
        let _lock = self.acquire_lock().await?;
        
        // 序列化为 JSON
        let json = serde_json::to_string_pretty(data)
            .map_err(|e| ServerError::DataShareError(format!("序列化失败: {}", e)))?;
        
        // 原子写入（先写临时文件，再重命名）
        let temp_path = self.shared_file_path.with_extension("tmp");
        
        let mut file = File::create(&temp_path)
            .map_err(|e| ServerError::IoError(e))?;
        
        file.write_all(json.as_bytes())
            .map_err(|e| ServerError::IoError(e))?;
        
        file.sync_all()
            .map_err(|e| ServerError::IoError(e))?;
        
        drop(file);
        
        // 重命名为正式文件
        std::fs::rename(&temp_path, &self.shared_file_path)
            .map_err(|e| ServerError::IoError(e))?;
        
        Ok(())
    }
    
    /// 通知其他实例（通过更新时间戳）
    pub async fn notify_instances(&self) -> Result<(), ServerError> {
        // 读取当前数据
        let mut data = self.read_shared_data().await?;
        
        // 更新时间戳
        data.last_update = chrono::Utc::now().timestamp_millis();
        data.instance_id = self.instance_id.clone();
        
        // 写回
        self.write_shared_data(&data).await?;
        
        Ok(())
    }
    
    /// 获取当前实例 ID
    pub fn get_instance_id(&self) -> &str {
        &self.instance_id
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_create_data_share_layer() {
        let layer = DataShareLayer::new().unwrap();
        assert!(!layer.instance_id.is_empty());
    }
    
    #[tokio::test]
    async fn test_read_write_shared_data() {
        let layer = DataShareLayer::new().unwrap();
        
        // 创建测试数据
        let test_data = SharedData {
            servers: vec![],
            last_update: chrono::Utc::now().timestamp_millis(),
            instance_id: layer.instance_id.clone(),
        };
        
        // 写入
        layer.write_shared_data(&test_data).await.unwrap();
        
        // 读取
        let read_data = layer.read_shared_data().await.unwrap();
        
        assert_eq!(read_data.servers.len(), 0);
        assert_eq!(read_data.instance_id, test_data.instance_id);
    }
    
    #[tokio::test]
    async fn test_corrupted_data_recovery() {
        let layer = DataShareLayer::new().unwrap();
        
        // 写入损坏的数据
        let mut file = File::create(&layer.shared_file_path).unwrap();
        file.write_all(b"{ invalid json }").unwrap();
        drop(file);
        
        // 读取应该返回空数据而不是错误
        let data = layer.read_shared_data().await.unwrap();
        assert_eq!(data.servers.len(), 0);
    }
}
