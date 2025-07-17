# Linux一键部署

!> Linux平台的一键部署我们依然集成了JDK17，Nginx与MySQL服务需要您自行提供。但在部署过程中我们通过一键启动脚本做了简化

## 目录结构

Linux一键部署方案提供如下目录结构：

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
    - license.zip（需购买后在LCP官网申请）

## 配置文件

和其他部署方式一样，在实际启动前，你依然需要调整现有的配置文件以满足你的自定义需求。linux的一键部署方案中，你只需调整在上述目录结构中的/linux/lib/config/目录下的
application.yml和lc.conf文件即可。内容的调整方式请参考[部署配置文件](/deploy/部署配置文件)。

## 启动项目

根据上述步骤调整好配置文件后，在linux目录下进入终端。运行如下命令启动项目

```shell
./start.sh
 ```

若要停止LCP服务

```shell
./stop.sh
 ```

启动后根据配置的id+端口使用lcp应用。 默认账户 admin / 123456