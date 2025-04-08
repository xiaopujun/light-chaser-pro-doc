# 脚手架开发组件

## 总览

LIGHT CHASER PRO开发自定义组件需要使用官方提供的脚手架来辅助开发。而不需要依赖源码。此种方式更简洁明了

?> LIGHT CHASER PRO 开发自定义组件需要熟悉前端相关技术栈，包括html、css、js、React、Vite、TypeScript、pnpm。自定义组件前请确保你已经掌握了相关技术栈

## 环境准备

?> LIGHT CHASER PRO使用pnpm作为包管理器，为确保兼容性，请使用pnpm进行依赖管理

开发自定义(服务器)组件，你需要准备以下开发环境

- `Node.js`: 版本>18.x.x
- `pnpm`: 版本>7.x.x
- `IDE`: 推荐使用VSCode、WebStorm

当上面的都准备好了之后，你需要全局安装LIGHT CHASER PRO提供的开发脚手架

```shell
npm install -g light-chaser-cli
```

安装完毕后使用使用light-chaser-cli -V或者light-chaser-cli --version命令查看版本号.

![查看版本.png](查看版本.png)

如上图显示说明安装成功。

## 创建项目

使用`light-chaser-cli create <workspace>`命令创建一个自定义组件项目

![创建项目.png](创建项目.png)

## 安装依赖

脚手架创建的项目同样建议使用pnpm进行依赖管理，使用`pnpm i`命令安装项目依赖

![安装脚手架项目依赖.png](安装脚手架项目依赖.png)

## 启动项目

依赖安装完毕后使用`light-chaser-cli dev`命令启动项目

![启动脚手架项目.png](启动脚手架项目.png)

访问 http://localhost:3000/ 即可看到项目列表

![脚手架组件列表.png](脚手架组件列表.png)

![脚手架组件效果.png](脚手架组件效果.png)

## 组件开发

当你用IDE打开脚手架创建的目录后，默认会带一个示例，组件的具体实现可参考示例代码。其目录结构如下图所示。

![编写脚手架组件.png](编写脚手架组件.png)

!> 注意：Pro版本的脚手架中每个目录下的文件命名最好与示例保持一致不要单独调整。特别是definition.ts文件。不要改动文件名。

### 核心文件及接口概念

在LIGHT CHASER PRO接入自定义组件的过程中一共涉及到6个必须的文件，分别是：

- definition.ts: 自定义组件信息定义文件，用于定义自定义组件的所有基础信息和初始配置数据

- controller.ts: 自定义组件控制器，用于管理自定义组件的整个生命周期，后续所有对自定义组件的操作都要依赖于controller文件的实例对象，所以理解他十分重要！

- component.tsx: 自定义的React组件，用于渲染自定义组件的UI，本质上和普通的React组件没有任何区别。事实上这个文件是非必须的，除非你完全自己实现React组件。
  对于像Echarts、G2这样的图表库而言，它们有自己的API可以直接创建页面元素

- component.less: 组件样式文件

- config.tsx: 自定义组件的右侧配置面板，用于配置自定义组件的属性，本质上也是一个普通的React组件

- xxx.png/jpg: 自定义组件的预览图，用于在设计器的组件列表中展示自定义组件的缩略图

### Controller定义说明

controller接口为LIGHT CHASER自定义组件接入的核心接口之一，他定义操作自定义组件生命周期的一系列标准方法。包括创建组件、修改组件配置，触发组件重新渲染等。其详细的定义如下：

> 注：controller存在一个抽象接口的继承体系，其中AbstractController是最顶级的抽象接口，其下为了功能扩展会派生出一些子接口：其中最为重要的便是AbstractDesignerController

**AbstractController定义**

```ts

export interface UpdateOptions {
  reRender: boolean;
}

/**
 * 设计器自定义组件控制器的顶级抽象接口，用于控制自定义组件的整个生命周期
 * @param I 组件实例类型，若组件为React的class组件，则I=class的实例化对象。
 * 若组件为React的函数式组件，则I=forwardRef钩子传递出的ref引用（当然你也可以有其他自定义的实现）
 * 若组件为纯Js实现的组件，则I=组件实例化对象（可参考Echarts活G2创建实例后的返回值）
 * @param C 组件配置类型，即组件的完整属性类型
 */
abstract class AbstractController<I = any, C = any> {

  /**
   * 组件实例引用
   * @protected
   */
  protected instance: I | null = null;
  /**
   * 组件配置(包括组件数据)
   * @protected
   */
  public config: C | null = null;
  /**
   * 组件所处容器的dom元素
   * @protected
   */
  public container: HTMLElement | null = null;

  /******************生命周期******************/

  /**
   * 创建组件并将组件挂载到指定的容器中
   * @param container 容器
   * @param config 组件配置
   * @param others 组件配置
   */
  public abstract create(container: HTMLElement, config: C, ...others: unknown[]): Promise<void>;

  /**
   * 更新组件配置，并触发组件重新渲染
   * @param config 组件属性（参数）
   * @param upOp 操作类型
   */
  public abstract update(config: C, upOp?: UpdateOptions): void;

  /**
   * 销毁组件
   */
  public destroy(): void {
    this.instance = null;
    this.config = null;
    this.container = null;
  }


  /******************普通方法******************/
  /**
   * 获取组件配置数据
   */
  public abstract getConfig(): C | null;

}

export default AbstractController;


```

