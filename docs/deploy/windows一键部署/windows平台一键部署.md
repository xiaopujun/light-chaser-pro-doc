# Windows一键部署

!> windows平台的一键部署包内已经集成了jdk17和nginx服务器，但仍需要您自己准备MySQL数据库

## 目录结构

windows一键部署方案提供如下目录结构：

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
    - license.zip（需购买后在LCP官网申请）

## 配置文件

和其他部署方式一样，在实际启动前，你依然需要调整现有的配置文件以满足你的自定义需求。window的一键部署方案中，你只需调整在上述目录结构中的/win/lib/config/目录下的
application.yml和lc.conf文件即可。内容的调整方式请参考[部署配置文件](/deploy/部署配置文件)。

## 启动项目

根据上述步骤调整好配置文件后，双击lcp.exe即可启动整个lcp服务。

启动后根据配置的id+端口使用lcp应用。 默认账户 admin / 123456