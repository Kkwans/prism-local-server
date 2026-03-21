# 架构文档：Prism Local Server Tauri

## 概述

Prism Local Server Tauri 是一个基于 **Tauri v2** 框架的 Windows 11 桌面应用程序，采用**前后端分离架构**，使用 Rust 后端处理业务逻辑和系统调用，React 前端负责 UI 渲染和用户交互。

### 核心技术栈

- **后端**: Rust + Tokio (异步运行时) + Axum (HTTP 服务器)
- **前端**: React 19 + TypeScript + Zustand (状态管理) + Tailwind CSS
- **通信层**: Tauri IPC (基于 JSON-RPC)
- **构建工具**: Cargo (Rust) + Vite (前端) + Tauri CLI

---

## 项目目录结构

```
prism-local-server-tauri/
├── src/                          # 前端代码目录 (React/TypeScript)
│   ├── components/               # React 组件
│   │   ├── Dashboard.tsx         # 主仪表盘组件
│   │   ├── ServerCard.tsx        # 服务卡片组件
│   │   ├── SettingsDialog.tsx    # 设置对话框组件
│   │   └── ui/                   # Shadcn/ui 基础组件
│   ├── stores/                   # Zustand 状态管理
│   │   ├── useServerStore.ts     # 服务状态管理
│   │   └── useConfigStore.ts     # 配置状态管理
│   ├── types/                    # TypeScript 类型定义
│   ├── hooks/                    # React 自定义 Hooks
│   ├── lib/                      # 工具函数库
│   ├── App.tsx                   # 根组件
│   ├── main.tsx                  # 前端入口文件
│   └── index.css                 # 全局样式
│
├── src-tauri/                    # 后端代码目录 (Rust)
│   ├── src/
│   │   ├── main.rs               # Rust 入口文件
│   │   ├── commands/             # Tauri Commands (IPC 接口)
│   │   ├── server/               # HTTP 服务器管理模块
│   │   ├── config/               # 配置管理模块
│   │   ├── utils/                # 工具函数模块
│   │   └── git/                  # Git 自动化模块
│   ├── Cargo.toml                # Rust 依赖配置
│   ├── tauri.conf.json           # Tauri 应用配置
│   ├── build.rs                  # 构建脚本
│   └── icons/                    # 应用图标资源
│
├── package.json                  # 前端依赖配置
├── vite.config.ts                # Vite 构建配置
├── tailwind.config.js            # Tailwind CSS 配置
├── tsconfig.json                 # TypeScript 配置
├── README.md                     # 项目说明文档
└── ARCHITECTURE.md               # 本架构文档
```


### 目录职责说明

#### `src/` - 前端目录 (React/TypeScript)

**职责范围**:
- ✅ UI 组件渲染和布局
- ✅ 用户交互事件处理
- ✅ 前端状态管理 (Zustand)
- ✅ 动画和视觉效果 (Framer Motion)
- ✅ 表单验证和输入处理

**禁止操作**:
- ❌ 文件系统 I/O 操作
- ❌ 网络端口操作
- ❌ 系统调用和进程管理
- ❌ 业务逻辑实现

**通信方式**: 通过 Tauri IPC 调用后端 Commands

#### `src-tauri/` - 后端目录 (Rust)

**职责范围**:
- ✅ HTTP 静态文件服务器实现
- ✅ 端口管理和可用性检测
- ✅ 文件系统操作 (读取、验证)
- ✅ 配置文件持久化
- ✅ 多服务实例管理
- ✅ 系统托盘和窗口控制
- ✅ Git 自动化操作

**禁止操作**:
- ❌ UI 渲染逻辑
- ❌ 用户交互处理

**通信方式**: 通过 Tauri Commands 暴露接口给前端

---

## 架构设计

