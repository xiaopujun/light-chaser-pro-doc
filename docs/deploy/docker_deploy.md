# Docker部署

?> Docker部署仍需要你自行准备MySQL数据库，可以是MySQL镜像，也可以是本地的MySQL服务。

## 目录结构

Docker部署提供如下目录结构

- docker
    - light-chaser-pro.tar # 前端镜像
    - light-chaser-pro-server.tar # 后端镜像

!> 注：使用docker部署前请确保已经安装docker服务，并熟练使用docker命令

## 部署步骤

### 第一步：导入镜像

根据上述目录结构确认镜像文件位置，使用如下命令将镜像导入到docker引擎中

```shell
docker load -i light-chaser-pro.tar
docker load -i light-chaser-pro-server.tar
```

导入后使用 `docker image ls` 命令查看镜像是否导入成功

### 第二步：配置docker compose

在上述镜像的同级目录下创建`docker-compose.yml`文件，修改如下内容

!> 注： 配置docker compose时尤其要注意路径问题，请确保路径正确。 对于docker容器而言，读取的路径始终是容器内部的路径，而不是宿主机的文件路径。不要混淆！

```yaml
version: "3"

services:
  light-chaser:
    image: "light-chaser-pro:0.0.2" # 与docker引擎中的镜像名保持一致
    container_name: light-chaser-container # 容器名，可自定义
    depends_on:
      - light-chaser-server # 依赖于light-chaser-server，先启动后端服务
    volumes: # 卷映射，配置格式为 宿主机路径:容器路径  此配置可以在使用容器启动应用的时候依然使用宿主机的配置文件
      - /usr/app/light-chaser/default.conf:/etc/nginx/conf.d/default.conf:ro # 读取配置文件
    networks:
      - light-chaser-network
    ports:
      - "80:80"
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"


  light-chaser-server:
    image: "lc-server:0.0.2" # 与docker引擎中的镜像名保持一致
    container_name: light-chaser-server-container
    volumes: # 卷映射，配置格式为 宿主机路径:容器路径  此配置可以在使用容器启动应用的时候依然使用宿主机的配置文件,或者将容器内产生的资源存储到宿主机
      - /usr/app/light-chaser-server/config/application.yml:/config/application.yml
      - /usr/app/light-chaser-server/source:/usr/app/resource
      - /usr/app/light-chaser-server/logs:/usr/app/light-chaser-server/logs
    environment:
      - SPRING_CONFIG_LOCATION=/config/application.yml
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

### 第三步：启动容器

当docker compose都配置完毕后，在docker-compose.yml文件所在目录使用如下命令启动容器

```shell
docker compose up  # 此命令将显示的启动前后端容器，并将日志打印到当前控制台

docker compose up -d # 此命令将后台启动前后端容器
```

启动完毕，根据nginx配置的ip地址和端口，即可访问到LIGHT CHASER PRO。 默认账户 admin / 123456

