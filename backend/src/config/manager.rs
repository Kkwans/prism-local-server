// 配置管理器 - 负责加载、保存和验证应用配置

use crate::models::AppConfig;
use crate::errors::ConfigError;
use std::path::PathBuf;
use std::sync::Arc;
use tokio::sync::RwLock;
use tokio::fs;

/// 配置管理器
/// 
/// 负责应用配置的加载、保存、验证和管理
pub struct ConfigManager {
    /// 配置文件路径
    config_path: PathBuf,
    /// 当前配置（线程安全）
    config: Arc<RwLock<AppConfig>>,
}

impl ConfigManager {
    /// 创建新的配置管理器
    ///
    /// # 返回
    /// * `Result<Self, ConfigError>` - 成功返回 ConfigManager 实例，失败返回错误
    pub async fn new() -> Result<Self, ConfigError> {
        let config_path = Self::get_config_path()?;
        let config = Self::load_config_from_file(&config_path).await?;
        
        Ok(Self {
            config_path,
            config: Arc::new(RwLock::new(config)),
        })
    }
    
    /// 获取配置文件路径
    ///
    /// # 返回
    /// * `Result<PathBuf, ConfigError>` - 配置文件路径
    ///
    /// # 路径
    /// Windows: `%APPDATA%/prism-local-server/config.json`
    fn get_config_path() -> Result<PathBuf, ConfigError> {
        let config_dir = dirs::config_dir()
            .ok_or_else(|| ConfigError::ValidationError("无法获取配置目录".to_string()))?;
        
        let app_config_dir = config_dir.join("prism-local-server");
        
        // 确保配置目录存在
        if !app_config_dir.exists() {
            std::fs::create_dir_all(&app_config_dir)?;
        }
        
        Ok(app_config_dir.join("config.json"))
    }
    
    /// 从文件加载配置
    ///
    /// # 参数
    /// * `path` - 配置文件路径
    ///
    /// # 返回
    /// * `Result<AppConfig, ConfigError>` - 配置对象
    async fn load_config_from_file(path: &PathBuf) -> Result<AppConfig, ConfigError> {
        // 如果配置文件不存在，返回默认配置
        if !path.exists() {
            log::info!("配置文件不存在，使用默认配置");
            return Ok(Self::init_default_config());
        }
        
        // 读取配置文件
        let content = fs::read_to_string(path).await?;
        
        // 解析 JSON
        let config: AppConfig = match serde_json::from_str(&content) {
            Ok(cfg) => cfg,
            Err(e) => {
                log::warn!("配置文件格式错误: {}, 使用默认配置", e);
                // 配置文件损坏时使用默认配置
                Self::init_default_config()
            }
        };
        
        // 验证配置
        Self::validate_config(&config)?;
        
        Ok(config)
    }
    
    /// 初始化默认配置
    ///
    /// # 返回
    /// * `AppConfig` - 默认配置对象
    pub fn init_default_config() -> AppConfig {
        // 尝试获取 EXE 所在目录作为默认部署目录
        let default_dir = Self::get_executable_directory()
            .ok()
            .and_then(|path| path.to_str().map(|s| s.to_string()))
            .unwrap_or_else(|| {
                // 如果无法获取 EXE 目录，回退到用户文档目录
                dirs::document_dir()
                    .and_then(|path| path.to_str().map(|s| s.to_string()))
                    .unwrap_or_else(|| ".".to_string())
            });
        
        AppConfig {
            default_port: 8888,
            default_directory: default_dir,
            default_entry_file: "index.html".to_string(),
            theme: "system".to_string(),
            auto_open_browser: true,
            minimize_to_tray: true,
            is_directory_user_set: false,
        }
    }
    
    /// 验证配置有效性
    ///
    /// # 参数
    /// * `config` - 要验证的配置
    ///
    /// # 返回
    /// * `Result<(), ConfigError>` - 验证通过返回 ()，失败返回错误
    pub fn validate_config(config: &AppConfig) -> Result<(), ConfigError> {
        // 验证端口范围
        if config.default_port < 1024 {
            return Err(ConfigError::ValidationError(format!(
                "端口 {} 小于最小值 1024",
                config.default_port
            )));
        }

        // 验证入口文件名非空
        if config.default_entry_file.trim().is_empty() {
            return Err(ConfigError::ValidationError(
                "入口文件名不能为空".to_string(),
            ));
        }

        Ok(())
    }
    
