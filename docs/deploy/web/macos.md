# macOS Web 部署

本页说明如何在 macOS 上部署 `lcp-server` 单服务。

## 1. 构建 `server.jar`

在仓库的 `backend` 目录执行：

```bash
mvn -pl lcp-server -am package -DskipTests
```

构建完成后，前端页面和后端接口已经一起打进：

- `backend/lcp-server/target/server.jar`

## 2. 准备外部配置

建议把配置文件放到固定目录，例如：

- `/Users/Shared/light-chaser-server/config/application.yml`

最少需要配置数据库和资源根目录。示例：

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
    root: /Users/Shared/light-chaser-server
  # 如果你有授权包，把下面路径指向 license.zip 所在目录
  # license: /Users/Shared/light-chaser-license
```

## 3. 启动服务

把 `server.jar` 复制到部署目录后，在终端中启动：

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"
nohup java -jar server.jar --spring.config.location=file:/Users/Shared/light-chaser-server/config/application.yml > server.log 2>&1 &
```

如果你要长期常驻运行，可以再把这条命令包到 `launchd` 任务里。

## 4. 验证部署

打开下面地址检查是否正常：

- `http://服务器IP:8080/`
- `http://服务器IP:8080/api/show/list`
- `http://服务器IP:8080/static/...`

## 5. 常见问题

- 如果页面能打开但图片或视频加载失败，先检查 `light-chaser.resource-path.root` 是否可写
- 如果数据库连不上，先检查 MySQL 地址、账号、密码和端口
- 如果授权相关功能异常，确认 `license.zip` 是否放在配置的授权目录里
