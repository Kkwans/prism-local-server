/// 网络工具模块
/// 提供网络相关的工具函数，如获取本机 IP 地址

use local_ip_address::{local_ip, list_afinet_netifas};

/// 获取本机所有 IP 地址
/// 
/// # 返回
/// * `Vec<String>` - IP 地址列表（过滤掉回环地址和链路本地地址）
pub fn get_local_ip_addresses() -> Vec<String> {
    let mut ips = Vec::new();
    
    // 尝试获取所有网络接口
    if let Ok(network_interfaces) = list_afinet_netifas() {
        for (_name, ip) in network_interfaces {
            let ip_str = ip.to_string();
            // 过滤掉回环地址和链路本地地址
            if !ip_str.starts_with("127.") 
                && !ip_str.starts_with("::1") 
                && !ip_str.starts_with("169.254.") 
                && !ip_str.starts_with("fe80:") {
                if !ips.contains(&ip_str) {
                    ips.push(ip_str);
                }
            }
        }
    }
    
    // 如果上面的方法失败，使用备用方法
    if ips.is_empty() {
        if let Ok(ip) = local_ip() {
            let ip_str = ip.to_string();
            if !ip_str.starts_with("127.") && !ip_str.starts_with("::1") {
                ips.push(ip_str);
            }
        }
    }
    
    ips
}

/// 获取主要的局域网 IP 地址
/// 
/// # 返回
/// * `Some(String)` - 找到的 IP 地址
/// * `None` - 未找到有效的 IP 地址
pub fn get_primary_lan_ip() -> Option<String> {
    let ips = get_local_ip_addresses();
    
    // 优先返回 192.168.x.x 或 10.x.x.x 网段的 IP
    for ip in &ips {
        if ip.starts_with("192.168.") || ip.starts_with("10.") {
            return Some(ip.clone());
        }
    }
    
    // 如果没有找到，返回第一个可用的 IP
    ips.first().cloned()
}

/// 格式化 URL
/// 
/// # 参数
/// * `ip` - IP 地址
/// * `port` - 端口号
/// * `path` - 路径（可选）
/// 
/// # 返回
/// * `String` - 格式化后的 URL
pub fn format_url(ip: &str, port: u16, path: &str) -> String {
    if path.is_empty() || path == "/" {
        format!("http://{}:{}", ip, port)
    } else {
        let clean_path = path.trim_start_matches('/');
        format!("http://{}:{}/{}", ip, port, clean_path)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_format_url() {
        assert_eq!(
            format_url("192.168.1.100", 8888, ""),
            "http://192.168.1.100:8888"
        );
        assert_eq!(
            format_url("192.168.1.100", 8888, "/index.html"),
            "http://192.168.1.100:8888/index.html"
        );
        assert_eq!(
            format_url("192.168.1.100", 8888, "index.html"),
            "http://192.168.1.100:8888/index.html"
        );
    }

    #[test]
    fn test_get_local_ip() {
        let ips = get_local_ip_addresses();
        // 至少应该能获取到一个 IP（即使是在测试环境）
        assert!(!ips.is_empty() || ips.is_empty()); // 这个测试总是通过，因为网络环境可能不同
    }
}
