/// 日志记录工具模块
/// 
/// 提供统一的日志记录接口，支持输出到文件和控制台

use std::fs;
use std::path::PathBuf;

/// 初始化日志系统
/// 
/// 创建日志目录并配置日志输出
pub fn init_logger() -> Result<(), Box<dyn std::error::Error>> {
    // 创建日志目录
    let log_dir = get_log_dir()?;
    if !log_dir.exists() {
        fs::create_dir_all(&log_dir)?;
    }
    
    Ok(())
}

/// 获取日志目录路径
/// 
/// 返回应用数据目录下的 logs 子目录
pub fn get_log_dir() -> Result<PathBuf, Box<dyn std::error::Error>> {
    let app_data_dir = dirs::data_local_dir()
        .ok_or("无法获取应用数据目录")?;
    
    Ok(app_data_dir.join("prism-local-server").join("logs"))
}

/// 获取日志文件路径
pub fn get_log_file_path() -> Result<PathBuf, Box<dyn std::error::Error>> {
    Ok(get_log_dir()?.join("prism-server.log"))
}

/// 记录服务启动日志
pub fn log_server_start(server_id: &str, port: u16, directory: &str) {
    log::info!(
        "服务启动 - ID: {}, 端口: {}, 目录: {}",
        server_id,
        port,
        directory
    );
}

/// 记录服务停止日志
pub fn log_server_stop(server_id: &str) {
    log::info!("服务停止 - ID: {}", server_id);
}

/// 记录错误日志
pub fn log_error(context: &str, error: &dyn std::error::Error) {
    log::error!("{}: {}", context, error);
}

/// 记录警告日志
pub fn log_warning(message: &str) {
    log::warn!("{}", message);
}
