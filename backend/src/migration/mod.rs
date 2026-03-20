//! 目录迁移模块
//! 
//! 负责执行项目目录重命名操作（src/ → frontend/, src-tauri/ → backend/）
//! 并更新所有配置文件中的路径引用

use std::path::{Path, PathBuf};
use std::fs;
use std::io::{Read, Write};
use crate::errors::AppError;

/// 目录重命名迁移器
/// 
/// 执行目录重命名操作并更新配置文件中的路径引用
pub struct DirectoryMigrator {
    /// 项目根目录
    project_root: PathBuf,
}

/// 目录重命名映射
const DIRECTORY_MAPPINGS: &[(&str, &str)] = &[
    ("src/", "frontend/"),
    ("src-tauri/", "backend/"),
];

/// 需要更新的配置文件列表
const CONFIG_FILES: &[&str] = &[
    "package.json",
    "vite.config.ts",
    "tauri.conf.json",
    ".gitignore",
    "README.md",
];

impl DirectoryMigrator {
    /// 创建新的目录迁移器实例
    /// 
    /// # 参数
    /// 
    /// * `project_root` - 项目根目录路径
    pub fn new<P: AsRef<Path>>(project_root: P) -> Self {
        Self {
            project_root: project_root.as_ref().to_path_buf(),
        }
    }

    /// 执行目录重命名操作
    /// 
    /// 将 src/ 重命名为 frontend/，将 src-tauri/ 重命名为 backend/
    /// 
    /// # 返回值
    /// 
    /// * `Ok(())` - 重命名成功
    /// * `Err(AppError)` - 重命名失败
    /// 
    /// # 错误
    /// 
    /// * `AppError::DirectoryNotFound` - 源目录不存在
    /// * `AppError::Io` - 文件系统操作失败
    pub fn rename_directories(&self) -> Result<(), AppError> {
        for (old_name, new_name) in DIRECTORY_MAPPINGS {
            let old_path = self.project_root.join(old_name.trim_end_matches('/'));
            let new_path = self.project_root.join(new_name.trim_end_matches('/'));

            // 检查源目录是否存在
            if !old_path.exists() {
                return Err(AppError::DirectoryNotFound(
                    old_path.to_string_lossy().to_string()
                ));
            }

            // 检查目标目录是否已存在
            if new_path.exists() {
                return Err(AppError::DirectoryAlreadyExists(
                    new_path.to_string_lossy().to_string()
                ));
            }

            // 执行重命名
            fs::rename(&old_path, &new_path)
                .map_err(AppError::Io)?;

            println!("✓ 已重命名: {} → {}", old_name, new_name);
        }

        Ok(())
    }

    /// 批量更新配置文件中的路径引用
    /// 
    /// 将所有配置文件中的旧路径（src/, src-tauri/）替换为新路径（frontend/, backend/）
    /// 
    /// # 返回值
    /// 
    /// * `Ok(())` - 更新成功
    /// * `Err(AppError)` - 更新失败
    /// 
    /// # 错误
    /// 
    /// * `AppError::ConfigNotFound` - 配置文件不存在
    /// * `AppError::Io` - 文件读写失败
    pub fn update_config_files(&self) -> Result<(), AppError> {
        for config_file in CONFIG_FILES {
            let file_path = self.project_root.join(config_file);

            // 检查文件是否存在
            if !file_path.exists() {
                println!("⚠ 跳过不存在的文件: {}", config_file);
                continue;
            }

            // 读取文件内容
            let mut content = String::new();
            let mut file = fs::File::open(&file_path)
                .map_err(AppError::Io)?;
            file.read_to_string(&mut content)
                .map_err(AppError::Io)?;

            // 替换所有路径引用
            let mut updated_content = content.clone();
            for (old_path, new_path) in DIRECTORY_MAPPINGS {
                updated_content = updated_content.replace(old_path, new_path);
            }

            // 如果内容有变化，写回文件
            if updated_content != content {
                let mut file = fs::File::create(&file_path)
                    .map_err(AppError::Io)?;
                file.write_all(updated_content.as_bytes())
                    .map_err(AppError::Io)?;

                println!("✓ 已更新配置文件: {}", config_file);
            } else {
                println!("  配置文件无需更新: {}", config_file);
            }
        }

        Ok(())
    }

