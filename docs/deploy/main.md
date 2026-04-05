# LIGHT CHASER PRO 运行时部署

本章节说明如何把当前版本的运行时发布包部署到服务器，让用户通过浏览器访问项目。

当前版本推荐使用官方运行时发布包部署。一个发布包内已经包含：

- `lcp-runtime`
- `web/`，即 Pure Release 前端资源
- `lcp-runtime-data/`，即运行时数据目录模板
- `部署说明.md`

?> 当前版本不再需要你自己单独准备前端服务器、后端运行环境或数据库来完成运行时部署。

## 推荐阅读顺序

- [Windows运行时部署](windows常规部署/windows常规部署.md)
- [Linux运行时部署](linux常规部署/linux常规部署.md)
- [Windows快速启动](windows一键部署/windows平台一键部署.md)
- [Linux快速启动](linux一键部署/Linux平台一键部署.md)
- [部署参数说明](部署配置文件.md)

## 旧方式

!> Docker 部署已经不建议作为新用户的首选方案，如需查看历史说明，请参考 [Docker部署（弃用）](docker部署/Docker部署.md)。

## 访问地址

- 首页：`http://服务器IP:端口/`
- 入口页：`http://服务器IP:端口/release.html#/`
