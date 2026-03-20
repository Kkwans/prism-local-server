# 目录迁移状态

## 迁移进度

### ✅ 已完成

1. **目录创建**
   - ✅ `frontend/` 目录已创建（从 `src/` 重命名）
   - ✅ `backend/` 目录已创建（从 `src-tauri/` 复制）

2. **配置文件更新**
   - ✅ `package.json` - 路径引用已更新
   - ✅ `vite.config.ts` - 路径引用已更新
   - ✅ `.gitignore` - 路径引用已更新
   - ✅ `README.md` - 路径引用已更新
   - ✅ `BUILD_GUIDE.md` - 路径引用已更新
   - ✅ `GITHUB_RELEASE_GUIDE.md` - 路径引用已更新
   - ✅ `scripts/post-build.ps1` - 路径引用已更新

3. **旧目录清理**
   - ✅ `src/` 目录已删除

### ⚠️ 待处理

1. **src-tauri 目录删除**
   - ⚠️ `src-tauri/` 目录仍然存在（文件被占用）
   - 原因：Windows 文件锁（可能是 IDE、文件管理器或系统服务正在访问）

## 如何完成迁移

### 方法 1：使用清理脚本（推荐）

1. 关闭所有可能访问 `src-tauri/` 目录的程序：
   - VS Code 或其他 IDE
   - 文件资源管理器
   - 终端窗口
   - Cargo 进程

2. 等待 5-10 秒让文件锁释放

3. 运行清理脚本：

   **PowerShell**:
   ```powershell
   .\cleanup-old-dirs.ps1
   ```

   **CMD**:
   ```cmd
   cleanup-old-dirs.bat
   ```

### 方法 2：手动删除

如果脚本仍然失败，可以手动删除：

1. 重启计算机（这会释放所有文件锁）
2. 重启后，直接删除 `src-tauri/` 目录：
   ```powershell
   Remove-Item -Path "src-tauri" -Recurse -Force
   ```

### 方法 3：使用 Git 清理

如果你使用 Git 管理项目：

```powershell
# 从 Git 索引中删除
git rm -rf src-tauri

# 提交更改
git commit -m "[chore] 删除旧的 src-tauri 目录"
```

## 验证迁移完成

运行以下命令验证迁移是否完全完成：

```powershell
# 检查目录结构
Get-ChildItem -Directory | Select-Object Name

# 应该看到：
# - frontend/
# - backend/
# - 不应该看到 src/ 或 src-tauri/
```

## 迁移后的项目结构

```
prism-local-server-tauri/
├── frontend/              # 前端源代码（原 src/）
│   ├── components/
│   ├── stores/
│   ├── App.tsx
│   └── main.tsx
├── backend/               # 后端源代码（原 src-tauri/）
│   ├── src/
│   │   ├── commands/
│   │   ├── server/
│   │   ├── config/
│   │   └── main.rs
│   ├── Cargo.toml
│   └── tauri.conf.json
├── scripts/               # 构建脚本
├── package.json
├── vite.config.ts
└── README.md
```

## 注意事项

1. **backend 目录是 src-tauri 的完整副本**，包含所有文件和构建缓存
2. **删除 src-tauri 不会影响功能**，因为所有代码已复制到 backend
3. **配置文件已全部更新**，指向新的目录结构
4. **可以安全删除 src-tauri**，不会丢失任何数据

## 下一步

完成 src-tauri 目录删除后，继续执行任务 2.4：

```powershell
# 验证前端构建
npm run build

# 验证后端编译
cd backend
cargo build

# 验证应用启动
cd ..
npm run tauri dev
```

---

**创建时间**: 2026-03-20  
**状态**: 迁移 95% 完成，仅剩 src-tauri 目录清理
