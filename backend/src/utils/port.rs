/// 端口管理工具模块
/// 提供端口可用性检测和自动分配功能

use std::net::TcpListener;
use std::time::Duration;
use tokio::net::TcpStream;
use tokio::time::timeout;

/// 端口范围常量
const MIN_PORT: u16 = 1024;
const MAX_PORT: u16 = 65535;
/// 最大尝试次数
const MAX_ATTEMPTS: u16 = 100;
/// 端口检测超时时间（毫秒）
const PORT_CHECK_TIMEOUT_MS: u64 = 50;

/// 端口管理器
/// 
/// 负责端口可用性检测和自动分配
pub struct PortManager;

impl PortManager {
    /// 创建新的端口管理器
    pub fn new() -> Self {
        Self
    }
    
    /// 异步检查端口是否可用
    /// 
    /// # 参数
    /// * `port` - 要检查的端口号
    /// 
    /// # 返回
    /// * `true` - 端口可用
    /// * `false` - 端口被占用或检测超时
    /// 
    /// # 超时
    /// 检测超时时间为 50ms，确保快速响应
    pub async fn check_port_available(&self, port: u16) -> bool {
        let addr = format!("127.0.0.1:{}", port);
        
        // 尝试连接端口，如果连接成功说明端口被占用
        let result = timeout(
            Duration::from_millis(PORT_CHECK_TIMEOUT_MS),
            TcpStream::connect(&addr),
        )
        .await;
        
        // 如果连接失败或超时，说明端口可用
        match result {
            Ok(Ok(_)) => false, // 连接成功，端口被占用
            Ok(Err(_)) => true, // 连接失败，端口可用
            Err(_) => true,     // 超时，端口可用
        }
    }
    
    /// 从指定端口开始查找可用端口（自动递增）
    /// 
    /// # 参数
    /// * `start_port` - 起始端口号
    /// 
    /// # 返回
    /// * `Some(port)` - 找到的可用端口
    /// * `None` - 未找到可用端口（尝试了 100 次）
    /// 
    /// # 限制
    /// - 端口范围: 1024-65535
    /// - 最大尝试次数: 100
    pub async fn find_available_port(&self, start_port: u16) -> Option<u16> {
        // 验证起始端口在有效范围内
        if start_port < MIN_PORT {
            log::warn!("起始端口 {} 小于最小值 {}", start_port, MIN_PORT);
            return None;
        }
        
        let mut port = start_port;
        let mut attempts = 0;
        
        while attempts < MAX_ATTEMPTS && port <= MAX_PORT {
            if self.check_port_available(port).await {
                log::info!("找到可用端口: {}", port);
                return Some(port);
            }
            port += 1;
            attempts += 1;
        }
        
        log::error!("未找到可用端口，起始端口: {}, 尝试次数: {}", start_port, attempts);
        None
    }
    
    /// 检查端口是否在有效范围内
    /// 
    /// # 参数
    /// * `port` - 要检查的端口号
    /// 
    /// # 返回
    /// * `true` - 端口在有效范围内 (1024-65535)
    /// * `false` - 端口超出有效范围
    pub fn is_port_in_valid_range(&self, port: u16) -> bool {
        port >= MIN_PORT && port <= MAX_PORT
    }
}

impl Default for PortManager {
    fn default() -> Self {
        Self::new()
    }
}

// 保留向后兼容的函数接口

/// 检查端口是否可用（同步版本）
/// 
/// # 参数
/// * `port` - 要检查的端口号
/// 
/// # 返回
/// * `true` - 端口可用
/// * `false` - 端口被占用
pub fn check_port_availability(port: u16) -> bool {
    TcpListener::bind(("0.0.0.0", port)).is_ok()
}

/// 从指定端口开始查找可用端口（同步版本）
/// 
/// # 参数
/// * `start_port` - 起始端口号
/// * `max_attempts` - 最大尝试次数
/// 
/// # 返回
/// * `Some(port)` - 找到的可用端口
/// * `None` - 未找到可用端口
pub fn find_available_port(start_port: u16, max_attempts: u16) -> Option<u16> {
    let mut port = start_port;
    let mut attempts = 0;
    
    while attempts < max_attempts && port <= MAX_PORT {
        if check_port_availability(port) {
            return Some(port);
        }
        port += 1;
        attempts += 1;
    }
    
    None
}

/// 检查端口是否在有效范围内
/// 
/// # 参数
/// * `port` - 要检查的端口号
/// 
/// # 返回
/// * `true` - 端口在有效范围内 (1024-65535)
/// * `false` - 端口超出有效范围
pub fn is_port_in_valid_range(port: u16) -> bool {
    port >= MIN_PORT && port <= MAX_PORT
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_port_range_validation() {
        assert!(!is_port_in_valid_range(80));
        assert!(is_port_in_valid_range(8080));
        assert!(is_port_in_valid_range(65535));
    }

    #[test]
    fn test_find_available_port() {
        let port = find_available_port(8888, 100);
        assert!(port.is_some());
        assert!(port.unwrap() >= 8888);
    }
    
    #[tokio::test]
    async fn test_port_manager_check_available() {
        let manager = PortManager::new();
        // 测试一个很可能可用的高端口
        let available = manager.check_port_available(54321).await;
        assert!(available);
    }
    
    #[tokio::test]
    async fn test_port_manager_find_available() {
        let manager = PortManager::new();
        let port = manager.find_available_port(8888).await;
        assert!(port.is_some());
        assert!(port.unwrap() >= 8888);
    }
}
