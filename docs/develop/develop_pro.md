# 使用脚手架开发服务器组件

服务器组件在浏览器中运行。用 `light-chaser-cli` 生成项目并实现组件后，可在本地预览、打包，再从 Web 端“服务器组件”管理页上传。Web 仓库中的 `lcp-web-interface` 只定义接口；组件运行时由 Web 应用提供。

## 环境与创建项目

需要 Node.js、pnpm 和 TypeScript/React 基础。CLI 模板使用 Vite，且 `pnpm install` 用于安装生成项目的依赖。CLI 包当前没有声明 `engines`，因此本仓库无法给出可靠的 Node.js 最低版本；安装后先用 `light-chaser-cli -V` 确认版本。

```bash
npm install -g light-chaser-cli
light-chaser-cli -V
light-chaser-cli create my-components
cd my-components
pnpm install
```

`create` 会在当前目录下创建项目文件夹；若同名目录已存在，CLI 会询问是否覆盖。生成的示例组件位于 `src/components/remote-button/`。

## 开发与本地预览

```bash
light-chaser-cli dev
```

脚手架开发服务器使用 `http://localhost:3000/`。首页列出被识别的组件，点击组件可查看组件效果及其配置面板。

## 组件文件

模板示例按组件目录组织：

| 文件 | 用途 |
| --- | --- |
| `definition.ts` | 定义唯一的 `compKey`、名称、初始配置、预览图、配置菜单及蓝图事件/动作。服务器组件的 `getBaseInfo()` 必须保留 `source: 'remote'` |
| `controller.ts` | 实现组件创建、配置更新、数据变更、事件注册、主题更新和销毁 |
| `component.tsx` | 渲染组件界面；模板示例用 React 组件和 `forwardRef` 暴露更新配置、绑定事件的方法 |
| `config.tsx` | 实现组件右侧配置表单，可用 `light-chaser-ui` 的 `LCGUI` 与 `Control` schema |
| `component.module.less` | 样式 |
| `*.png` | 组件列表中的预览图 |

组件 ID `compKey` 需要唯一。定义类应继承模板提供的 `AbstractDesignerDefinition`，并返回基础信息、初始配置、控制器、预览图和配置菜单映射。设计器组件还可以定义事件列表和动作列表，蓝图会按定义显示相应锚点。

控制器需要实现 `AbstractDesignerController` 的运行约定。`create(container, config, executor, index?)` 接收组件容器、初始配置、蓝图执行器及可选循环索引；`update()` 更新样式或其他配置，`changeData()` 更新组件数据，`registerEvent()` 把组件交互转发给蓝图，`destroy()` 释放定时器、监听器和组件实例。

下面是点击事件接入蓝图的核心写法：

```ts
registerEvent() {
  const componentId = this.config?.base?.id;
  this.instance?.setEventHandler({
    click: () => this.bpExecutor?.triggerComponentEvent(componentId!, "click", this.config, this.index),
  });
}
```

如果组件支持网络或静态数据，需在 `loadComponentData()` / `changeData()` 中实现加载与重新渲染；如果组件使用全局主题，还需在 `updateTheme()` 中处理主题变化。组件的配置项 schema 见[配置面板与 JSON Schema UI](/develop/ui.md)。

## 打包并上传

```bash
light-chaser-cli build
```

不带组件名时，CLI 会打包 `src/components/` 下的所有组件；指定一个目录名可单独打包，例如 `light-chaser-cli build remote-button`。打包前会清空 `dist/`，每个组件输出为 `dist/<目录名>.js`。当前 CLI 参数只声明一个可选组件名，旧文档中的逗号分隔多组件命令不适用。

1. 登录 Web 端，打开首页的“服务器组件”。
2. 点击“上传”，选择脚手架生成的 `.js` 文件；管理页也接受 `.mjs` 或 `.zip` 文件。
3. 上传后组件会出现在设计器的组件库中，可像其他组件一样添加到画布。

需要更新已上传组件时，使用管理页中的“替换”操作。删除组件前，先确认没有项目引用它；Web 端删除确认提示也说明了这一影响。

> 本文中的 `create`、`dev`、`build` 行为按当前可核对的 `light-chaser-cli 0.0.11` 模板说明。CLI 模板使用 `light-chaser-interface`、`light-chaser-types`、`light-chaser-ui`、`light-chaser-util` 这些依赖名；请保留生成模板中的包名，不要直接替换成 Web 仓库的 workspace 包名。
