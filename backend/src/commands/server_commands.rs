// 服务管理命令 - Tauri IPC 命令实现

use crate::models::{ServerConfig, ServerInfo};
use crate::server::manager::ServerManager;
use tauri::{State, AppHandle};

/// 启动服务器
#[tauri::command]
pub async fn start_server(
    config: ServerConfig,
    manager: State<'_, ServerManager>,
    app: AppHandle,
) -> Result<ServerInfo, String> {
    let server_info = manager
        .start_server(config.clone())
        .await
        .map_err(|e| format!("启动服务失败: {}", e))?;
    
    // 自动打开浏览器（如果配置启用）
    // 注意：这里简化处理，实际应该从 AppConfig 读取配置
    // 为了不阻塞服务启动，我们在后台异步打开浏览器
    let url = server_info.local_url.clone();
    tokio::spawn(async move {
        #[cfg(not(target_os = "linux"))]
        {
            use tauri_plugin_opener::OpenerExt;
            if let Err(e) = app.opener().open_url(&url, None::<&str>) {
                log::warn!("自动打开浏览器失败: {}", e);
            }
        }
    });
    
    Ok(server_info)
}

/// 停止服务器
#[tauri::command]
pub async fn stop_server(
    server_id: String,
    manager: State<'_, ServerManager>,
) -> Result<(), String> {
    manager
        .stop_server(&server_id)
        .await
        .map_err(|e| format!("停止服务失败: {}", e))
}

/// 重启服务器
#[tauri::command]
pub async fn restart_server(
    server_id: String,
    manager: State<'_, ServerManager>,
) -> Result<ServerInfo, String> {
    manager
        .restart_server(&server_id)
        .await
        .map_err(|e| format!("重启服务失败: {}", e))
}

/// 列出所有服务器
#[tauri::command]
pub async fn list_servers(manager: State<'_, ServerManager>) -> Result<Vec<ServerInfo>, String> {
    Ok(manager.list_servers().await)
}

/// 获取服务器信息
#[tauri::command]
pub async fn get_server(
    server_id: String,
    manager: State<'_, ServerManager>,
) -> Result<Option<ServerInfo>, String> {
    Ok(manager.get_server(&server_id).await)
}
