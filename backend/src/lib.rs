// 模块声明
pub mod models;
pub mod errors;
pub mod utils;
pub mod config;
pub mod server;
pub mod commands;
pub mod git;
pub mod migration;

use server::manager::ServerManager;
use config::manager::ConfigManager;
use commands::config_commands::ConfigManagerState;
use tauri::{Manager, menu::{MenuBuilder, MenuItem}, tray::{TrayIconBuilder, TrayIconEvent}};
use std::sync::Arc;
use tokio::sync::Mutex;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .plugin(tauri_plugin_dialog::init())
    .plugin(tauri_plugin_fs::init())
    .plugin(tauri_plugin_shell::init())
    .plugin(tauri_plugin_opener::init())
    .setup(|app| {
      if cfg!(debug_assertions) {
        app.handle().plugin(
          tauri_plugin_log::Builder::default()
            .level(log::LevelFilter::Info)
            .build(),
        )?;
      }
      
      // 初始化配置管理器
      let config_manager = tauri::async_runtime::block_on(async {
        ConfigManager::new().await
      }).expect("无法初始化配置管理器");
      app.manage(Arc::new(Mutex::new(config_manager)) as ConfigManagerState);
      
      // 初始化服务管理器
      app.manage(ServerManager::new());
      
      // 创建系统托盘菜单
      let show_item = MenuItem::with_id(app, "show", "显示主窗口", true, None::<&str>)?;
      let quit_item = MenuItem::with_id(app, "quit", "退出程序", true, None::<&str>)?;
      let menu = MenuBuilder::new(app)
        .item(&show_item)
        .separator()
        .item(&quit_item)
        .build()?;
      
      // 创建系统托盘图标
      let _tray = TrayIconBuilder::new()
        .menu(&menu)
        .icon(app.default_window_icon().unwrap().clone())
        .on_menu_event(|app, event| {
          match event.id().as_ref() {
            "show" => {
              if let Some(window) = app.get_webview_window("main") {
                let _ = window.show();
                let _ = window.set_focus();
              }
            }
            "quit" => {
              app.exit(0);
            }
            _ => {}
          }
        })
        .on_tray_icon_event(|tray, event| {
          if let TrayIconEvent::Click { button: tauri::tray::MouseButton::Left, .. } = event {
            let app = tray.app_handle();
            if let Some(window) = app.get_webview_window("main") {
              let _ = window.show();
              let _ = window.set_focus();
            }
          }
        })
        .build(app)?;
      
      Ok(())
    })
    .on_window_event(|window, event| {
      if let tauri::WindowEvent::CloseRequested { api, .. } = event {
        // 隐藏窗口而非退出
        window.hide().unwrap();
        api.prevent_close();
      }
    })
    .invoke_handler(tauri::generate_handler![
      // 服务管理命令
      commands::server_commands::start_server,
      commands::server_commands::stop_server,
      commands::server_commands::restart_server,
      commands::server_commands::list_servers,
      commands::server_commands::get_server,
      // 配置管理命令
      commands::config_commands::load_app_config,
      commands::config_commands::save_app_config,
      commands::config_commands::get_executable_directory,
      // 网络工具命令
      commands::network_commands::check_port,
      commands::network_commands::get_lan_ip,
      // 文件系统命令
      commands::fs_commands::select_directory,
      commands::fs_commands::scan_html_files,
    ])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
