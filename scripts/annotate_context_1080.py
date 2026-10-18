#!/usr/bin/env python3
"""Give reused overview captures task-specific instructional annotations."""

from __future__ import annotations

import argparse
from pathlib import Path

from annotation_rules import RuleCard, SOURCE_DIR, render


# Evidence paths are relative to lcp-web/frontend/lcp-web-app/src.
SPECS = {
    # ThemeHdItemImpl.updateGlobalTheme calls currentManager.layerManager.flashGlobalTheme;
    # LayerManager.flashGlobalTheme visits all current canvas controllers. ThemeConfig.themeChange
    # calls updateTheme only on rightStore.activeElem.id.
    "designer-theme": ("designer-overview", (
        RuleCard(
            "统一换色，要确认后再批量应用",
            ("点顶栏主题图标，选择预设并检查预览。", "点击「更新全局主题」才批量应用到当前画布。"),
            "只想改一个组件时，不要更新全局主题。",
            (470, 145, 1140, 375), (1075, 36), ((1057, 18, 1092, 55),), badge=(1075, 86),
        ),
        RuleCard(
            "只改一处，就从目标组件的配置入手",
            ("双击目标组件，在右侧「主题」中选择预设。", "此入口只更新所选组件，不会逐个修改全画布。"),
            "不同组件支持的配置不同，以实际可用标签为准。",
            (1170, 730, 1860, 980), (1210, 375), badge=(1330, 330),
        ),
    )),
    # footer/cover/CoverConfig.beforeUpload returns false; doSave calls BaseApi.uploadCover.
    # BaseApi/cover endpoint updates the cover reference rather than component layout.
    "designer-cover": ("designer-project-menu", (
        RuleCard(
            "选图后保存，才会上传封面",
            ("从「设置封面快照」打开窗口，再选择图片。", "检查 JPG / PNG / WebP 预览后，点击保存封面。"),
            "只选图片或看到预览，不等于已经上传保存。",
            (1040, 75, 1670, 315), (1734, 279), ((1734, 261, 1897, 297),), badge=(1710, 279),
        ),
        RuleCard(
            "封面用于项目列表，不会替换画布",
            ("封面帮助你在项目列表里识别项目。", "更换封面不会改变当前画布里的图表或图片。"),
            "要修改展示页面内容，请回画布编辑组件。",
            (1050, 780, 1710, 1010), (1547, 740),
        ),
    )),
    # HotKeyPlatform resolves primary to Command/Ctrl. ShortcutStore.updateBinding rejects
    # conflicting bindings; HotKey.tsx skips editable targets unless allowInInput is true.
    "designer-shortcuts": ("designer-overview", (
        RuleCard(
            "先看本机当前绑定，再使用快捷键",
            ("点工具栏 ?，查看当前系统生效的实际按键。", "macOS 主键为 ⌘，Windows 主键为 Ctrl。"),
            "默认组合可能已被修改或禁用，以面板为准。",
            (1170, 145, 1850, 375), (1240, 36), ((1222, 18, 1259, 55),), badge=(1240, 86),
        ),
        RuleCard(
            "画布编辑快捷键，要在画布范围内使用",
            ("先点回画布或图层，再执行复制、移动等操作。", "输入框接收文字时，通常不会执行画布编辑。"),
            "更改绑定时遇到冲突，应先换一个组合。",
            (1050, 770, 1740, 1000), (199, 740), (), ((980, 900), (180, 900), (180, 740)),
        ),
    )),
    # blueprint/footer/BPFooter handles switching, rename, add, delete confirmation.
    # BluePrintPageManager.getData stores page-local maps; BluePrintManager.deleteBptPage
    # refuses the last page. Pages organize the flow; this is not a tab-controlled runtime switch.
    "blueprint-pages": ("blueprint-overview", (
        RuleCard(
            "按流程拆页，点页签切换编辑",
            ("每页分别保存节点、连线与节点布局。", "点页签切换，双击名称可重命名。"),
            "切换编辑页，不会把各页合并成一张画布。",
            (420, 720, 1090, 980), (95, 1037), ((95, 1019, 228, 1057),), badge=(160, 995),
        ),
        RuleCard(
            "用 + 新建页，页签菜单里删除",
            ("可把初始化与点击联动拆到不同页面。", "删除页签前会再次确认，并移除该页内容。"),
            "必须保留至少一页，最后一页不能删除。",
            (1160, 720, 1840, 980), (262, 1019), ((244, 1019, 280, 1057),), ((1130, 1005), (325, 1005)), badge=(305, 995),
        ),
    )),
    # blueprint/left/BPLeft.BPGlobalVariablesNodeList reads currentManager.globalVariableManager
    # and filters by key. Used variable IDs cannot be dragged again; usedNodes is populated
    # across pages in BluePrintManager.init. BPGlobalVariableNodeController declares input
    # 更新数据 and output 数据变更时; execute sets the existing variable's value.
    "blueprint-variables": ("blueprint-overview", (
        RuleCard(
            "先创建变量，再切到这里使用",
            ("主设计器创建变量后，点左侧 { } 切换列表。", "拖入变量节点，从「更新数据」输入新值。", "从「数据变更时」输出连接后续动作。"),
            "这里引用已有变量，不是新建变量的入口。",
            (430, 85, 1150, 375), (44, 227), ((23, 186, 65, 227),), ((400, 230), (400, 205)), badge=(80, 205),
        ),
        RuleCard(
            "按变量名搜索，重复使用先找已有节点",
            ("切到变量列表后，可按变量名称筛选。", "同一变量已拖入时，不能再重复拖入一份。"),
            "新建蓝图页面，也不能绕过同一变量的重复限制。",
            (1210, 85, 1860, 355), (351, 155), ((99, 137, 351, 173),), ((1180, 60), (390, 60), (390, 155)), badge=(386, 155),
        ),
    )),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", nargs="?", type=Path, default=SOURCE_DIR)
    args = parser.parse_args()
    for name, (source_name, cards) in SPECS.items():
        destination = render(name, cards, source_dir=args.source_dir, source_name=source_name)
        print(destination)


if __name__ == "__main__":
    main()