### 分层架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      用户界面层 (UI Layer)                    │
│                    React Components + Tailwind CSS           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Dashboard   │  │  ServerCard  │  │   Settings   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ↕ Props & Events
┌─────────────────────────────────────────────────────────────┐
│                   状态管理层 (State Layer)                    │
│                      Zustand Stores                          │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │   useServerStore     │  │   useConfigStore     │        │
│  └──────────────────────┘  └──────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              ↕ Tauri IPC (invoke)
┌─────────────────────────────────────────────────────────────┐
│                   IPC 通信层 (IPC Layer)                      │
│                      Tauri Commands                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ start_server │  │ stop_server  │  │ load_config  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ↕ Function Calls
┌─────────────────────────────────────────────────────────────┐
│                  业务逻辑层 (Business Layer)                  │
│                      Rust Modules                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ServerManager │  │ ConfigManager│  │  PortManager │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ↕ System Calls
┌─────────────────────────────────────────────────────────────┐
│                  系统资源层 (System Layer)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ File System  │  │ Network Port │  │  Git Repo    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```


### 前后端分离原则

#### 职责边界

| 层级 | 前端 (src/) | 后端 (src-tauri/) |
|------|------------|------------------|
| **UI 渲染** | ✅ 负责 | ❌ 禁止 |
| **用户交互** | ✅ 负责 | ❌ 禁止 |
| **状态管理** | ✅ 负责 (Zustand) | ⚠️ 仅内部状态 |
| **表单验证** | ✅ 初步验证 | ✅ 严格验证 |
| **文件 I/O** | ❌ 禁止 | ✅ 负责 |
| **网络操作** | ❌ 禁止 | ✅ 负责 |
| **业务逻辑** | ❌ 禁止 | ✅ 负责 |
| **系统调用** | ❌ 禁止 | ✅ 负责 |

#### 通信机制

前后端通过 **Tauri IPC** 进行通信，基于 JSON-RPC 协议：

**前端调用后端 (invoke)**:
```typescript
// 前端代码 (src/stores/useServerStore.ts)
import { invoke } from '@tauri-apps/api/core';

async function startServer(config: ServerConfig) {
  try {
    const serverInfo = await invoke<ServerInfo>('start_server', { config });
    return serverInfo;
  } catch (error) {
    console.error('启动服务失败:', error);
    throw error;
  }
}
```

**后端暴露接口 (Command)**:
```rust
// 后端代码 (src-tauri/src/commands/server.rs)
#[tauri::command]
pub async fn start_server(
    config: ServerConfig,
    state: State<'_, AppState>,
) -> Result<ServerInfo, String> {
    // 业务逻辑实现
    state.server_manager
        .start_server(config)
        .await
        .map_err(|e| e.to_string())
}
```

---

## 核心模块设计

### 1. 前端模块 (src/)

#### 1.1 状态管理 (Zustand)

**服务状态管理** (`stores/useServerStore.ts`):
```typescript
interface ServerStore {
  servers: ServerInfo[];           // 服务列表
  loading: boolean;                // 加载状态
  error: string | null;            // 错误信息
  
  // Actions
  fetchServers: () => Promise<void>;
  startServer: (config: ServerConfig) => Promise<ServerInfo>;
  stopServer: (serverId: string) => Promise<void>;
  restartServer: (serverId: string) => Promise<void>;
}
```

**配置状态管理** (`stores/useConfigStore.ts`):
```typescript
interface ConfigStore {
  config: AppConfig;               // 应用配置
  loading: boolean;
  
  // Actions
  loadConfig: () => Promise<void>;
  saveConfig: (config: Partial<AppConfig>) => Promise<void>;
}
```

#### 1.2 组件层次结构

```
App.tsx (根组件)
├── Dashboard.tsx (主仪表盘)
│   ├── ServerCard.tsx (服务卡片) × N
│   │   ├── Button (启动/停止按钮)
│   │   ├── Badge (状态标识)
│   │   └── Link (访问链接)
│   └── NewServerForm (新建服务表单)
│       ├── Input (目录/端口输入)
│       └── Button (浏览/启动按钮)
└── SettingsDialog.tsx (设置对话框)
    ├── Input (配置项输入)
    ├── Switch (开关选项)
    └── Button (保存/取消按钮)
