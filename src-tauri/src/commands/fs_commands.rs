// 文件系统命令 - Tauri IPC 命令实现

use std::path::PathBuf;
use tauri::AppHandle;
use tauri_plugin_dialog::DialogExt;

/// 选择目录
#[tauri::command]
pub async fn select_directory(app: AppHandle) -> Result<Option<String>, String> {
    let dialog = app.dialog().file();
    
    // 使用 blocking 方式打开目录选择对话框
    let result = dialog.blocking_pick_folder();
    
    Ok(result.map(|path| path.to_string()))
}

/// 扫描目录下的 HTML 文件
#[tauri::command]
pub async fn scan_html_files(directory: String) -> Result<Vec<String>, String> {
    let dir_path = PathBuf::from(&directory);
    
    if !dir_path.exists() {
        return Err(format!("目录不存在: {}", directory));
    }
    
    if !dir_path.is_dir() {
        return Err(format!("路径不是目录: {}", directory));
    }
    
    let mut html_files = Vec::new();
    
    // 读取目录内容
    let entries = std::fs::read_dir(&dir_path)
        .map_err(|e| format!("读取目录失败: {}", e))?;
    
    for entry in entries {
        let entry = entry.map_err(|e| format!("读取目录项失败: {}", e))?;
        let path = entry.path();
        
        if path.is_file() {
            if let Some(extension) = path.extension() {
                if extension == "html" || extension == "htm" {
                    if let Some(file_name) = path.file_name() {
                        html_files.push(file_name.to_string_lossy().to_string());
                    }
                }
            }
        }
    }
    
    // 优先返回 index.html 和 messages.html
    html_files.sort_by(|a, b| {
        let a_lower = a.to_lowercase();
        let b_lower = b.to_lowercase();
        
        if a_lower == "index.html" {
            std::cmp::Ordering::Less
        } else if b_lower == "index.html" {
            std::cmp::Ordering::Greater
        } else if a_lower == "messages.html" {
            std::cmp::Ordering::Less
        } else if b_lower == "messages.html" {
            std::cmp::Ordering::Greater
        } else {
            a.cmp(b)
        }
    });
    
    Ok(html_files)
}
