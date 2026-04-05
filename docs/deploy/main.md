# 软件部署

当前版本的部署文档按三条交付线整理：

- 桌面端安装包：给普通用户安装桌面应用
- Web 端部署：把 `lcp-server` 部署到 Windows / macOS / Linux
- 运行时部署：把 `lcp-runtime` 部署到 Windows / macOS / Linux

?> 如果你只是想让用户下载安装到桌面端，直接看 [桌面端安装包](desktop_install.md)。
?> 如果你要给服务器部署站点服务，先判断是 Web 端还是运行时，再进入对应章节。

## 一览

| 部署线 | 主要产物 | 适用场景 | 入口 |
| --- | --- | --- | --- |
| 桌面端 | Windows 安装包、macOS 安装包 | 普通用户下载安装到本机 | [桌面端安装包](desktop_install.md) |
| Web 端 | `server.jar` | 给服务器部署浏览器访问版 | [Web 端部署](web.md) |
| 运行时 | `lcp-runtime` + `web/` + `lcp-runtime-data/` | 给 Pure Release 同源部署 | [运行时部署](runtime.md) |

## 当前版本要点

- 当前桌面端正式发版通过 [latest.json](https://lcpdesigner.cn/latest.json) 提供当前下载入口
- 当前 Web 端已经收敛为单服务 `lcp-server`
- 当前运行时通过 `lcp-runtime` 同时提供页面、接口和项目资源
- 生产环境不再推荐把运行时拆成独立前端服务器和后端服务

## 推荐阅读顺序

1. [桌面端安装包](desktop_install.md)
2. [Web 端部署](web.md)
3. [运行时部署](runtime.md)

## 历史说明

如果你在维护旧环境，可以继续查看 [旧版部署说明](deploy.md)。
