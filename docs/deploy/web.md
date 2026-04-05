# Web 端部署

Web 端当前已经收敛为单服务部署：

- `lcp-server` 同时提供前端页面、`/api/**` 接口和 `/static/**` 业务资源
- 不再需要单独的前端 Nginx
- 前端构建产物会随 `server.jar` 一起打包

## 部署前准备

| 项目 | 说明 |
| --- | --- |
| JDK | 推荐 JDK 17 |
| 数据库 | MySQL 8 或兼容版本 |
| 服务端口 | 默认 `8080`，如需修改可在外部配置中指定 |
| 资源目录 | 一个可写的资源根目录，用于保存图片、视频、字体、模型和动态脚本 |
| 授权目录 | 如果你使用授权包，请准备 `license.zip` 所在目录 |

## 推荐流程

1. 在 `backend` 目录构建 `server.jar`
2. 准备外部 `application.yml`
3. 配置数据库和资源目录
4. 按操作系统启动 `server.jar`
5. 访问首页并检查 `/api/**` 和 `/static/**`

## 通用配置示例

下面是一个最小可用的外部配置示例，具体值请按你的环境调整：

```yaml
spring:
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource
    driver-class-name: com.mysql.cj.jdbc.Driver
    druid:
      url: jdbc:mysql://127.0.0.1:3306/light_chaser_server?serverTimezone=GMT%2B8&useUnicode=true&characterEncoding=utf-8
      username: root
      password: 123456

light-chaser:
  resource-path:
    root: /usr/app/light-chaser-server
  # 如果你有授权包，把下面路径指向 license.zip 所在目录
  # license: /usr/app/license
```

?> `light-chaser.resource-path.root` 一定要指向一个可写目录，否则图片、视频、字体、模型和动态脚本资源无法落盘。

## 操作系统入口

- [Windows 部署](web/windows.md)
- [macOS 部署](web/macos.md)
- [Linux 部署](web/linux.md)
