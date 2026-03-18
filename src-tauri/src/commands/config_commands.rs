// 配置管理命令 - Tauri IPC 命令实现

use crate::config::manager::{load_config, save_config};
use crate::models::AppConfig;

/// 加载配置
#[tauri::command]
pub async fn load_app_config() -> Result<AppConfig, String> {
    load_config().map_err(|e| format!("加载配置失败: {}", e))
}

/// 保存配置
#[tauri::command]
pub async fn save_app_config(config: AppConfig) -> Result<(), String> {
    save_config(&config).map_err(|e| format!("保存配置失败: {}", e))
}
