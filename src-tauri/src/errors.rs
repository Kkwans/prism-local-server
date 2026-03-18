/// 错误类型定义模块

use thiserror::Error;

/// 服务器错误类型
#[derive(Debug, Error)]
pub enum ServerError {
    /// 端口不可用
    #[error("端口 {0} 不可用")]
    PortUnavailable(u16),
    
    /// 端口超出有效范围
    #[error("端口 {0} 超出有效范围 (1024-65535)")]
    InvalidPort(u16),
    
    /// 目录不存在
    #[error("目录不存在: {0}")]
    DirectoryNotFound(String),
    
    /// 入口文件不存在
    #[error("入口文件不存在: {0}")]
    EntryFileNotFound(String),
    
    /// 服务未找到
    #[error("服务 {0} 未找到")]
    ServerNotFound(String),
    
    /// 服务启动失败
    #[error("服务启动失败: {0}")]
    StartFailed(String),
    
    /// 服务停止失败
    #[error("服务停止失败: {0}")]
    StopFailed(String),
    
    /// IO 错误
    #[error("IO 错误: {0}")]
    IoError(#[from] std::io::Error),
}

/// 配置错误类型
#[derive(Debug, Error)]
pub enum ConfigError {
    /// 配置文件不存在
    #[error("配置文件不存在: {0}")]
    FileNotFound(String),
    
    /// 配置文件格式错误
    #[error("配置文件格式错误: {0}")]
    ParseError(String),
    
    /// 配置验证失败
    #[error("配置验证失败: {0}")]
    ValidationError(String),
    
    /// IO 错误
    #[error("IO 错误: {0}")]
    IoError(#[from] std::io::Error),
    
    /// 序列化错误
    #[error("序列化错误: {0}")]
    SerdeError(#[from] serde_json::Error),
}
