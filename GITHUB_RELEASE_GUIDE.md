# GitHub Release 发布指南

## 📋 前置条件

✅ 已完成的操作：
- [x] tauri-v3 分支已合并到 main 分支
- [x] 已创建 Git Tag: v3.0.0
- [x] 已推送 main 分支和 v3.0.0 标签到远程仓库

✅ 构建产物已准备：
- [x] `prism-local-server-v3.0.0.exe` (4.72 MB) - 根目录
- [x] `Prism Local Server_3.0.0_x64_en-US.msi` (2.43 MB) - src-tauri/target/release/bundle/msi/
- [x] `Prism Local Server_3.0.0_x64-setup.exe` (1.74 MB) - src-tauri/target/release/bundle/nsis/

---

## 🚀 创建 GitHub Release 步骤

### 1. 访问 GitHub Releases 页面

打开浏览器，访问：
```
https://github.com/Kkwans/prism-local-server/releases/new
```

或者：
1. 进入项目主页：https://github.com/Kkwans/prism-local-server
2. 点击右侧的 "Releases"
3. 点击 "Draft a new release" 按钮

---

### 2. 填写 Release 信息

#### 选择标签
- **Tag version**: 选择 `v3.0.0`（已存在的标签）
- **Target**: `main` 分支

#### 填写标题
```
v3.0.0 - Tauri v2 完整重写版本
```

#### 填写描述
将 `RELEASE_v3.0.0.md` 文件的内容复制粘贴到描述框中。

**快速复制命令**（在项目根目录执行）：
```powershell
Get-Content RELEASE_v3.0.0.md | Set-Clipboard
```

---

### 3. 上传构建产物

点击 "Attach binaries by dropping them here or selecting them" 区域，上传以下文件：

#### 文件 1：便携版 EXE
- **路径**: `prism-local-server-tauri/prism-local-server-v3.0.0.exe`
- **大小**: 4.72 MB
- **说明**: 无需安装，双击即用

#### 文件 2：MSI 安装包
- **路径**: `prism-local-server-tauri/src-tauri/target/release/bundle/msi/Prism Local Server_3.0.0_x64_en-US.msi`
- **大小**: 2.43 MB
- **说明**: Windows Installer 标准安装包

#### 文件 3：NSIS 安装包
- **路径**: `prism-local-server-tauri/src-tauri/target/release/bundle/nsis/Prism Local Server_3.0.0_x64-setup.exe`
- **大小**: 1.74 MB
- **说明**: 自定义安装向导

---

### 4. 发布设置

- ✅ **Set as the latest release**: 勾选（设为最新版本）
- ⬜ **Set as a pre-release**: 不勾选（这是正式版本）
- ⬜ **Create a discussion for this release**: 可选（如需讨论区可勾选）

---

### 5. 发布

点击 **"Publish release"** 按钮完成发布。

---

## 📦 发布后验证

### 验证清单

1. **Release 页面显示正常**
   - 访问：https://github.com/Kkwans/prism-local-server/releases/tag/v3.0.0
   - 确认标题、描述、文件都正确显示

2. **下载链接可用**
   - 测试下载每个构建产物
   - 确认文件大小和名称正确

3. **Latest Release 标签**
   - 项目主页右侧应显示 "Latest" 标签指向 v3.0.0

4. **Tag 链接正常**
   - 点击 Tag 应跳转到对应的 commit

---

## 🔄 后续操作

### 切换回开发分支

发布完成后，切换回 `tauri-v3` 分支继续开发：

```powershell
cd prism-local-server-tauri
git checkout tauri-v3
```

### 同步 tauri-v3 分支

确保 tauri-v3 分支与 main 分支同步：

```powershell
git merge main
git push origin tauri-v3
```

---

## 📝 Release 说明模板（简化版）

如果需要更简洁的 Release 说明，可以使用以下模板：

```markdown
# Prism Local Server v3.0.0

## 🎉 重大更新：完整 Tauri v2 重写

从 Python/Flet 架构完全迁移到 Tauri v2 (Rust + React)，带来革命性的性能提升。

## ✨ 核心特性

- 🚀 **性能飞跃**：内存占用 ≤ 50MB，启动速度 ≤ 1.5s
- 💎 **Windows 11 Fluent Design UI**：毛玻璃效果、流畅动画
- 🎯 **智能服务管理**：自动命名、端口管理、唯一性约束
- 📦 **完整功能**：Range Requests、MIME 识别、局域网访问

## 📥 下载

| 文件 | 类型 | 大小 |
|------|------|------|
| prism-local-server-v3.0.0.exe | 便携版 | 4.72 MB |
| Prism Local Server_3.0.0_x64_en-US.msi | MSI 安装包 | 2.43 MB |
| Prism Local Server_3.0.0_x64-setup.exe | NSIS 安装包 | 1.74 MB |

## 📋 系统要求

- Windows 11（推荐）或 Windows 10 1809+
- WebView2（Windows 11 自带）

## 📚 文档

- [用户指南](./USER_GUIDE.md)
- [构建指南](./BUILD_GUIDE.md)
- [性能测试报告](./PERFORMANCE_TEST.md)

**发布日期**：2025-01-20
```

---

## ⚠️ 注意事项

1. **文件命名**：确保上传的文件名与构建产物完全一致
2. **文件大小**：GitHub 单个文件限制 2GB，当前文件都在限制内
3. **Release 编辑**：发布后仍可编辑 Release 说明和添加/删除文件
4. **Tag 不可变**：Tag 一旦推送不建议删除或修改

---

## 🆘 常见问题

### Q: 如何删除错误的 Release？
A: 在 Release 页面点击 "Delete" 按钮，但 Tag 仍会保留在仓库中。

### Q: 如何删除错误的 Tag？
A: 
```powershell
# 删除本地 Tag
git tag -d v3.0.0

# 删除远程 Tag
git push origin :refs/tags/v3.0.0
```

### Q: 如何修改 Release 说明？
A: 在 Release 页面点击 "Edit release" 按钮即可修改。

---

**准备完成！现在可以前往 GitHub 创建 Release 了。**
