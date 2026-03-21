// MIME 类型检测器 - 根据文件扩展名返回正确的 MIME 类型

use std::path::Path;

/// 根据文件扩展名检测 MIME 类型
pub fn detect_mime_type(path: &Path) -> String {
    let extension = path
        .extension()
        .and_then(|ext| ext.to_str())
        .unwrap_or("");

    match extension.to_lowercase().as_str() {
        // HTML 和 XML
        "html" | "htm" => "text/html; charset=utf-8",
        "xml" => "application/xml; charset=utf-8",
        
        // 样式表
        "css" => "text/css; charset=utf-8",
        
        // JavaScript
        "js" | "mjs" => "application/javascript; charset=utf-8",
        "json" => "application/json; charset=utf-8",
        
        // 图片
        "png" => "image/png",
        "jpg" | "jpeg" => "image/jpeg",
        "gif" => "image/gif",
        "svg" => "image/svg+xml",
        "webp" => "image/webp",
        "ico" => "image/x-icon",
        "bmp" => "image/bmp",
        
        // 视频
        "mp4" => "video/mp4",
        "webm" => "video/webm",
        "ogg" => "video/ogg",
        "mov" => "video/quicktime",
        "avi" => "video/x-msvideo",
        
        // 音频
        "mp3" => "audio/mpeg",
        "wav" => "audio/wav",
        "m4a" => "audio/mp4",
        
        // 字体
        "woff" => "font/woff",
        "woff2" => "font/woff2",
        "ttf" => "font/ttf",
        "otf" => "font/otf",
        
        // 文档
        "pdf" => "application/pdf",
        "txt" => "text/plain; charset=utf-8",
        
        // 默认
        _ => "application/octet-stream",
    }
    .to_string()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::PathBuf;

    #[test]
    fn test_detect_mime_type() {
        assert_eq!(detect_mime_type(&PathBuf::from("test.html")), "text/html; charset=utf-8");
        assert_eq!(detect_mime_type(&PathBuf::from("test.css")), "text/css; charset=utf-8");
        assert_eq!(detect_mime_type(&PathBuf::from("test.js")), "application/javascript; charset=utf-8");
        assert_eq!(detect_mime_type(&PathBuf::from("test.png")), "image/png");
        assert_eq!(detect_mime_type(&PathBuf::from("test.mp4")), "video/mp4");
        assert_eq!(detect_mime_type(&PathBuf::from("test.MP4")), "video/mp4"); // 大写扩展名
        assert_eq!(detect_mime_type(&PathBuf::from("test.unknown")), "application/octet-stream");
    }
}
