// 服务管理器 - 管理多个 HTTP 服务器实例

use crate::errors::ServerError;
use crate::models::{ServerConfig, ServerInfo, ServerStatus};
use crate::server::handler::handle_static_file;
use crate::server::namer::ServiceNamer;
use crate::server::data_share::{DataShareLayer, SharedData};
use crate::utils::network::get_primary_lan_ip;
use crate::utils::port::{check_port_availability, find_available_port};
use axum::Router;
use std::collections::HashMap;
use std::net::SocketAddr;
use std::path::PathBuf;
use std::sync::Arc;
use tokio::sync::{oneshot, RwLock};
use tokio::task::JoinHandle;

/// 服务器实例信息
struct ServerInstance {
    /// 服务器基本信息
    info: ServerInfo,
    /// 异步任务句柄
    task_handle: JoinHandle<()>,
    /// 优雅关闭信号发送器
    shutdown_tx: Option<oneshot::Sender<()>>,
}

/// 服务管理器状态
#[derive(Clone)]
pub struct ServerManager {
    /// 运行中的服务实例映射表（服务 ID -> 实例）
    servers: Arc<RwLock<HashMap<String, ServerInstance>>>,
    /// 服务命名器
    namer: ServiceNamer,
    /// 数据共享层
    data_share: Arc<DataShareLayer>,
}

impl ServerManager {
    /// 创建新的服务管理器
    pub fn new() -> Self {
        let data_share = DataShareLayer::new()
            .expect("无法初始化数据共享层");
        
        Self {
            servers: Arc::new(RwLock::new(HashMap::new())),
            namer: ServiceNamer::new(),
            data_share: Arc::new(data_share),
        }
    }
    
    /// 从共享数据初始化服务列表
    pub async fn init_from_shared_data(&self) -> Result<(), ServerError> {
        let shared_data = self.data_share.read_shared_data().await?;
        
        // 注意：这里只读取共享数据用于显示
        // 实际的服务进程由各自的应用实例管理
        log::info!("从共享数据加载了 {} 个服务", shared_data.servers.len());
        
        Ok(())
    }

    /// 启动服务器
    pub async fn start_server(&self, config: ServerConfig) -> Result<ServerInfo, ServerError> {
        // 验证配置
        self.validate_config(&config)?;

        // 检查目录唯一性
        self.check_directory_uniqueness(&config.directory).await?;

        // 检查端口可用性，如果不可用则自动递增查找
        let port = if check_port_availability(config.port) {
            config.port
        } else {
            find_available_port(config.port, 100)
                .ok_or_else(|| ServerError::PortUnavailable(config.port))?
        };

        // 生成服务 ID
        let server_id = uuid::Uuid::new_v4().to_string();

        // 生成服务名称（从目录路径提取）
        let service_name = self.namer.generate_service_name(&config.directory);

        // 获取局域网 IP
        let lan_ip = get_primary_lan_ip().unwrap_or_else(|| "127.0.0.1".to_string());

        // 构造访问地址
        let local_url = format!("http://127.0.0.1:{}/{}", port, config.entry_file);
        let lan_urls = vec![format!("http://{}:{}/{}", lan_ip, port, config.entry_file)];

        // 创建服务器信息
        let server_info = ServerInfo {
            id: server_id.clone(),
            name: service_name,
            port,
            directory: config.directory.clone(),
            entry_file: config.entry_file.clone(),
            status: ServerStatus::Running,
            local_url: local_url.clone(),
            lan_urls: lan_urls.clone(),
            start_time: chrono::Utc::now().timestamp_millis(),
        };

        // 创建优雅关闭通道
        let (shutdown_tx, shutdown_rx) = oneshot::channel();

        // 启动 HTTP 服务器
        let root_dir = PathBuf::from(&config.directory);
        let task_handle = tokio::spawn(async move {
            if let Err(e) = start_http_server(root_dir, port, shutdown_rx).await {
                eprintln!("服务器错误: {}", e);
            }
        });

        // 保存服务器实例
        let instance = ServerInstance {
            info: server_info.clone(),
            task_handle,
            shutdown_tx: Some(shutdown_tx),
        };

        let mut servers = self.servers.write().await;
        servers.insert(server_id, instance);
        
        // 同步到共享数据
        let all_servers: Vec<ServerInfo> = servers.values()
            .map(|inst| inst.info.clone())
            .collect();
        drop(servers); // 释放锁
        
        let shared_data = SharedData {
            servers: all_servers,
            last_update: chrono::Utc::now().timestamp_millis(),
            instance_id: self.data_share.get_instance_id().to_string(),
        };
        
        if let Err(e) = self.data_share.write_shared_data(&shared_data).await {
            log::warn!("写入共享数据失败: {}", e);
        }

        Ok(server_info)
    }

