# Windows Web 部署

本文说明常规 Web 发布 ZIP 的 Windows 部署。请从发布 ZIP 解压完整文件，不要只复制 `server.jar`：包内启动脚本还会读取配置和同级的 `component-docs/`。

## 准备目录和数据库

例如将发布包解压到 `D:\light-chaser-server\`。目录中应保留：

- `server.jar`
- `component-docs\`
- `config\application.yml`
- `deploy_windows.cmd` 及包内其他文件

部署机需安装 Java 17，并准备可用的 MySQL 实例。启动入口默认使用 `127.0.0.1:3306`，首次运行会交互询问数据库名、用户名和密码；启动账号需具备应用运行和数据库迁移所需权限。

资源根目录可不配置，默认以 Java 进程工作目录为基准。若改用专门的数据目录，在 `config\application.yml` 中配置 `light-chaser.resource-path.root`，并确保运行账号有写权限。

## 启动和管理

在文件资源管理器中双击 `deploy_windows.cmd`，或在 PowerShell 的发布包根目录运行：

```powershell
Set-Location D:\light-chaser-server
.\deploy_windows.cmd
```

首次启动按提示填写数据库连接信息。应用在后台运行；标准输出和错误日志分别写入 `logs\startup.stdout.log` 与 `logs\startup.stderr.log`。后续可用：

```powershell
.\deploy_windows.cmd --check
.\deploy_windows.cmd --status
.\deploy_windows.cmd --restart
.\deploy_windows.cmd --stop
```

`--check` 只读检查，不会提示或修改配置；缺少数据库值时会报告错误。`--status`、`--stop` 和 `--restart` 管理当前发布目录记录的进程。脚本不会安装 Java、注册 Windows 服务或配置开机自启。常驻运行时，可按需把发布目录入口接入你使用的 Windows 服务管理工具。

## 手动运行（可选）

若自行管理进程，可在启动前填好 `config\application.yml`，然后用 Java Agent 启动。示例假设发布包位于 `D:\light-chaser-server\`：

```powershell
Set-Location D:\light-chaser-server
java "-javaagent:D:\light-chaser-server\server.jar" `
  -jar "D:\light-chaser-server\server.jar" `
  --spring.config.location=file:D:/light-chaser-server/config/application.yml
```

手动启动不会使用包内脚本的进程状态和日志管理。无论采用哪种方式，都要保留 `component-docs\` 与 `server.jar` 同级；若通过远程发布脚本只替换了 JAR，也要把发布 ZIP 中对应的 `component-docs\` 同步到该目录。

## 验证

打开 `http://服务器IP:8080/` 检查页面。应用 API 例如 `/api/show/list`；业务资源会通过 `/static/**` 提供。端口默认为 `8080`，可在配置文件的 `server.port` 修改。