```


### 2. 后端模块 (src-tauri/)

#### 2.1 核心模块架构

```
src-tauri/src/
├── main.rs                       # 应用入口，初始化 Tauri
├── commands/                     # Tauri Commands (IPC 接口层)
│   ├── mod.rs
│   ├── server.rs                 # 服务管理命令
│   ├── config.rs                 # 配置管理命令
│   └── utils.rs                  # 工具命令
├── server/                       # HTTP 服务器模块
│   ├── mod.rs
│   ├── manager.rs                # 服务管理器
│   ├── instance.rs               # 服务实例
│   ├── handler.rs                # HTTP 请求处理器
│   └── performance.rs            # 性能监控
├── config/                       # 配置管理模块
│   ├── mod.rs
│   └── manager.rs                # 配置管理器
├── utils/                        # 工具模块
│   ├── mod.rs
│   ├── port_manager.rs           # 端口管理
│   ├── path_utils.rs             # 路径工具
│   └── logger.rs                 # 日志工具
└── git/                          # Git 自动化模块
    ├── mod.rs
    └── automation.rs             # Git 操作封装
```

#### 2.2 服务管理器 (ServerManager)

**职责**:
- 管理多个 HTTP 服务实例的生命周期
- 检查部署目录唯一性
- 生成服务名称
- 协调端口管理器

**核心数据结构**:
```rust
pub struct ServerManager {
    servers: Arc<RwLock<HashMap<String, ServerInstance>>>,
    data_share: Arc<DataShareLayer>,
}

pub struct ServerInstance {
    pub id: String,                    // UUID
    pub name: String,                  // 从目录提取的名称
    pub config: ServerConfig,
    pub status: ServerStatus,
    pub start_time: i64,
    pub shutdown_tx: Option<oneshot::Sender<()>>,
}
```

#### 2.3 HTTP 服务器 (Axum)

**实现方式**:
- 使用 **Axum** 框架构建高性能静态文件服务器
- 支持 **Range Requests** (视频拖拽播放)
- 自动识别 MIME 类型
- 使用 **Tokio** 异步运行时

**关键特性**:
```rust
// 静态文件服务配置
let app = Router::new()
    .nest_service("/", ServeDir::new(&directory)
        .append_index_html_on_directories(true))
    .layer(
        ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())
            .layer(CompressionLayer::new())
    );

// 支持 Range Requests
let server = axum::Server::bind(&addr)
    .serve(app.into_make_service())
    .with_graceful_shutdown(shutdown_signal);
```

#### 2.4 配置管理器 (ConfigManager)

**职责**:
- 持久化应用配置到文件系统
- 验证配置有效性
- 提供默认配置
- 自动识别 EXE 所在目录

**配置文件位置**: `%APPDATA%/prism-local-server/config.json`

**配置结构**:
```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppConfig {
    pub default_port: u16,
    pub default_directory: String,
    pub default_entry_file: String,
    pub theme: String,
    pub auto_open_browser: bool,
    pub minimize_to_tray: bool,
    pub is_directory_user_set: bool,
}
```

#### 2.5 端口管理器 (PortManager)

**职责**:
- 检测端口可用性 (TCP 连接测试)
- 自动递增查找可用端口
- 限制端口范围 (1024-65535)

**算法**:
```rust
pub async fn find_available_port(start_port: u16) -> Result<u16, ServerError> {
    for offset in 0..MAX_PORT_ATTEMPTS {
        let port = start_port.saturating_add(offset);
        if port > PORT_RANGE_MAX {
            break;
        }
        if check_port_available(port).await {
            return Ok(port);
        }
    }
    Err(ServerError::PortUnavailable(start_port))
}
```

---

## 数据流转

### 服务启动流程

```
用户点击"启动服务"
    ↓
