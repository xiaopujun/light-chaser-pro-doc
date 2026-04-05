# Linux Web 部署

本页说明如何在 Linux 上部署 `lcp-server` 单服务。

## 1. 构建 `server.jar`

在仓库的 `backend` 目录执行：

```bash
mvn -pl lcp-server -am package -DskipTests
```

构建完成后，前端页面和后端接口已经一起打进：

- `backend/lcp-server/target/server.jar`

## 2. 准备外部配置

建议把配置文件放到固定目录，例如：

- `/usr/app/light-chaser-server/config/application.yml`

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
    root: /usr/app/light-chaser-server
  # 如果你有授权包，把下面路径指向 license.zip 所在目录
  # license: /usr/app/light-chaser-license
```

## 3. 启动服务

把 `server.jar` 复制到部署目录后，在 shell 中启动：

```bash
export JAVA_HOME=/usr/lib/jvm/temurin-17-jdk
export PATH="$JAVA_HOME/bin:$PATH"
nohup java -jar server.jar --spring.config.location=file:/usr/app/light-chaser-server/config/application.yml > server.log 2>&1 &
```

如果你要长期常驻运行，建议把它写成 `systemd` 服务。下面是一个最小示例：

```ini
[Unit]
Description=Light Chaser Server
After=network.target mysql.service

[Service]
Type=simple
WorkingDirectory=/usr/app/light-chaser-server
ExecStart=/usr/bin/java -jar /usr/app/light-chaser-server/server.jar --spring.config.location=file:/usr/app/light-chaser-server/config/application.yml
Restart=always
RestartSec=5
User=lcp

[Install]
WantedBy=multi-user.target
```

如果你使用这个方式，记得先把 `server.jar` 和 `config/application.yml` 放到上面写的目录。
如果你的机器上没有 `lcp` 用户，就把 `User=` 改成你自己的服务账号，或者先创建一个独立账号再绑定服务。

## 4. 验证部署

打开下面地址检查是否正常：

- `http://服务器IP:8080/`
- `http://服务器IP:8080/api/show/list`
- `http://服务器IP:8080/static/...`

## 5. 常见问题

- 如果页面能打开但图片或视频加载失败，先检查 `light-chaser.resource-path.root` 是否可写
- 如果数据库连不上，先检查 MySQL 地址、账号、密码和端口
- 如果授权相关功能异常，确认 `license.zip` 是否放在配置的授权目录里
