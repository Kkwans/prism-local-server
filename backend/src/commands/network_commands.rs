// 网络工具命令 - Tauri IPC 命令实现

use crate::utils::network::get_primary_lan_ip;
use crate::utils::port::check_port_availability;

/// 检查端口可用性
#[tauri::command]
pub async fn check_port(port: u16) -> Result<bool, String> {
    Ok(check_port_availability(port))
}

/// 获取局域网 IP 地址
#[tauri::command]
pub async fn get_lan_ip() -> Result<Vec<String>, String> {
    match get_primary_lan_ip() {
        Some(ip) => Ok(vec![ip]),
        None => Ok(vec!["127.0.0.1".to_string()]),
    }
}