前端组件触发 startServer
    ↓
Zustand Store 调用 invoke('start_server')
    ↓
Tauri IPC 序列化参数为 JSON
    ↓
后端 start_server Command 接收请求
    ↓
ServerManager 验证配置
    ↓
检查目录唯一性
    ↓
PortManager 检查端口可用性
    ↓ (如果被占用)
自动递增查找可用端口
    ↓
启动 Axum HTTP 服务器
    ↓
保存服务实例到 HashMap
    ↓
写入共享数据 (多实例同步)
    ↓
返回 ServerInfo 给前端
    ↓
Zustand Store 更新状态
    ↓
React 组件重新渲染
    ↓
显示服务卡片 + Toast 提示
```


### 配置加载流程

```
应用启动
    ↓
前端调用 loadConfig()
    ↓
invoke('load_app_config')
    ↓
ConfigManager 读取配置文件
    ↓ (如果文件不存在)
创建默认配置
    ↓ (如果 default_directory 为空)
自动识别 EXE 所在目录
    ↓
返回配置对象
    ↓
Zustand Store 保存配置
    ↓
自动填充到主界面输入框
```

---

## 性能优化策略

### 前端优化

1. **代码分割 (Code Splitting)**
   - 使用 React.lazy 和 Suspense 按需加载组件
   - 路由级别的代码分割

2. **组件优化**
   - 使用 React.memo 避免不必要的重渲染
   - 使用 useMemo 和 useCallback 缓存计算结果
   - 虚拟滚动处理大量服务列表

3. **构建优化**
   - Vite 生产构建启用 Terser 压缩
   - 移除 console.log 和 debugger
   - Tree-shaking 移除未使用代码

### 后端优化

1. **异步运行时 (Tokio)**
   - 使用 tokio::spawn 并发处理多个服务
   - 避免阻塞操作，使用异步 I/O

2. **零拷贝技术**
   - 使用 sendfile 系统调用传输大文件
   - 避免不必要的内存复制

3. **资源管理**
   - 使用 RAII 自动释放资源
   - 服务停止时自动关闭端口和文件句柄

4. **编译优化**
   ```toml
   [profile.release]
   opt-level = "z"        # 优化体积
   lto = true             # 链接时优化
   codegen-units = 1      # 单编译单元
   strip = true           # 移除调试符号
   panic = "abort"        # Panic 时直接终止
   ```

---

## 安全考虑

### Tauri 安全模型

1. **最小权限原则**
   - 仅授予必要的 ACL 权限
   - 禁用不需要的 Tauri 插件

2. **IPC 安全**
   - 所有 Commands 进行严格的输入验证
   - 使用 Rust 类型系统防止注入攻击
   - 前端无法直接访问系统 API

3. **路径安全**
   - 验证路径合法性，禁止路径遍历 (`..`)
   - 使用绝对路径，避免相对路径歧义

4. **端口安全**
   - 限制端口范围 (1024-65535)
   - 避免使用系统保留端口

### 内容安全策略 (CSP)

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline'; 
               style-src 'self' 'unsafe-inline';">
```

---

## 错误处理

### 错误分类

1. **用户输入错误**
   - 无效的端口号
   - 不存在的部署目录
   - 无效的入口文件名

2. **资源冲突错误**
   - 端口已被占用 → 自动递增
   - 部署目录已被使用 → 拒绝启动

3. **系统错误**
   - 文件 I/O 失败
   - 网络操作失败
   - 权限不足

### 错误处理策略