**AbstractDesignerController定义**

```ts

/**
 * AbstractDesignerController继承自AbstractController，在泛型的定义和约束上和AbstractController完全保持一致。
 * 此外，AbstractDesignerController扩展了一些自定义组件所需的特有方法，如：修改组件数据、注册蓝图事件等
 */
abstract class AbstractDesignerController<I = any, C = any> extends AbstractController<I, C> {
  //上一次数据连接状态 true：成功 false：失败
  protected lastReqState: boolean = true;
  //异常提示信息dom元素
  private errMsgDom: HTMLElement | null = null;
  //蓝图事件触发器
  public bpExecutor: BPExecutor | null = null;
  //组件统一数据更新器
  public componentDataUpdater: ComponentDataUpdater | null = null;

  public abstract create(container: HTMLElement, config: C, bpExecutor: BPExecutor): Promise<void>;

  /**
   * 更新组件数据,且必须触发组件的重新渲染
   * @param data
   */
  public changeData(data: any): void {
  }

  /**
   * 用于注册组件事件，在组件接入蓝图事件系统时使用
   */
  public registerEvent(): void {
  }

  /**
   * 加载组件数据，用于在预览（展示）模式下渲染完组件后根据当前组件的数据配置自动加载并更新组件数组。
   * 注：若自定义组件有自己的数据加载方式，则需要覆写此方法
   */
  public loadComponentData(): void {
  }

  /**
   * 更新本组件的主题样式方法，用于在全局切换主题时使用
   * @param newTheme 新主题
   */
  public updateTheme(newTheme: ThemeItemType): void {
  }

  public updateFilter(filter: IFilterConfigType): void {
    
  }

  /**
   * 设置组件的显示状态，默认直接使用css属性控制组件显示。
   * 接入组件的过程中，建议自行实现该方法以达到更好的性能表现。建议的做法是显示时重新渲染组件. 隐藏时卸载整个组件即dom元素。可以节省内存开销
   * @param visible
   */
  public setVisible(visible: boolean): void {
    
  }


  destroy() {
    
  }
}

export default AbstractDesignerController;
```

### Definition定义说明

definition.ts 是定义组件所有基础信息和初始化数据的文件，其完整结构如下：

```ts

/**
 * 自动扫描抽象组件定义核心类。
 * 对于所有继承并实现了该抽象类的子类，都会被自动扫描到并注册到设计器中。
 * 因此，所有要接入设计器的react组件都应该按照该类的约定实现其所有的方法。
 *
 * 泛型说明：
 * C: 组件控制器类，用于指定当前组件定义对应的控制器类
 * P: 组件配置类型，用于指定当前组件的配置数据(config属性的类型)
 */
export abstract class AbstractDefinition<C extends AbstractController = AbstractController, P = any> {

  /**
   * 返回组件基础信息，用于在组件列表中展示
   */
  abstract getBaseInfo(): BaseInfoType ;

  /**
   * 返回组件的初始配置，用于在画布渲染组件时的初始化组件数据
   */
  abstract getInitConfig(): P;

  /**
   * 返回React组件Controller控制器的类模板，在画布中创建组件实例时会根据该方法的返回值实例化组件控制器并保存。
   * 后续将通过该控制器的实例对象来控制组件的生命周期
   */
  abstract getController(): ClazzTemplate<C> | null;

  /**
   * 返回组件图片缩略图，在组件列表中展示时使用。图片尺寸越小越好
   */
  abstract getChartImg(): string | null;

  /**
   * 返回右侧配置菜单列表，双击组件时需要展示该菜单列表
   */
  abstract getMenuList(): Array<MenuInfo>;

  /**
   * 返回右侧菜单与对应配置内容组件的映射关系
   */
  abstract getMenuToConfigContentMap(): MenuToConfigMappingType;



  /**
   * 自定义组件主分类，如需要创建一个设计器没有提供的主分类，则实现该方法
   */
  getCategorize(): ICategorize | null {
    return null;
  }

  /**
   * 自定义组件子分类,如需要创建一个设计器没有提供的子分类，则实现该方法
   */
  getSubCategorize(): ICategorize | null {
    return null;
  }
}
```

如上，我们介绍了接入自定义组件过程中最重要的两个核心文件controller.ts和definition.ts，请务必重点理解这两个文件的作用和使用方法。并在实际开发组件的过程加以理解

## 打包组件

当你的组件编写测试完成之后，使用`light-chaser-cli build`命令打包组件，会在dist目录下生成一个组件包。

打包命令：

- `light-chaser-cli build`：打包所有组件
- `light-chaser-cli build <componentName>`：打包指定组件，componentName为组件所在的文件夹名称。多个componentName之间用","分隔

![打包组件.png](打包组件.png)

![上传组件.png](上传组件.png)

打开主设计器，并查看组件列表，你应该可以看到刚才上传的组件。组件的操作与默认集成的标准组件没有任何区别

![加载服务器组件.png](加载服务器组件.png)