    /// 停止服务器
    pub async fn stop_server(&self, server_id: &str) -> Result<(), ServerError> {
        let mut servers = self.servers.write().await;

        let mut instance = servers
            .remove(server_id)
            .ok_or_else(|| ServerError::ServerNotFound(server_id.to_string()))?;

        // 发送优雅关闭信号
        if let Some(shutdown_tx) = instance.shutdown_tx.take() {
            let _ = shutdown_tx.send(());
        }

        // 中止任务
        instance.task_handle.abort();
        
        // 同步到共享数据
        let all_servers: Vec<ServerInfo> = servers.values()
            .map(|inst| inst.info.clone())
            .collect();
        drop(servers); // 释放锁
        
        let shared_data = SharedData {
            servers: all_servers,
            last_update: chrono::Utc::now().timestamp_millis(),
            instance_id: self.data_share.get_instance_id().to_string(),
        };
        
        if let Err(e) = self.data_share.write_shared_data(&shared_data).await {
            log::warn!("写入共享数据失败: {}", e);
        }

        Ok(())
    }

    /// 重启服务器
    pub async fn restart_server(&self, server_id: &str) -> Result<ServerInfo, ServerError> {
        // 获取原服务器配置
        let config = {
            let servers = self.servers.read().await;
            let instance = servers
                .get(server_id)
                .ok_or_else(|| ServerError::ServerNotFound(server_id.to_string()))?;

            ServerConfig {
                port: instance.info.port,
                directory: instance.info.directory.clone(),
                entry_file: instance.info.entry_file.clone(),
            }
        };

        // 停止服务器
        self.stop_server(server_id).await?;

        // 启动新服务器
        self.start_server(config).await
    }

    /// 列出所有服务器
    pub async fn list_servers(&self) -> Vec<ServerInfo> {
        let servers = self.servers.read().await;
        servers.values().map(|instance| instance.info.clone()).collect()
    }

    /// 获取服务器信息
    pub async fn get_server(&self, server_id: &str) -> Option<ServerInfo> {
        let servers = self.servers.read().await;
        servers.get(server_id).map(|instance| instance.info.clone())
    }

    /// 检查部署目录唯一性
    async fn check_directory_uniqueness(&self, directory: &str) -> Result<(), ServerError> {
        let servers = self.servers.read().await;
        
        // 规范化路径（转换为绝对路径）
        let target_path = PathBuf::from(directory)
            .canonicalize()
            .map_err(|_| ServerError::DirectoryNotFound(directory.to_string()))?;

        // 检查是否有服务正在使用该目录
        for instance in servers.values() {
            let existing_path = PathBuf::from(&instance.info.directory)
                .canonicalize()
                .unwrap_or_else(|_| PathBuf::from(&instance.info.directory));

            if target_path == existing_path {
                return Err(ServerError::DirectoryInUse {
                    name: instance.info.name.clone(),
                    port: instance.info.port,
                });
            }
        }

        Ok(())
    }

    /// 验证配置
    fn validate_config(&self, config: &ServerConfig) -> Result<(), ServerError> {
        // 验证端口范围 (u16 类型最大值是 65535，所以只需检查下限)
        if config.port < 1024 {
            return Err(ServerError::InvalidPort(config.port));
        }

        // 验证目录存在性
        let dir_path = PathBuf::from(&config.directory);
        if !dir_path.exists() {
            return Err(ServerError::DirectoryNotFound(config.directory.clone()));
        }

        if !dir_path.is_dir() {
            return Err(ServerError::DirectoryNotFound(config.directory.clone()));
        }

        // 验证 HTML 文件存在性
        let html_path = dir_path.join(&config.entry_file);
        if !html_path.exists() {
            return Err(ServerError::EntryFileNotFound(config.entry_file.clone()));
        }

        Ok(())
    }
}

/// 启动 HTTP 服务器
async fn start_http_server(
    root_dir: PathBuf,
    port: u16,
    shutdown_rx: oneshot::Receiver<()>,
) -> Result<(), Box<dyn std::error::Error>> {
    let root_dir_clone = root_dir.clone();

    // 创建路由
    let app = Router::new()
        .fallback(move |req| {
            let root = root_dir_clone.clone();
            async move {
                handle_static_file(root, req)
                    .await
                    .unwrap_or_else(|status| {
                        axum::response::Response::builder()
                            .status(status)
                            .body(axum::body::Body::empty())
                            .unwrap()
                    })
            }
        })
        .layer(
            tower_http::cors::CorsLayer::permissive(), // 允许跨域
        );

    // 绑定地址
    let addr = SocketAddr::from(([0, 0, 0, 0], port));

    // 启动服务器
    let listener = tokio::net::TcpListener::bind(addr).await?;
    
    // 使用 with_graceful_shutdown 支持优雅关闭
    axum::serve(listener, app)
        .with_graceful_shutdown(async {
            shutdown_rx.await.ok();
        })
        .await?;

    Ok(())
}
