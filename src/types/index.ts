// 类型定义 - 与 Rust 后端数据模型保持一致

export type ServerStatus = 'running' | 'stopped';

export interface ServerConfig {
  port: number;
  directory: string;
  entry_file: string;
}

export interface ServerInfo {
  id: string;
  name: string;
  port: number;
  directory: string;
  entry_file: string;
  status: ServerStatus;
  start_time: number;
  local_url: string;
  lan_urls: string[];
}

export interface AppConfig {
  default_port: number;
  default_directory: string;
  default_entry_file: string;
  theme: string;
  auto_open_browser: boolean;
  minimize_to_tray: boolean;
}
