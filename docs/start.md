## 快速开始

如果你想本地开发或联调当前仓库，需要先准备好开发环境。

## 环境准备

- Git
- Node.js
- pnpm
- Rust toolchain

## 克隆项目

当前仓库地址是 `lcp-desktop`。

```bash
git clone https://github.com/xiaopujun/lcp-desktop.git
```

## 安装依赖

进入项目目录后安装依赖。

```bash
pnpm install
```

## 启动桌面端设计器

```bash
pnpm -F light-chaser-app dev
```

启动完毕后访问本地页面即可查看设计器。

## 启动桌面端联调

```bash
pnpm -F light-chaser-app tauri:dev
```

## 启动运行时联调

```bash
pnpm dev:runtime
```

## 打包

如果你需要打包设计器前端，可以执行：

```bash
pnpm -F light-chaser-app build
```

如果你需要构建运行时发布包，可以执行：

```bash
pnpm build:runtime
```
