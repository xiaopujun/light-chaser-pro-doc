# 软件部署

当前功能指南对应 Web 端：浏览器访问同一个 `lcp-server` 服务，由它提供前端页面、`/api/**` 和 `/static/**`。部署 Web 站点优先查看 [Web 端部署](/deploy/web.md)。

## 选择 Web 部署包

| 部署方式 | 主机条件 | 数据库 | 说明 |
| --- | --- | --- | --- |
| 常规部署包 | Java 17 | 自行准备 MySQL | 包含 `server.jar`、`component-docs/`、外部配置及平台启动脚本 |
| Docker app | Docker 与 Compose | 自行准备 MySQL 8.0 | 应用在容器中运行，资源保留在部署目录 |
| Docker allinone | Docker 与 Compose | 容器内 MySQL | 应用和数据库在同一容器中，数据保存在宿主机 `data/` |

- [Windows 常规部署](/deploy/web/windows.md)
- [Linux 常规部署](/deploy/web/linux.md)
- [Docker app / allinone 部署](/deploy/web/docker.md)
- [Web 升级与验证](/upgrade/upgrade.md)

本节面向已取得部署包的使用者。源码开发启动见 [开发环境](/start.md)。

## 其他交付方式

以下页面保留为独立交付方式或历史版本参考，未按 `lcp-web` 工程推断其当前发行状态：

- [桌面端安装包](/deploy/desktop_install.md)：安装到用户电脑的桌面应用。
- [独立运行时](/deploy/runtime.md)：另一套项目展示服务，不是当前 Web 的 `lcp-server`。
- [旧版部署说明](/deploy/deploy.md)：维护历史环境时参考。

Web 包的目录、参数和命令不应与上述其他交付方式混用。