    /// 加载配置
    ///
    /// # 返回
    /// * `Result<AppConfig, ConfigError>` - 当前配置的克隆
    pub async fn load_config(&self) -> Result<AppConfig, ConfigError> {
        let mut config = self.config.read().await.clone();
        
        // 如果目录未被用户手动设置，且当前为空，则自动填充 EXE 目录
        if !config.is_directory_user_set && config.default_directory.is_empty() {
            if let Ok(exe_dir) = Self::get_executable_directory() {
                if let Some(dir_str) = exe_dir.to_str() {
                    config.default_directory = dir_str.to_string();
                    log::info!("自动填充默认部署目录: {}", dir_str);
                }
            }
        }
        
        Ok(config)
    }
    
    /// 保存配置（使用原子写入）
    ///
    /// # 参数
    /// * `config` - 要保存的配置
    ///
    /// # 返回
    /// * `Result<(), ConfigError>` - 成功返回 ()，失败返回错误
    ///
    /// # 原子写入流程
    /// 1. 验证配置有效性
    /// 2. 序列化为 JSON
    /// 3. 写入临时文件
    /// 4. 重命名临时文件为正式文件（原子操作）
    pub async fn save_config(&self, config: &AppConfig) -> Result<(), ConfigError> {
        // 1. 验证配置
        Self::validate_config(config)?;
        
        // 2. 序列化为 JSON
        let content = serde_json::to_string_pretty(config)?;
        
        // 3. 写入临时文件
        let temp_path = self.config_path.with_extension("tmp");
        fs::write(&temp_path, &content).await?;
        
        // 4. 原子重命名（Windows 上需要先删除目标文件）
        if self.config_path.exists() {
            fs::remove_file(&self.config_path).await?;
        }
        fs::rename(&temp_path, &self.config_path).await?;
        
        // 5. 更新内存中的配置
        let mut current_config = self.config.write().await;
        *current_config = config.clone();
        
        log::info!("配置已保存到: {:?}", self.config_path);
        Ok(())
    }
    
    /// 获取 EXE 所在目录
    ///
    /// # 返回
    /// * `Result<PathBuf, ConfigError>` - EXE 所在目录路径
    pub fn get_executable_directory() -> Result<PathBuf, ConfigError> {
        let exe_path = std::env::current_exe()
            .map_err(|e| ConfigError::ValidationError(format!("无法获取 EXE 路径: {}", e)))?;
        
        let exe_dir = exe_path
            .parent()
            .ok_or_else(|| ConfigError::ValidationError("无法获取 EXE 所在目录".to_string()))?
            .to_path_buf();
        
        Ok(exe_dir)
    }
}

// 保留向后兼容的函数接口

/// 获取默认配置
pub fn get_default_config() -> AppConfig {
    ConfigManager::init_default_config()
}

/// 验证配置有效性
pub fn validate_config(config: &AppConfig) -> Result<(), ConfigError> {
    ConfigManager::validate_config(config)
}

/// 获取配置文件路径
pub fn get_config_path() -> Result<PathBuf, ConfigError> {
    ConfigManager::get_config_path()
}

/// 加载配置
pub fn load_config() -> Result<AppConfig, ConfigError> {
    let config_path = get_config_path()?;
    
    // 如果配置文件不存在，返回默认配置
    if !config_path.exists() {
        return Ok(get_default_config());
    }
    
    // 读取配置文件
    let content = std::fs::read_to_string(&config_path)?;
    
    // 解析 JSON
    let config: AppConfig = serde_json::from_str(&content)?;
    
    // 验证配置
    validate_config(&config)?;
    
    Ok(config)
}

/// 保存配置
pub fn save_config(config: &AppConfig) -> Result<(), ConfigError> {
    // 验证配置
    validate_config(config)?;
    
    let config_path = get_config_path()?;
    
    // 序列化为 JSON
    let content = serde_json::to_string_pretty(config)?;
    
    // 写入文件
    std::fs::write(&config_path, content)?;
    
    Ok(())
}
