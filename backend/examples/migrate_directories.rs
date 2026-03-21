/// 目录迁移示例程序
/// 
/// 演示如何使用 DirectoryMigrator 执行目录重命名操作
/// 
/// 运行方式：
/// ```
/// cargo run --example migrate_directories
/// ```

use app_lib::migration::DirectoryMigrator;
use std::env;

fn main() {
    println!("=== Prism Local Server 目录迁移工具 ===\n");

    // 获取项目根目录（当前工作目录的父目录）
    let current_dir = env::current_dir().expect("无法获取当前目录");
    let project_root = current_dir.parent().expect("无法获取项目根目录");

    println!("项目根目录: {}\n", project_root.display());

    // 创建迁移器实例
    let migrator = DirectoryMigrator::new(project_root);

    // 执行完整迁移流程
    match migrator.migrate() {
        Ok(()) => {
            println!("\n✓ 迁移成功完成！");
            println!("\n后续步骤：");
            println!("1. 运行 'npm run build' 验证前端构建");
            println!("2. 运行 'cargo build' 验证后端编译");
            println!("3. 运行 'cargo tauri dev' 验证应用启动");
        }
        Err(e) => {
            eprintln!("\n✗ 迁移失败: {}", e);
            std::process::exit(1);
        }
    }
}
