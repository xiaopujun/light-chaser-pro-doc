# 一键部署

?> LIGHT CHASER PRO支持在window和linux下的一键部署。一键部署仍需自行准备MySQL数据库

## 目录结构

一键部署方案提供如下目录结构：

- win
    - lib
        - app
        - config
            - application.yml （后端服务修改此配置文件）
            - lc.conf （前端服务修改此配置文件）
        - jdk-17
        - nginx
        - server
            - server.jar
    - lcp.exe
    - license.zip
- linux
    - lib
        - app
        - config
            - application.yml （后端服务修改此配置文件）
            - lc.conf （前端服务修改此配置文件）
        - jdk-17
        - server
            - server.jar
    - lcp (linux可执行文件)
    - start.sh (linux启动脚本)
    - stop.sh (linux停止脚本)
    - license.zip

请根据自身需要选择合适的一键部署版本

## window一键部署

如目录结构所示，window下的一键部署已经为你准备好了jdk和nginx。除了MySQL数据库外你不需要在安装任何其他基础软件。
你需要做的仅仅是根据自身场景需要调整config目录下的配置文件。然后双击lcp.exe即可启动整个lcp服务。修改配置项请参考[配置项](/deploy/bootstrap_deploy?id=配置项参考)。

## linux一键部署

linux下的一键部署需要自行准备MySQL数据库。另外你还需安装nginx。除此之外不再需要其他基础软件。配置文件的修改与window一样，可参考[配置项](/deploy/bootstrap_deploy?id=配置项参考)。
在准备好上述内容后执行`start.sh`即可启动整个lcp服务。 执行`stop.sh`即可停止整个lcp服务。

## 配置项参考

配置文件均在`lib/config`目录下。

nginx配置

```nginx configuration
server {
    client_max_body_size 10M;
    listen               9091; # 修改为自定义端口
    server_name          localhost; # 修改为自己的ip或域名

    root  ../app;
    index index.html;

    location / {
        try_files $uri       $uri/ @router;
        index     index.html;
    }

    location ~ /(api|static)/ {
        proxy_pass       http://127.0.0.1:9999; # 修改为后端服务的ip和端口
        proxy_set_header Host                  $host;
        proxy_set_header X-Real-IP             $remote_addr;
        proxy_set_header X-Forwarded-For       $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto     $scheme;
    }

    location @router {
        rewrite ^.*$ /index.html last;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root html;
    }
}
```

后端服务配置

```yaml
spring:
  servlet:
    multipart:
      max-file-size: 50MB
      max-request-size: 50MB
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource
    driver-class-name: com.mysql.cj.jdbc.Driver
    druid:
      url: jdbc:mysql://修改为自己的数据库服务器地址:3306/修改为自己创建的数据库名?serverTimezone=GMT%2B8&useUnicode=true&characterEncoding=utf-8
      username: 替换为自己的MySQL用户名
      password: 替换为自己的MySQL密码
server:
  port: 9999 # 修改为自定义端口

# mybatis-plus配置
mybatis-plus:
  type-aliases-package: com.dagu.lcserver.model
  global-config:
    db-config:
      logic-delete-field: deleted
      logic-delete-value: 1
      logic-not-delete-value: 0
  configuration:
    map-underscore-to-camel-case: true

logging:
  config: classpath:log4j2-spring.xml
  level:
    cn.jay.repository: info


light-chaser:
  #  license: C:/Users/DAGU/Desktop/license # 可选配置，不配置的情况下默认读取执行命令路径下的license.zip文件
  resource-path:
    root: D:/project/light-chaser-server # 必须配置，lcp产生的所有文件都将基于此路径进行保存
    image: /static/images
    cover: /static/covers
    avatar: /static/avatar
    remote-component: /static/components
  file:
    image-max-size: 10MB
    max-size: 20MB
  migration: # 是否自动跑sql脚本
    enable: true
#  mode: test


```

启动后根据配置的id+端口使用lcp应用。 默认账户 admin / 123456