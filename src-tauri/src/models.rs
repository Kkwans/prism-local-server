/// 数据模型模块
/// 定义应用程序使用的所有数据结构

use serde::{Deserialize, Serialize};

/// 服务器配置
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ServerConfig {
    /// 端口号，默认 8888
    #[serde(default = "default_port")]
    pub port: u16,
    
    /// 部署目录，默认当前目录
    #[serde(default = "default_directory")]
    pub directory: String,
    
    /// 入口 HTML 文件名，默认 index.html
    #[serde(default = "default_entry_file")]
    pub entry_file: String,
}

fn default_port() -> u16 {
    8888
}

fn default_directory() -> String {
    ".".to_string()
}

fn default_entry_file() -> String {
    "index.html".to_string()
}

/// 服务器状态
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ServerStatus {
    /// 运行中
    Running,
    /// 已停止
    Stopped,
}

/// 服务器信息
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ServerInfo {
    /// 服务唯一标识符（UUID）
    pub id: String,
    /// 服务名称（从目录提取）
    pub name: String,
    /// 监听端口
    pub port: u16,
    /// 部署目录路径
    pub directory: String,
    /// 入口 HTML 文件名
    pub entry_file: String,
    /// 运行状态
    pub status: ServerStatus,
    /// 启动时间戳（毫秒）
    pub start_time: i64,
    /// 本地访问地址
    pub local_url: String,
    /// 局域网访问地址列表
    pub lan_urls: Vec<String>,
}

/// 应用配置
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppConfig {
    /// 默认端口号
    #[serde(default = "default_port")]
    pub default_port: u16,
    
    /// 默认部署目录
    #[serde(default = "default_directory")]
    pub default_directory: String,
    
    /// 默认入口文件
    #[serde(default = "default_entry_file")]
    pub default_entry_file: String,
    
    /// 主题设置
    #[serde(default = "default_theme")]
    pub theme: String,
    
    /// 是否自动打开浏览器
    #[serde(default = "default_true")]
    pub auto_open_browser: bool,
    
    /// 是否最小化到托盘
    #[serde(default = "default_true")]
    pub minimize_to_tray: bool,
    
    /// 目录是否由用户手动设置（用于区分用户设置和自动识别）
    #[serde(default = "default_false")]
    pub is_directory_user_set: bool,
}

fn default_theme() -> String {
    "system".to_string()
}

fn default_true() -> bool {
    true
}

fn default_false() -> bool {
    false
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            default_port: default_port(),
            default_directory: default_directory(),
            default_entry_file: default_entry_file(),
            theme: default_theme(),
            auto_open_browser: true,
            minimize_to_tray: true,
            is_directory_user_set: false,
        }
    }
}
