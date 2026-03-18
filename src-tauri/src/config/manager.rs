// 配置管理器 - 负责加载、保存和验证应用配置

use crate::models::AppConfig;
use crate::errors::ConfigError;
use std::path::PathBuf;

/// 获取默认配置
pub fn get_default_config() -> AppConfig {
    AppConfig {
        default_port: 8888,
        default_directory: String::new(),
        default_entry_file: "index.html".to_string(),
        theme: "system".to_string(),
        auto_open_browser: true,
        minimize_to_tray: true,
    }
}

/// 验证配置有效性
pub fn validate_config(config: &AppConfig) -> Result<(), ConfigError> {
    // 验证端口范围 (u16 类型最大值是 65535，所以只需检查下限)
    if config.default_port < 1024 {
        return Err(ConfigError::ValidationError(format!("端口 {} 小于最小值 1024", config.default_port)));
    }

    // 验证入口文件名非空
    if config.default_entry_file.trim().is_empty() {
        return Err(ConfigError::ValidationError("入口文件名不能为空".to_string()));
    }

    Ok(())
}

/// 获取配置文件路径
pub fn get_config_path() -> Result<PathBuf, ConfigError> {
    let config_dir = dirs::config_dir()
        .ok_or_else(|| ConfigError::ValidationError("无法获取配置目录".to_string()))?;
    
    let app_config_dir = config_dir.join("prism-local-server");
    
    // 确保配置目录存在
    if !app_config_dir.exists() {
        std::fs::create_dir_all(&app_config_dir)?;
    }
    
    Ok(app_config_dir.join("config.json"))
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
