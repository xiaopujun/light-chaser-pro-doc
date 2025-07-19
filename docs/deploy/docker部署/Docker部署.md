# Docker部署

?> Docker部署LCP会向您提供前后端镜像文件，前端镜像中包含nginx，后端镜像中包含JDK17。因此这两个环境您无需准备，但您需要准备MySQL数据库，可以是MySQL镜像，也可以是本机的MySQL服务。

## 目录结构

Docker部署提供如下目录结构 +

- docker
    - lcp.tar # 前端镜像
    - lcp-server.tar # 前端镜像
    - nginx.conf # nginx配置文件
    - application.yml # 配置文件
    - docker-compose.yml # docker compose文件

?> 注：使用docker部署前请确保已经安装docker服务，并熟练使用docker命令

## 导入镜像

根据上述目录结构确认镜像文件位置，使用如下命令将镜像导入到docker引擎中

```shell
docker load -i lcp.tar
docker load -i lcp-server.tar
```

导入后使用 `docker image ls` 命令查看镜像是否导入成功

## 修改配置文件

配置文件的调整请参考[配置文件](deploy/部署配置文件.md)

## 配置docker compose

参考下方内容修改docker-compose.yml配置文件

> 1. 每一个通过docker镜像启动的容器。都可以理解为一个最小单位的计算机。
>
>
> 2. 配置docker compose时尤其要注意路径问题，明确容器内部路径与宿主机的文件路径，不要混淆。
     对于docker容器而言，读取的路径始终是容器内部的路径，而不是宿主机的文件路径。

```yaml
version: "3"

services:
  lcp:
    image: "lcp:2025.2" # 与docker引擎中的镜像名和标签保持一致
    container_name: lcp-app # 容器名，可自定义
    depends_on:
      - lcp-server # 依赖于light-chaser-server，先启动后端服务
    volumes: # 卷映射，配置格式为 宿主机路径:容器路径  此配置可以在使用容器启动应用的时候依然使用宿主机的配置文件
      - /nginx/config/path/nginx.conf:/etc/nginx/conf.d/nginx.conf:ro # 读取配置文件
    networks:
      - light-chaser-network
    ports:
      - "80:80"
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"


  lcp-server:
    image: "lcp-server:2025.2" # 与docker引擎中的镜像名和标签保持一致
    container_name: light-chaser-server-container
    volumes: # 卷映射，配置格式为 宿主机路径:容器路径  此配置可以在使用容器启动应用的时候依然使用宿主机的配置文件,或者将容器内产生的资源存储到宿主机
      - /server/config/path/application.yml:/lcp/server/application.yml
      - /server/source/path/source:/lcp/server/resource  # docker部署时建议开启application.yml中的light-chaser.root配置
      - /server/log/path/logs:/lcp/server/logs
    environment:
      - SPRING_CONFIG_LOCATION=/lcp/server/application.yml  # 此处配置读取的是容器内部的路径，注意区分
    networks:
      - light-chaser-network
    ports:
      - "8080:8080"
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"

networks:
  light-chaser-network:
    driver: bridge

```

!> 由于MySQL服务可以直接使用本地服务，也可以通过容器方式启动，因此此处不做选择。请用户自行根据实际情况进行选择。若使用本地的MySQL服务，则在application.yml中配置本地服务地址即可。若使用容器方式启动MySQL服务，则需要自行在docker-compose.yml中添加MySQL服务配置。并在application.yml中配置容器的地址。

### 第三步：启动容器

当docker compose都配置完毕后，在docker-compose.yml文件所在目录使用如下命令启动容器

```shell
docker compose up  # 此命令将显示的启动前后端容器，并将日志打印到当前控制台

docker compose up -d # 此命令将后台启动前后端容器
```

启动完毕，根据nginx配置的ip地址和端口，即可访问到LIGHT CHASER PRO。 默认账户 admin / 123456

