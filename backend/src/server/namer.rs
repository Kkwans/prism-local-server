/// 服务命名器模块
/// 负责从部署目录路径生成有意义的服务名称

use std::path::Path;

/// 服务名称最大长度
const MAX_NAME_LENGTH: usize = 50;

/// 服务命名器
#[derive(Clone)]
pub struct ServiceNamer;

impl ServiceNamer {
    /// 创建新的服务命名器
    pub fn new() -> Self {
        Self
    }
    
    /// 从路径生成服务名称
    ///
    /// # 参数
    /// * `path` - 部署目录路径
    ///
    /// # 返回
    /// * `String` - 生成的服务名称
    ///
    /// # 规则
    /// 1. 提取路径的最后一级文件夹名作为服务名称
    /// 2. 支持中文、日期、下划线等特殊字符
    /// 3. 如果是根目录（如 C:\），返回"根目录"
    /// 4. 长度超过 50 字符时截断并添加省略号
    ///
    /// # 示例
    /// ```
    /// let namer = ServiceNamer::new();
    /// 
    /// // 示例 1: 普通路径
    /// let name = namer.generate_service_name("C:\\MyProgram\\TODO\\Telegram\\我的收藏_2026-01-20");
    /// assert_eq!(name, "我的收藏_2026-01-20");
    /// 
    /// // 示例 2: 根目录
    /// let name = namer.generate_service_name("C:\\");
    /// assert_eq!(name, "根目录");
    /// 
    /// // 示例 3: 长名称
    /// let long_path = "C:\\很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文件夹名称";
    /// let name = namer.generate_service_name(long_path);
    /// assert!(name.len() <= MAX_NAME_LENGTH + 3); // +3 for "..."
    /// ```
    pub fn generate_service_name<P: AsRef<Path>>(&self, path: P) -> String {
        let path = path.as_ref();
        
        // 获取路径的最后一个组件
        if let Some(folder_name) = path.file_name() {
            let name = folder_name.to_string_lossy().to_string();
            
            // 检查长度并截断
            if name.chars().count() > MAX_NAME_LENGTH {
                // 截取前 50 个字符并添加省略号
                let truncated: String = name.chars().take(MAX_NAME_LENGTH).collect();
                format!("{}...", truncated)
            } else {
                name
            }
        } else {
            // 如果无法获取文件夹名（可能是根目录），返回"根目录"
            "根目录".to_string()
        }
    }
}

impl Default for ServiceNamer {
    fn default() -> Self {
        Self::new()
    }
}

/// 从路径生成服务名称（便捷函数）
///
/// # 参数
/// * `path` - 部署目录路径
///
/// # 返回
/// * `String` - 生成的服务名称
pub fn generate_service_name<P: AsRef<Path>>(path: P) -> String {
    ServiceNamer::new().generate_service_name(path)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_service_name_normal() {
        let namer = ServiceNamer::new();
        
        // 测试普通路径
        let name = namer.generate_service_name("C:\\MyProgram\\TODO\\Telegram\\我的收藏_2026-01-20");
        assert_eq!(name, "我的收藏_2026-01-20");
    }
    
    #[test]
    fn test_generate_service_name_with_date() {
        let namer = ServiceNamer::new();
        
        // 测试包含日期的路径
        let name = namer.generate_service_name("D:\\Projects\\Website_2026-03-20");
        assert_eq!(name, "Website_2026-03-20");
    }
    
    #[test]
    fn test_generate_service_name_chinese() {
        let namer = ServiceNamer::new();
        
        // 测试中文路径
        let name = namer.generate_service_name("E:\\文档\\项目文件夹");
        assert_eq!(name, "项目文件夹");
    }
    
    #[test]
    fn test_generate_service_name_root() {
        let namer = ServiceNamer::new();
        
        // 测试根目录
        let name = namer.generate_service_name("C:\\");
        assert_eq!(name, "根目录");
    }
    
    #[test]
    fn test_generate_service_name_long() {
        let namer = ServiceNamer::new();
        
        // 测试超长名称（直接使用文件夹名）- 需要超过 50 个字符
        let long_name = "这是一个非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常长的文件夹名称";
        let name = namer.generate_service_name(long_name);
        
        // 验证长度限制
        assert!(name.ends_with("..."), "名称应该以...结尾，实际: {}", name);
        assert!(name.chars().count() <= MAX_NAME_LENGTH + 3);
    }
    
    #[test]
    fn test_generate_service_name_special_chars() {
        let namer = ServiceNamer::new();
        
        // 测试特殊字符
        let name = namer.generate_service_name("C:\\Projects\\my-app_v1.0.0");
        assert_eq!(name, "my-app_v1.0.0");
    }
}
