/// 端口管理工具模块
/// 提供端口可用性检测和自动分配功能

use std::net::TcpListener;

/// 端口范围常量
const MIN_PORT: u16 = 1024;
const MAX_PORT: u16 = 65535;

/// 检查端口是否可用
/// 
/// # 参数
/// * `port` - 要检查的端口号
/// 
/// # 返回
/// * `true` - 端口可用
/// * `false` - 端口被占用
pub fn check_port_availability(port: u16) -> bool {
    TcpListener::bind(("0.0.0.0", port)).is_ok()
}

/// 从指定端口开始查找可用端口
/// 
/// # 参数
/// * `start_port` - 起始端口号
/// * `max_attempts` - 最大尝试次数
/// 
/// # 返回
/// * `Some(port)` - 找到的可用端口
/// * `None` - 未找到可用端口
pub fn find_available_port(start_port: u16, max_attempts: u16) -> Option<u16> {
    let mut port = start_port;
    let mut attempts = 0;
    
    while attempts < max_attempts && port <= MAX_PORT {
        if check_port_availability(port) {
            return Some(port);
        }
        port += 1;
        attempts += 1;
    }
    
    None
}

/// 检查端口是否在有效范围内
/// 
/// # 参数
/// * `port` - 要检查的端口号
/// 
/// # 返回
/// * `true` - 端口在有效范围内 (1024-65535)
/// * `false` - 端口超出有效范围
pub fn is_port_in_valid_range(port: u16) -> bool {
    port >= MIN_PORT && port <= MAX_PORT
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_port_range_validation() {
        assert!(!is_port_in_valid_range(80));
        assert!(is_port_in_valid_range(8080));
        assert!(is_port_in_valid_range(65535));
    }

    #[test]
    fn test_find_available_port() {
        let port = find_available_port(8888, 100);
        assert!(port.is_some());
        assert!(port.unwrap() >= 8888);
    }
}
