// HTTP Range Request 处理器 - 支持视频拖拽播放和断点续传

use axum::http::HeaderMap;
use std::ops::Range;

/// Range 请求信息
#[derive(Debug, Clone)]
pub struct RangeInfo {
    pub start: u64,
    pub end: u64,
    pub total_size: u64,
}

impl RangeInfo {
    /// 获取内容范围
    pub fn content_range(&self) -> Range<u64> {
        self.start..self.end + 1
    }

    /// 获取内容长度
    pub fn content_length(&self) -> u64 {
        self.end - self.start + 1
    }

    /// 生成 Content-Range 响应头值
    pub fn content_range_header(&self) -> String {
        format!("bytes {}-{}/{}", self.start, self.end, self.total_size)
    }
}

/// 解析 Range 请求头
/// 
/// 支持格式：
/// - bytes=0-499 (前 500 字节)
/// - bytes=500-999 (500-999 字节)
/// - bytes=500- (从 500 字节到文件末尾)
/// - bytes=-500 (最后 500 字节)
pub fn parse_range_header(
    headers: &HeaderMap,
    file_size: u64,
) -> Option<RangeInfo> {
    let range_header = headers.get("range")?.to_str().ok()?;
    
    // 检查是否以 "bytes=" 开头
    if !range_header.starts_with("bytes=") {
        return None;
    }
    
    let range_str = &range_header[6..]; // 跳过 "bytes="
    
    // 解析范围（目前只支持单范围请求）
    let parts: Vec<&str> = range_str.split('-').collect();
    if parts.len() != 2 {
        return None;
    }
    
    let (start, end) = if parts[0].is_empty() {
        // bytes=-500 格式（最后 N 字节）
        let suffix_length: u64 = parts[1].parse().ok()?;
        let start = file_size.saturating_sub(suffix_length);
        (start, file_size - 1)
    } else if parts[1].is_empty() {
        // bytes=500- 格式（从 N 到末尾）
        let start: u64 = parts[0].parse().ok()?;
        (start, file_size - 1)
    } else {
        // bytes=500-999 格式（指定范围）
        let start: u64 = parts[0].parse().ok()?;
        let end: u64 = parts[1].parse::<u64>().ok()?.min(file_size - 1);
        (start, end)
    };
    
    // 验证范围有效性
    if start > end || start >= file_size {
        return None;
    }
    
    Some(RangeInfo {
        start,
        end,
        total_size: file_size,
    })
}

/// 检查是否为 Range 请求
pub fn is_range_request(headers: &HeaderMap) -> bool {
    headers.contains_key("range")
}

#[cfg(test)]
mod tests {
    use super::*;
    use axum::http::HeaderValue;

    #[test]
    fn test_parse_range_header() {
        let mut headers = HeaderMap::new();
        
        // 测试 bytes=0-499
        headers.insert("range", HeaderValue::from_static("bytes=0-499"));
        let range = parse_range_header(&headers, 1000).unwrap();
        assert_eq!(range.start, 0);
        assert_eq!(range.end, 499);
        assert_eq!(range.content_length(), 500);
        
        // 测试 bytes=500-
        headers.insert("range", HeaderValue::from_static("bytes=500-"));
        let range = parse_range_header(&headers, 1000).unwrap();
        assert_eq!(range.start, 500);
        assert_eq!(range.end, 999);
        
        // 测试 bytes=-500
        headers.insert("range", HeaderValue::from_static("bytes=-500"));
        let range = parse_range_header(&headers, 1000).unwrap();
        assert_eq!(range.start, 500);
        assert_eq!(range.end, 999);
    }
}
