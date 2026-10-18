# 配置面板与 JSON Schema UI

脚手架模板使用 `light-chaser-ui` 提供的 `LCGUI`，根据控件 schema 生成组件的右侧配置面板。配置表单不是必须项；如果需要复杂交互，也可以自行实现 React 配置组件。

## 最小示例

当前 CLI 模板从 `light-chaser-ui` 导入 `Control`、`FieldChangeData` 和 `LCGUI`。schema 中的 `key` 表示要更新的配置字段；控件变化时，`dataFragment` 会包含对应配置片段，可直接传给控制器的 `update()`。

```tsx
import {Control, FieldChangeData, LCGUI} from "light-chaser-ui";
import {Controller} from "./controller";

export const StyleConfig = ({controller}: {controller: Controller}) => {
  const style = controller.getConfig()?.style;
  const schema: Control[] = [
    {
      type: "accordion",
      label: "基础",
      children: [
        {
          type: "grid",
          key: "style",
          children: [
            {
              key: "content",
              type: "input",
              label: "内容",
              value: style?.content,
            },
            {
              key: "fontSize",
              type: "number-input",
              label: "字号",
              value: style?.fontSize,
              config: {min: 1},
            },
          ],
        },
      ],
    },
  ];

  const onFieldChange = ({dataFragment}: FieldChangeData) => {
    controller.update(dataFragment!);
  };

  return <LCGUI schema={schema} onFieldChange={onFieldChange}/>;
};
```

在这个例子中，修改“内容”会产生类似 `{ style: { content: "新内容" } }` 的片段；控制器再把片段合并到组件配置并重新渲染。`accordion` 用于分组，`grid` 用于布局，子控件的 `key` 用来描述数据字段。

## 常用控件

当前脚手架示例实际使用了：

- `input`：文字输入。
- `number-input`：数字输入，可通过 `config` 设置最小值、最大值或步长。
- `select`：下拉选择，选项写在 `config.options`。
- `color-picker`：颜色选择。

控件可用属性以安装的 `light-chaser-ui` 版本和模板类型定义为准。组件属性发生变化时，先确认 schema 的 `key` 路径与 `getInitConfig()` 返回的数据结构一致。