**后端 (Rust)**:
```rust
#[derive(Debug, thiserror::Error)]
pub enum ServerError {
    #[error("端口 {0} 超出有效范围 (1024-65535)")]
    InvalidPort(u16),
    
    #[error("部署目录不存在: {0}")]
    DirectoryNotFound(String),
    
    #[error("部署目录已被服务 {name} (端口 {port}) 使用")]
    DirectoryInUse { name: String, port: u16 },
    
    #[error("在 {attempts} 次尝试后未找到可用端口")]
    PortUnavailable { attempts: u16 },
}
```

**前端 (TypeScript)**:
```typescript
try {
  const serverInfo = await invoke<ServerInfo>('start_server', { config });
  toast.success(`服务 ${serverInfo.name} 已启动`);
} catch (error) {
  if (error.includes('DirectoryInUse')) {
    toast.error('该目录已被其他服务使用', { description: error });
  } else {
    toast.error('启动服务失败', { description: error });
  }
}
```

---

## 构建与部署

### 开发环境

```powershell
# 1. 安装依赖
npm install

# 2. 开发模式运行
npm run tauri:dev
```

### 生产构建

```powershell
# 1. 构建前端
npm run build

# 2. 构建 Tauri 应用
npm run tauri:build

# 3. 输出位置
# - EXE: src-tauri/target/release/prism-local-server.exe
# - 安装包: src-tauri/target/release/bundle/msi/*.msi
```

### 构建产物

| 文件 | 大小 | 说明 |
|------|------|------|
| prism-local-server.exe | ~8.5MB | 可执行文件 |
| *.msi | ~12MB | Windows 安装包 |

---

## 性能指标

### 启动性能

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 冷启动时间 | ≤ 1.5s | 首次启动 |
| 热启动时间 | ≤ 0.5s | 后续启动 |
| 首次渲染 | ≤ 0.3s | UI 可见时间 |

### 内存占用

| 场景 | 目标值 | 说明 |
|------|--------|------|
| 空闲状态 | ≤ 50MB | 无服务运行 |
| 运行 1 个服务 | ≤ 80MB | 单服务 |
| 运行 5 个服务 | ≤ 150MB | 多服务 |

### 文件服务性能

| 文件类型 | 响应时间 | 说明 |
|---------|---------|------|
| HTML/CSS/JS | ≤ 10ms | 小文件 |
| 图片 (1MB) | ≤ 50ms | 中等文件 |
| 视频 (Range) | ≤ 100ms | 首帧加载 |

---

## 目录命名说明

### 为什么使用 `src/` 和 `src-tauri/`？

1. **Tauri 官方标准**
   - `src/` 是 Tauri 项目的默认前端目录
   - `src-tauri/` 是 Tauri 项目的默认后端目录
   - 遵循官方约定，便于社区理解和维护

2. **工具链兼容性**
   - Tauri CLI 默认识别这些目录
   - Vite 配置默认指向 `src/`
   - 无需修改大量配置文件

3. **清晰的职责划分**
   - `src/` = 前端 (React/TypeScript)
   - `src-tauri/` = 后端 (Rust)
   - 目录名称已经明确表达了技术栈

### 替代方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| `src/` + `src-tauri/` | ✅ 官方标准<br>✅ 工具链兼容 | ⚠️ 需要文档说明 |
| `frontend/` + `backend/` | ✅ 语义明确 | ❌ 需要修改配置<br>❌ 偏离官方标准 |
| `ui/` + `core/` | ✅ 简洁 | ❌ 不符合 Tauri 约定 |

**结论**: 保持 `src/` 和 `src-tauri/` 命名，通过文档明确说明职责。

---

## 参考资料

- [Tauri v2 官方文档](https://v2.tauri.app/)
- [Rust 异步编程](https://rust-lang.github.io/async-book/)
- [Axum Web 框架](https://docs.rs/axum/)
- [React 官方文档](https://react.dev/)
- [Zustand 状态管理](https://zustand-demo.pmnd.rs/)

---

## 文档维护

**版本**: 1.0  
**最后更新**: 2026-01-20  
**维护者**: Kiro  
**状态**: ✅ 已完成

