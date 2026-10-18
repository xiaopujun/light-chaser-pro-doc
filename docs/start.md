# Web 源码开发启动

本页面向 `lcp-web` 工程开发者。仅使用产品或部署成品时，分别查看 [快速开始](/quick_start/quick_start.md)和 [Web 部署](/deploy/web.md)。

## 工程与环境

| 目录 | 内容 |
| --- | --- |
| `frontend/` | pnpm workspace，主应用包为 `lcp-web-app` |
| `backend/` | Maven 多模块工程，应用模块为 `lcp-server` |
| `script/build/` | 常规和 Docker 发布包构建脚本 |
| `tests/` | 独立测试工程 |

准备 Git、Node.js、pnpm、**JDK 17**、Maven 和可用的 MySQL。若运行统一发布包构建脚本，Node.js 需为 20+，且 Docker 构建还需要 Docker Buildx；仅开发前端不需要 Docker。

## 安装前端依赖

从工程根目录进入 `frontend/`：

```bash
cd frontend
pnpm install
```

## 启动后端

使用 IDE 以 Maven 工程打开 `backend/pom.xml`，选择 JDK 17。默认 `application.yml` 激活 `dev` 配置，因此需要在 `backend/lcp-server/src/main/resources/application-dev.yml` 中设置你自己的数据库地址、数据库名、用户名和密码，也可在 IDE 启动参数中显式指定其他配置。`application-template.yml` 只是字段参考，不会自动加载；不要直接使用模板里的占位值。

运行 `com.zsq.lcpserver.LcpServerApplication`。默认开发代理目标是 `http://127.0.0.1:8080`；请确认后端日志没有数据库或迁移错误，并具备对应目录的写入权限。数据库初始化需要配置账号具备相应权限；也可以先由数据库管理员建库。

## 启动前端

在 `frontend/` 目录另开终端：

```bash
pnpm -F lcp-web-app dev
```

以 Vite 终端实际打印的地址打开浏览器。默认空闲端口通常为 `5173`；`/api/**` 与 `/static/**` 代理到同一个后端。

如果后端端口不同，在 macOS/Linux 终端可指定：

```bash
LCP_SERVER_DEV_TARGET=http://127.0.0.1:18080 pnpm -F lcp-web-app dev
```

Windows PowerShell 对应写法：

```powershell
$env:LCP_SERVER_DEV_TARGET = "http://127.0.0.1:18080"
pnpm -F lcp-web-app dev
```

仅启动 Vite 不会提供登录、项目保存和资源接口；这些功能需要真实后端与数据库。

## 构建与检查

以下命令均在 `frontend/` 执行：

```bash
pnpm -F lcp-web-app build
pnpm -F lcp-web-app docs:test
pnpm -F lcp-web-app test
```

`build` 会先生成组件文档，再执行 TypeScript 检查和 Vite 构建。生产 Web 包由后端同时托管页面、接口和资源；不要将 Vite 开发服务器当作生产部署方式。完整发布包的构建参数见源码中的 `script/build/README.md`。
