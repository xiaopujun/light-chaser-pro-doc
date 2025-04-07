# 常规部署

## 部署环境准备

常规部署需要自行准备除源码包以外的其他环境，具体如下：

- `Nginx`：用于部署lcp的前端部分
- `JDK17`：用于部署lcp的后端部分
- `MySQL`：用于存储lcp的数据（版本5.7-8.0均可）

## 目录结构

常规部署提供如下目录结构

- `app`: 前端源码目录，需要配合nginx进行部署
- `server.jar`: 后端jar文件，需要配合MySQL + JDK17进行部署

## 部署步骤

### 第一步：准备MySQL数据库

在自行准备好MySQL服务后，创建名为light_chaser_pro的数据库（数据库名称可自定义，但需要和后续后端配置文件中的数据库名保持一致）

```mysql
create database light_chaser_pro default character set utf8mb4;
```

### 第二步：部署后端

?> 部署前请确保已经准备好了JDK17并配置好了环境变量。

!> 后端启动需要license文件。若没有license，请联系作者购买

在server.jar的同级目录下创建一个名为`application.yml`文件，并配置如下内容

```yaml
spring:
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource
    driver-class-name: com.mysql.cj.jdbc.Driver
    druid:
      url: jdbc:mysql://替换为你ip地址:3306/light_chaser_pro?serverTimezone=GMT%2B8&useUnicode=true&characterEncoding=utf-8
      username: 替换为你的数据库用户名
      password: 替换为你的数据库密码
  servlet:
    multipart:
      max-file-size: 50MB
      max-request-size: 50MB

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
  license: C:/Users/DAGU/Desktop/license # 可选配置，不配置的情况下默认读取执行命令路径下的license.zip文件
  resource-path:
    root: D:/project/light-chaser-server # 必须配置，lcp产生的所有文件都将基于此路径进行保存
    image: /static/images
    cover: /static/covers
    avatar: /static/avatar
    remote-component: /static/components
  file:
    image-max-size: 50MB
  migration:
    enable: true  # 是否自动跑sql脚本，可保持开启，当lcp有新功能新脚本时，会自动更新数据库内容

```

当准备好上面所需文件和jdk后使用命令启动后端服务

```shell
java -javaagent:server.jar -jar server.jar
```

### 第三步：部署前端

- 定位nginx配置文件，如果是window，配置文件在nginx安装目录的conf目录下，如果是linux，可以通过命令`nginx -t`查看配置文件路径
- 参考以下配置，修改配置文件内容并保存

```nginx configuration
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;
#pid        logs/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
            client_max_body_size 10M;
            listen       80; #可替换为自己所需端口
            server_name  www.lcp.com; #替换为自己服务器的ip或者域名
        
            root /usr/app; # 替换为app所在目录
            index index.html;

            location / {
                try_files $uri $uri/ @router;
                index index.html;
            }

            location ~ /(api|static)/ {
                    proxy_pass www.lcp.com; #替换为自己后端服务器的ip或者域名:后端服务端口
                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;
            }

            location @router {
                rewrite ^.*$ /index.html last;
            }

            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root   html;
            }
        }
}
```

- 启动/重启nginx服务器
- 根据对应域名/ip + 端口访问lcp页面

?> 如果是linux系统，并且nginx配置文件内容中包含`include /etc/nginx/conf.d/*.conf;`则可在`/etc/nginx/conf.d`目录下直接创建单独的配置文件，并配置独属于lcp的server块

至此，lcp常规部署完成，可通过访问域名/ip + 端口使用lcp应用。默认账户 admin / 123456


