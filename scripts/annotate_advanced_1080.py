#!/usr/bin/env python3
"""Annotate four advanced-guide WebP screenshots at native 1920x1080 size."""

from __future__ import annotations

import argparse
from pathlib import Path

from annotation_rules import OUTPUT_DIR, SOURCE_DIR, RuleCard, render


REPO_ROOT = Path(__file__).resolve().parents[1]
IMAGE_NAMES = (
    "blueprint-overview",
    "blueprint-functions",
    "loop-config",
    "loop-return",
)


# Evidence checked against /Users/yinzhenpu/projects/lcp-web:
# - Event/action anchors and their direction: frontend/lcp-web-app/src/designer/blueprint/node/core/impl/layer/BPLayerNodeController.ts:60-84;
#   connections start at an output and end at an input in frontend/lcp-web-app/src/designer/blueprint/line/LineLayer.tsx:346-390.
# - Node configuration and execution: frontend/lcp-web-app/src/designer/blueprint/right/BPRight.tsx:76-110;
#   condition and logic handlers are in .../condition/BPConditionNodeController.ts:42-64 and .../logical-process/BPLogicalProcessNodeController.ts:42-64.
#   WebSocket and MQTT forms are in .../websocket/WebSocketNodeConfig.tsx:18-32, .../common-component/data-source-config/WebSocketConfig.tsx:44-60,
#   .../mqtt/MqttNodeConfig.tsx:18-32, and .../common-component/data-source-config/MQTTConfig.tsx:48-90.
# - The main canvas has the selected loop component: frontend/lcp-web-app/src/designer/operate-provider/hot-key/HotKeyImpl.ts:983-1005;
#   the internal manager layout is serialized by .../comps/loop-container/LoopContainerController.ts:255-260.
# - Loop data is array-based and carousel is gated by mode, enableCarousel, and dataLength > 1:
#   frontend/lcp-web-app/src/comps/loop-container/LoopContainerController.ts:115-133, 284-307.
# - Layout controls and carousel disabling wrap/overflow are in frontend/lcp-web-app/src/comps/loop-container/LoopContainerConfig.tsx:32-129.
# - Returning only switches managers: frontend/lcp-web-app/src/designer/operate-provider/hot-key/HotKeyImpl.ts:1011-1027;
#   saving serializes currentFinalManager in .../HotKeyImpl.ts:96-107, and ManagerStore keeps the parent as currentFinalManager for loop editing at .../manager/ManagerStore.ts:50-70.


CARDS: dict[str, tuple[RuleCard, ...]] = {
    "blueprint-overview": (
        RuleCard(
            title="从事件输出连到动作输入",
            lines=(
                "本例把“点击整个组件时”输出，接到目标组件的“显示”输入。",
                "事件触发后，蓝图沿连线方向执行后续动作。",
            ),
            note="连线从输出锚点拖到输入锚点。",
            box=(1270, 250, 1870, 545),
            target=(914, 408),
            frames=((775, 365, 801, 391), (1035, 423, 1062, 449)),
            via=((1255, 396), (1135, 396)),
        ),
        RuleCard(
            title="先检查节点，再验证流程",
            lines=(
                "双击节点查看它支持的锚点与配置；组件提供的事件和动作各不相同。",
                "保存项目后进入预览，实际触发事件检查执行结果。",
            ),
            note="没有触发组件事件时，连线流程不会启动。",
            box=(390, 700, 1040, 1000),
            target=(630, 289),
            frames=((647, 260, 808, 646),),
            via=((630, 670),),
        ),
    ),
    "blueprint-functions": (
        RuleCard(
            title="条件与逻辑节点要配置处理函数",
            lines=(
                "条件判断用函数选择“满足/不满足”；逻辑处理把返回值交给后续节点。",
                "双击节点，在右侧配置区编辑函数。",
            ),
            note="缺少处理函数时，节点不会继续执行分支或后续动作。",
            box=(800, 165, 1820, 450),
            target=(385, 316),
            frames=((96, 294, 356, 340),),
            via=((760, 145), (385, 145)),
        ),
        RuleCard(
            title="通信节点先填连接信息",
            lines=(
                "WebSocket 要设置服务 URL；MQTT 要填写 Host、端口和主题等连接信息。",
                "配置入口在双击节点后的右侧面板。",
            ),
            note="服务必须能从浏览器连接，否则无法正常收发数据。",
            box=(800, 500, 1820, 815),
            target=(385, 443),
            frames=((96, 393, 356, 487),),
            via=((760, 890), (385, 890)),
        ),
    ),
    "loop-config": (
        RuleCard(
            title="一份模板，按数组逐项复用",
            lines=("循环容器内部布局会按数据数组的每一项生成实例。",),
            note="数据须为数组，模板用首项预览。",
            box=(470, 770, 935, 1000),
            target=(915, 540),
            frames=((934, 394, 1405, 689),),
            via=((930, 748), (915, 700)),
        ),
        RuleCard(
            title="布局与轮播开关",
            lines=("横/纵布局和间距控制排列；轮播可设方向、速度和停顿。",),
            note="至少两条数据才轮播；开启后换行、溢出选项停用。",
            box=(950, 770, 1410, 1000),
            target=(1855, 386),
            frames=((1593, 369, 1657, 405), (1594, 428, 1804, 565), (1594, 585, 1804, 785)),
            via=((1418, 1005), (1840, 1005), (1840, 386)),
        ),
    ),
    "loop-return": (
        RuleCard(
            title="“返回主项目”只退出模板编辑",
            lines=("退出内部模板，回到主画布继续编辑。",),
            note="返回不会自动把修改保存到服务器。",
            box=(480, 660, 1090, 955),
            target=(1690, 92),
            frames=((1708, 68, 1904, 117),),
            via=((1100, 630), (1650, 630), (1650, 92)),
        ),
        RuleCard(
            title="返回后保存整个项目",
            lines=("保存整个项目，会同时保存内部模板。",),
            note="编辑模板后：返回主项目 → 保存项目。",
            box=(1105, 660, 1700, 955),
            target=(1690, 141),
            frames=((1708, 117, 1904, 168),),
            via=((1690, 630), (1690, 300)),
        ),
    ),
}


HEADINGS = {
    "blueprint-overview": (
        "让组件事件驱动目标动作",
        "输出锚点 → 输入锚点；保存后在预览触发事件验证。",
        (420, 72),
    ),
    "blueprint-functions": (
        "功能节点按类型配置",
        "处理函数、连接信息和可用锚点由节点类型决定。",
        (420, 72),
    ),
    "loop-return": (
        "循环模板编辑完成后，返回并保存",
        "返回只退出内部画布；保存项目才会把修改写入服务器。",
        (480, 175),
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source_dir",
        nargs="?",
        type=Path,
        default=SOURCE_DIR,
        help="directory containing the original 1920x1080 WebP captures",
    )
    return parser.parse_args()


def main() -> None:
    source_dir = parse_args().source_dir
    if not source_dir.is_absolute():
        source_dir = REPO_ROOT / source_dir

    for name in IMAGE_NAMES:
        title, subtitle, heading_at = HEADINGS.get(name, ("", "", (52, 190)))
        destination = render(
            name,
            CARDS[name],
            title=title,
            subtitle=subtitle,
            heading_at=heading_at,
            source_dir=source_dir,
            output_dir=OUTPUT_DIR,
        )
        print(f"{destination}: 1920x1080")


if __name__ == "__main__":
    main()
