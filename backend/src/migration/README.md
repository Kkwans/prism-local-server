# 目录迁移模块 (DirectoryMigrator)

## 概述

DirectoryMigrator 模块负责执行项目目录重命名操作，将 `src/` 重命名为 `frontend/`，将 `src-tauri/` 重命名为 `backend/`，并自动更新所有配置文件中的路径引用。

## 功能特性

- ✅ 自动重命名目录（src/ → frontend/, src-tauri/ → backend/）
- ✅ 批量更新配置文件中的路径引用
- ✅ 完整性验证（检查新目录存在、旧目录删除、配置文件更新）
- ✅ 详细的日志输出
- ✅ 完善的错误处理

## 使用方法

### 方法 1: 使用示例程序（推荐）

```bash
# 在 src-tauri 目录下运行
cargo run --example migrate_directories
```

### 方法 2: 在代码中使用

```rust
use app_lib::migration::DirectoryMigrator;
use std::path::Path;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 创建迁移器实例
    let project_root = Path::new("path/to/project");
    let migrator = DirectoryMigrator::new(project_root);

    // 执行完整迁移流程
    migrator.migrate()?;

    Ok(())
}
```

### 方法 3: 分步执行

```rust
use app_lib::migration::DirectoryMigrator;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let migrator = DirectoryMigrator::new(".");

    // 步骤 1: 重命名目录
    migrator.rename_directories()?;

    // 步骤 2: 更新配置文件
    migrator.update_config_files()?;

    // 步骤 3: 验证迁移
    let verification_passed = migrator.verify_migration()?;
    
    if !verification_passed {
        eprintln!("验证失败，请检查错误信息");
    }

    Ok(())
}
```

## 迁移流程

```
1. 重命名目录
   ├── src/ → frontend/
   └── src-tauri/ → backend/

2. 更新配置文件
   ├── package.json
   ├── vite.config.ts
   ├── tauri.conf.json
   ├── .gitignore
   └── README.md

3. 验证迁移
   ├── 检查新目录存在
   ├── 检查旧目录删除
   └── 检查配置文件无旧路径引用
```

## 错误处理

模块使用 `AppError` 枚举处理所有错误情况：

- `DirectoryNotFound` - 源目录不存在
- `DirectoryAlreadyExists` - 目标目录已存在
- `ConfigNotFound` - 配置文件不存在
- `MigrationVerificationFailed` - 迁移验证失败
- `Io` - 文件系统操作失败

## 测试

运行单元测试：

```bash
cargo test --lib migration
```

测试覆盖：
- ✅ 目录重命名功能
- ✅ 配置文件更新功能
- ✅ 迁移验证功能
- ✅ 完整迁移流程

## 注意事项

1. **备份数据**：执行迁移前建议备份项目
2. **Git 状态**：确保工作区干净（无未提交更改）
3. **权限检查**：确保有足够的文件系统权限
4. **路径验证**：迁移后需要验证所有路径引用是否正确

## 迁移后验证步骤

```bash
# 1. 验证前端构建
npm run build

# 2. 验证后端编译
cargo build

# 3. 验证应用启动
cargo tauri dev
```

## 相关需求

- 需求 4.1: 将 src/ 目录重命名为 frontend/
- 需求 4.2: 将 src-tauri/ 目录重命名为 backend/
- 需求 4.3-4.7: 更新所有配置文件中的路径引用
- 需求 4.8: 验证重命名后应用能正常启动和构建

## 技术实现

- **语言**: Rust
- **命名规范**: snake_case
- **错误处理**: Result<T, AppError>
- **测试框架**: Rust 内置测试 + tempfile
- **文档注释**: 中文
