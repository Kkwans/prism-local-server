//! 执行目录迁移示例程序
//! 
//! 使用 DirectoryMigrator 模块执行 src/ → frontend/, src-tauri/ → backend/ 的重命名操作

use std::env;
use std::path::{Path, PathBuf};

// 引入迁移模块（需要在 main.rs 或 lib.rs 中声明）
// 这里假设项目结构中已经包含了 migration 模块

fn main() {
    // 获取项目根目录（向上两级：examples/ → src-tauri/ → project_root/）
    let current_exe = env::current_exe().expect("无法获取当前可执行文件路径");
    let project_root = current_exe
        .parent() // target/debug/examples/
        .and_then(|p| p.parent()) // target/debug/
        .and_then(|p| p.parent()) // target/
        .and_then(|p| p.parent()) // src-tauri/
        .and_then(|p| p.parent()) // project_root/
        .expect("无法确定项目根目录");

    println!("项目根目录: {}", project_root.display());
    println!("\n=== 开始执行目录迁移 ===\n");

    // 注意：由于这是一个示例程序，实际的 DirectoryMigrator 需要从主项目导入
    // 这里我们直接使用文件系统操作来演示迁移过程
    
    execute_migration(project_root);
}

fn execute_migration(project_root: &Path) {
    use std::fs;
    use std::io::{Read, Write};

    // 目录映射
    let mappings = vec![
        ("src", "frontend"),
        ("src-tauri", "backend"),
    ];

    // 配置文件列表
    let config_files = vec![
        "package.json",
        "vite.config.ts",
        "tauri.conf.json",
        ".gitignore",
        "README.md",
    ];

    // 步骤 1: 重命名目录
    println!("步骤 1: 重命名目录");
    for (old_name, new_name) in &mappings {
        let old_path = project_root.join(old_name);
        let new_path = project_root.join(new_name);

        if !old_path.exists() {
            println!("  ⚠ 源目录不存在: {}", old_name);
            continue;
        }

        if new_path.exists() {
            println!("  ⚠ 目标目录已存在: {}", new_name);
            continue;
        }

        match fs::rename(&old_path, &new_path) {
            Ok(_) => println!("  ✓ 已重命名: {} → {}", old_name, new_name),
            Err(e) => println!("  ✗ 重命名失败: {} → {} (错误: {})", old_name, new_name, e),
        }
    }

    // 步骤 2: 更新配置文件
    println!("\n步骤 2: 更新配置文件");
    for config_file in &config_files {
        let file_path = project_root.join(config_file);

        if !file_path.exists() {
            println!("  - {} (文件不存在，跳过)", config_file);
            continue;
        }

        // 读取文件内容
        let mut content = String::new();
        if let Ok(mut file) = fs::File::open(&file_path) {
            if file.read_to_string(&mut content).is_err() {
                println!("  ✗ 读取失败: {}", config_file);
                continue;
            }
        } else {
            println!("  ✗ 打开失败: {}", config_file);
            continue;
        }

        // 替换路径引用
        let mut updated_content = content.clone();
        updated_content = updated_content.replace("src/", "frontend/");
        updated_content = updated_content.replace("src-tauri/", "backend/");

        // 如果内容有变化，写回文件
        if updated_content != content {
            if let Ok(mut file) = fs::File::create(&file_path) {
                if file.write_all(updated_content.as_bytes()).is_ok() {
                    println!("  ✓ 已更新: {}", config_file);
                } else {
                    println!("  ✗ 写入失败: {}", config_file);
                }
            } else {
                println!("  ✗ 创建失败: {}", config_file);
            }
        } else {
            println!("  - {} (无需更新)", config_file);
        }
    }

    // 步骤 3: 验证迁移
    println!("\n步骤 3: 验证迁移");
    let mut all_checks_passed = true;

    // 检查新目录是否存在
    println!("  检查新目录:");
    for (_, new_name) in &mappings {
        let new_path = project_root.join(new_name);
        if new_path.exists() {
            println!("    ✓ {} 存在", new_name);
        } else {
            println!("    ✗ {} 不存在", new_name);
            all_checks_passed = false;
        }
    }

    // 检查旧目录是否已删除
    println!("  检查旧目录:");
    for (old_name, _) in &mappings {
        let old_path = project_root.join(old_name);
        if !old_path.exists() {
            println!("    ✓ {} 已删除", old_name);
        } else {
            println!("    ✗ {} 仍然存在", old_name);
            all_checks_passed = false;
        }
    }

    // 检查配置文件中的路径引用
    println!("  检查配置文件:");
    for config_file in &config_files {
        let file_path = project_root.join(config_file);

        if !file_path.exists() {
            continue;
        }

        if let Ok(content) = fs::read_to_string(&file_path) {
            let has_old_paths = content.contains("src/") || content.contains("src-tauri/");
            if !has_old_paths {
                println!("    ✓ {} 无旧路径引用", config_file);
            } else {
                println!("    ✗ {} 仍包含旧路径引用", config_file);
                all_checks_passed = false;
            }
        }
    }

    println!("\n=== 迁移完成 ===");
    if all_checks_passed {
        println!("✓ 所有检查通过，迁移成功！");
    } else {
        println!("✗ 部分检查失败，请手动修复问题");
    }
}
