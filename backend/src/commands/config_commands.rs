// 配置管理命令 - Tauri IPC 命令实现

use crate::config::manager::ConfigManager;
use crate::models::AppConfig;
use tauri::State;
use std::sync::Arc;
use tokio::sync::Mutex;

/// 配置管理器状态（全局单例）
pub type ConfigManagerState = Arc<Mutex<ConfigManager>>;

/// 加载应用配置
///
/// # 返回
/// * `Result<AppConfig, String>` - 成功返回配置对象，失败返回错误信息
#[tauri::command]
pub async fn load_app_config(
    config_manager: State<'_, ConfigManagerState>,
) -> Result<AppConfig, String> {
    let manager = config_manager.lock().await;
    manager
        .load_config()
        .await
        .map_err(|e| format!("加载配置失败: {}", e))
}

/// 保存应用配置
///
/// # 参数
/// * `config` - 要保存的配置对象
///
/// # 返回
/// * `Result<(), String>` - 成功返回 ()，失败返回错误信息
#[tauri::command]
pub async fn save_app_config(
    config: AppConfig,
    config_manager: State<'_, ConfigManagerState>,
) -> Result<(), String> {
    let manager = config_manager.lock().await;
    manager
        .save_config(&config)
        .await
        .map_err(|e| format!("保存配置失败: {}", e))
}

/// 获取 EXE 所在目录
///
/// # 返回
/// * `Result<String, String>` - 成功返回目录路径，失败返回错误信息
#[tauri::command]
pub async fn get_executable_directory() -> Result<String, String> {
    ConfigManager::get_executable_directory()
        .and_then(|path| {
            path.to_str()
                .map(|s| s.to_string())
                .ok_or_else(|| {
                    crate::errors::ConfigError::ValidationError(
                        "无法转换路径为字符串".to_string(),
                    )
                })
        })
        .map_err(|e| format!("获取 EXE 目录失败: {}", e))
}
