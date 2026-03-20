// 静态文件处理器 - 处理 HTTP 请求并返回静态文件

use crate::server::mime::detect_mime_type;
use crate::server::range::{is_range_request, parse_range_header};
use axum::{
    body::Body,
    extract::Request,
    http::{header, HeaderMap, StatusCode},
    response::Response,
};
use std::path::{Path, PathBuf};
use tokio::fs::File;
use tokio::io::{AsyncReadExt, AsyncSeekExt};

/// 静态文件处理器
pub async fn handle_static_file(
    root_dir: PathBuf,
    request: Request,
) -> Result<Response, StatusCode> {
    let uri_path = request.uri().path();
    
    // 解码 URL 编码的路径（处理中文文件名和空格）
    let decoded_path = urlencoding::decode(uri_path)
        .map_err(|_| StatusCode::BAD_REQUEST)?
        .to_string();
    
    // 移除前导斜杠
    let relative_path = decoded_path.trim_start_matches('/');
    
    // 构造完整文件路径
    let file_path = root_dir.join(relative_path);
    
    // 安全检查：防止目录遍历攻击
    let canonical_root = root_dir
        .canonicalize()
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    let canonical_file = file_path
        .canonicalize()
        .map_err(|_| StatusCode::NOT_FOUND)?;
    
    if !canonical_file.starts_with(&canonical_root) {
        return Err(StatusCode::FORBIDDEN);
    }
    
    // 检查文件是否存在
    if !canonical_file.exists() {
        return Err(StatusCode::NOT_FOUND);
    }
    
    // 如果是目录，尝试返回 index.html
    let file_to_serve = if canonical_file.is_dir() {
        let index_path = canonical_file.join("index.html");
        if index_path.exists() {
            index_path
        } else {
            return Err(StatusCode::FORBIDDEN);
        }
    } else {
        canonical_file
    };
    
    // 获取文件元数据
    let metadata = tokio::fs::metadata(&file_to_serve)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    let file_size = metadata.len();
    
    // 检测 MIME 类型
    let mime_type = detect_mime_type(&file_to_serve);
    
    // 检查是否为 Range 请求
    let headers = request.headers();
    if is_range_request(headers) {
        handle_range_request(&file_to_serve, headers, file_size, &mime_type).await
    } else {
        handle_full_request(&file_to_serve, file_size, &mime_type).await
    }
}

/// 处理完整文件请求
async fn handle_full_request(
    file_path: &Path,
    file_size: u64,
    mime_type: &str,
) -> Result<Response, StatusCode> {
    let file = File::open(file_path)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    let stream = tokio_util::io::ReaderStream::new(file);
    let body = Body::from_stream(stream);
    
    Ok(Response::builder()
        .status(StatusCode::OK)
        .header(header::CONTENT_TYPE, mime_type)
        .header(header::CONTENT_LENGTH, file_size)
        .header(header::ACCEPT_RANGES, "bytes")
        .body(body)
        .unwrap())
}

/// 处理 Range 请求（支持视频拖拽播放）
async fn handle_range_request(
    file_path: &Path,
    headers: &HeaderMap,
    file_size: u64,
    mime_type: &str,
) -> Result<Response, StatusCode> {
    // 解析 Range 头
    let range_info = parse_range_header(headers, file_size)
        .ok_or(StatusCode::RANGE_NOT_SATISFIABLE)?;
    
    // 打开文件
    let mut file = File::open(file_path)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    // 定位到起始位置
    file.seek(std::io::SeekFrom::Start(range_info.start))
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    // 读取指定范围的数据
    let content_length = range_info.content_length();
    let mut buffer = vec![0u8; content_length as usize];
    file.read_exact(&mut buffer)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    // 构造 206 Partial Content 响应
    Ok(Response::builder()
        .status(StatusCode::PARTIAL_CONTENT)
        .header(header::CONTENT_TYPE, mime_type)
        .header(header::CONTENT_LENGTH, content_length)
        .header(header::CONTENT_RANGE, range_info.content_range_header())
        .header(header::ACCEPT_RANGES, "bytes")
        .body(Body::from(buffer))
        .unwrap())
}