    /// 验证重命名操作的完整性
    /// 
    /// 检查：
    /// 1. 新目录是否存在
    /// 2. 旧目录是否已删除
    /// 3. 配置文件中是否还残留旧路径引用
    /// 
    /// # 返回值
    /// 
    /// * `Ok(true)` - 验证通过
    /// * `Ok(false)` - 验证失败
    /// * `Err(AppError)` - 验证过程出错
    pub fn verify_migration(&self) -> Result<bool, AppError> {
        let mut all_checks_passed = true;

        println!("\n=== 开始验证迁移完整性 ===\n");

        // 1. 检查新目录是否存在
        println!("1. 检查新目录是否存在:");
        for (_, new_name) in DIRECTORY_MAPPINGS {
            let new_path = self.project_root.join(new_name.trim_end_matches('/'));
            if new_path.exists() {
                println!("  ✓ {} 存在", new_name);
            } else {
                println!("  ✗ {} 不存在", new_name);
                all_checks_passed = false;
            }
        }

        // 2. 检查旧目录是否已删除
        println!("\n2. 检查旧目录是否已删除:");
        for (old_name, _) in DIRECTORY_MAPPINGS {
            let old_path = self.project_root.join(old_name.trim_end_matches('/'));
            if !old_path.exists() {
                println!("  ✓ {} 已删除", old_name);
            } else {
                println!("  ✗ {} 仍然存在", old_name);
                all_checks_passed = false;
            }
        }

        // 3. 检查配置文件中是否还残留旧路径引用
        println!("\n3. 检查配置文件中的路径引用:");
        for config_file in CONFIG_FILES {
            let file_path = self.project_root.join(config_file);

            if !file_path.exists() {
                println!("  - {} (文件不存在，跳过)", config_file);
                continue;
            }

            let mut content = String::new();
            let mut file = fs::File::open(&file_path)
                .map_err(AppError::Io)?;
            file.read_to_string(&mut content)
                .map_err(AppError::Io)?;

            let mut has_old_paths = false;
            for (old_path, _) in DIRECTORY_MAPPINGS {
                if content.contains(old_path) {
                    println!("  ✗ {} 仍包含旧路径: {}", config_file, old_path);
                    has_old_paths = true;
                    all_checks_passed = false;
                }
            }

            if !has_old_paths {
                println!("  ✓ {} 无旧路径引用", config_file);
            }
        }

        println!("\n=== 验证完成 ===");
        if all_checks_passed {
            println!("✓ 所有检查通过，迁移成功！");
        } else {
            println!("✗ 部分检查失败，请手动修复问题");
        }

        Ok(all_checks_passed)
    }

    /// 执行完整的迁移流程
    /// 
    /// 包括：
    /// 1. 重命名目录
    /// 2. 更新配置文件
    /// 3. 验证迁移完整性
    /// 
    /// # 返回值
    /// 
    /// * `Ok(())` - 迁移成功
    /// * `Err(AppError)` - 迁移失败
    pub fn migrate(&self) -> Result<(), AppError> {
        println!("=== 开始目录迁移 ===\n");

        // 步骤 1: 重命名目录
        println!("步骤 1: 重命名目录");
        self.rename_directories()?;

        // 步骤 2: 更新配置文件
        println!("\n步骤 2: 更新配置文件");
        self.update_config_files()?;

        // 步骤 3: 验证迁移
        println!("\n步骤 3: 验证迁移");
        let verification_passed = self.verify_migration()?;

        if !verification_passed {
            return Err(AppError::MigrationVerificationFailed);
        }

        println!("\n=== 迁移完成 ===");
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    /// 创建测试用的项目结构
    fn create_test_project() -> TempDir {
        let temp_dir = TempDir::new().unwrap();
        let root = temp_dir.path();

        // 创建 src/ 和 src-tauri/ 目录
        fs::create_dir(root.join("src")).unwrap();
        fs::create_dir(root.join("src-tauri")).unwrap();

        // 创建测试配置文件
        fs::write(
            root.join("package.json"),
            r#"{"scripts": {"dev": "vite", "build": "vite build"}}"#
        ).unwrap();

        fs::write(
            root.join("vite.config.ts"),
            r#"export default { root: "src/" }"#
        ).unwrap();

        fs::write(
            root.join(".gitignore"),
            "src-tauri/target/\nnode_modules/"
        ).unwrap();

        temp_dir
    }

    #[test]
    fn test_rename_directories() {
        let temp_dir = create_test_project();
        let migrator = DirectoryMigrator::new(temp_dir.path());

        // 执行重命名
        migrator.rename_directories().unwrap();

        // 验证新目录存在
        assert!(temp_dir.path().join("frontend").exists());
        assert!(temp_dir.path().join("backend").exists());

        // 验证旧目录不存在
        assert!(!temp_dir.path().join("src").exists());
        assert!(!temp_dir.path().join("src-tauri").exists());
    }

    #[test]
    fn test_update_config_files() {
        let temp_dir = create_test_project();
        let migrator = DirectoryMigrator::new(temp_dir.path());

        // 先重命名目录
        migrator.rename_directories().unwrap();

        // 更新配置文件
        migrator.update_config_files().unwrap();

        // 验证配置文件已更新
        let vite_config = fs::read_to_string(temp_dir.path().join("vite.config.ts")).unwrap();
        assert!(vite_config.contains("frontend/"));
        assert!(!vite_config.contains("src/"));

        let gitignore = fs::read_to_string(temp_dir.path().join(".gitignore")).unwrap();
        assert!(gitignore.contains("backend/target/"));
        assert!(!gitignore.contains("src-tauri/target/"));
    }

    #[test]
    fn test_verify_migration() {
        let temp_dir = create_test_project();
        let migrator = DirectoryMigrator::new(temp_dir.path());

        // 执行完整迁移
        migrator.rename_directories().unwrap();
        migrator.update_config_files().unwrap();

        // 验证迁移
        let result = migrator.verify_migration().unwrap();
        assert!(result, "迁移验证应该通过");
    }

    #[test]
    fn test_full_migration() {
        let temp_dir = create_test_project();
        let migrator = DirectoryMigrator::new(temp_dir.path());

        // 执行完整迁移
        migrator.migrate().unwrap();

        // 验证结果
        assert!(temp_dir.path().join("frontend").exists());
        assert!(temp_dir.path().join("backend").exists());
        assert!(!temp_dir.path().join("src").exists());
        assert!(!temp_dir.path().join("src-tauri").exists());
    }
}
