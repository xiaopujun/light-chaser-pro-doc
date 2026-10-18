#!/usr/bin/env python3
"""Annotate 1920x1080 WebP screenshots without resizing them."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from annotation_rules import RuleCard, render


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = REPO_ROOT / "docs/assets/web-2026-10/originals"
OUTPUT_DIR = REPO_ROOT / "docs/assets/web-2026-10"
EXPECTED_SIZE = (1920, 1080)
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
NUMBER_FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"
WHITE = (242, 250, 255, 255)


@dataclass(frozen=True)
class RuleCallout:
    title: str
    lines: tuple[str, ...]
    caution: str
    box: tuple[int, int, int, int]
    control: tuple[int, int, int, int]
    badge: tuple[int, int]
    leader: tuple[tuple[int, int], ...]


# Explain decisions and their consequences, rather than renaming controls.
# Rules checked against ReleaseHdConfigImpl.tsx and ProjectReleaseServiceImpl.java.
PUBLISH_RULES = (
    RuleCallout(
        title="更新旧版本，还是另存一版？",
        lines=(
            "覆盖：沿用最近更新的发布链接，替换内容。",
            "增量：创建新链接，已有发布保留。",
            "首次发布没有旧记录时，会新建链接。",
        ),
        caution="要保留旧版本，就选增量，不要选覆盖。",
        box=(52, 314, 650, 556),
        control=(731, 433, 1189, 472),
        badge=(713, 453),
        leader=((650, 435), (680, 435), (680, 453), (713, 453), (731, 453)),
    ),
    RuleCallout(
        title="开启后，还必须填写访问密码",
        lines=(
            "打开开关后，会出现密码输入框。",
            "访问者通过该密码验证后，才能加载发布页。",
        ),
        caution="只开开关、密码留空，无法发布。",
        box=(1270, 360, 1868, 570),
        control=(1121, 508, 1175, 540),
        badge=(1206, 524),
        leader=((1270, 464), (1240, 464), (1240, 524), (1206, 524), (1175, 524)),
    ),
    RuleCallout(
        title="临时分享填天数，长期访问留空",
        lines=(
            "填 7：本次发布后有效 7 天，到期不能访问。",
            "留空：永久有效；填写时最少为 1 天。",
        ),
        caution="永久有效请留空，不要用 0 代替。",
        box=(1270, 610, 1868, 820),
        control=(731, 604, 1189, 642),
        badge=(1206, 623),
        leader=((1270, 712), (1240, 712), (1240, 623), (1206, 623), (1189, 623)),
    ),
    RuleCallout(
        title="确认范围后，再点“发布项目”",
        lines=(
            "发布对象是主项目及其关联内容。",
            "即使正在编辑子项目，也会发布主项目。",
        ),
        caution="不能把它当成“只发布当前子项目”。",
        box=(52, 626, 650, 836),
        control=(1083, 739, 1190, 778),
        badge=(1136, 818),
        leader=((650, 733), (674, 733), (674, 818), (1136, 818), (1136, 778)),
    ),
)


# Rule text is checked against the documentation and implementation at:
# - Overview: docs/functions/main_desiner/main_designer.md; frontend/lcp-web-app/src/designer/header/DesignerHeader.tsx
# - AI: docs/functions/main_desiner/ai_fusion.md; frontend/lcp-web-app/src/designer/ai-driven/AiDrivenBar.tsx and AiDrivenBarStore.ts
# - AI settings: frontend/lcp-web-app/src/designer/ai-driven/AiDrivenSettingsPanel.tsx
# - Canvas: docs/functions/main_desiner/canvas.md; frontend/lcp-web-app/src/designer/header/items/canvas/CanvasHdConfigImpl.tsx
# - Components: docs/functions/main_desiner/component_lib.md; frontend/lcp-web-app/src/designer/left/compoent-lib/ComponentList.tsx
# - Data: docs/quick_start/quick_start.md; frontend/lcp-web-app/src/comps/common-component/data-source-config/StaticDataConfig.tsx
# - Layers: docs/functions/main_desiner/layer.md; frontend/lcp-web-app/src/designer/left/layer-list/LayerList.tsx and frontend/lcp-web-app/src/designer/operate-provider/undo-redo/HistoryRecordOperateProxy.ts
# - Project menu: docs/functions/main_desiner/save.md; frontend/lcp-web-app/src/designer/header/DesignerHeader.tsx and frontend/lcp-web-app/src/designer/loader/EditDesignerLoader.ts
# - Preview: docs/functions/main_desiner/view/preview.md; frontend/lcp-web-app/src/designer/header/DesignerHeader.tsx
# - Project creation: docs/quick_start/quick_start.md; frontend/lcp-web-app/src/pages/home/project-list/NewProjectDialog.tsx
RULE_CARDS: dict[str, tuple[RuleCard, ...]] = {
    # General workspace flow; scenario-specific overview variants are handled separately.
    "designer-overview": (
        RuleCard(
            title="先看顶栏保存状态",
            lines=(
                "顶部显示保存中、已保存时间或失败；失败可点状态重试。",
                "点击预览前会先保存，保存失败则不打开。",
            ),
            note="底部项目、场景信息不代表服务器已经保存。",
            box=(1555, 70, 1910, 480),
            target=(1648, 36),
            frames=((1642, 24, 1733, 49),),
            via=((1550, 65), (1550, 36)),
            badge=(1610, 36),
        ),
        RuleCard(
            title="双击画布对象再配置",
            lines=(
                "在中央画布放置、编辑组件。",
                "双击组件打开右侧配置。",
            ),
            note="可用设置随组件类型变化，不要套用其他组件选项。",
            box=(1555, 665, 1910, 995),
            target=(1518, 800),
        ),
    ),
    # Both selectors are required by submitPrompt; preview drafts require explicit confirmation.
    "designer-ai": (
        RuleCard(
            title="提交前先配齐两项",
            lines=(
                "先选模型配置和模型型号；两项都必填。",
                "列表为空时，先检查模型管理中的可用配置。",
            ),
            note="需求文本不能为空。",
            box=(70, 718, 455, 1020),
            target=(496, 900),
            frames=((496, 875, 615, 923), (616, 875, 735, 923)),
            badge=(475, 900),
        ),
        RuleCard(
            title="需要预览时，确认后才写入",
            lines=(
                "发送后可查看任务步骤；部分任务会先展示临时画布结果。",
                "检查预览符合预期后，再确认应用修改。",
            ),
            note="不符合预期时拒绝预览，正式画布不会应用这次草稿。",
            box=(1300, 90, 1840, 350),
            target=(957, 289),
            frames=((253, 289, 957, 710),),
            via=((1290, 180), (1100, 180), (1100, 270)),
            badge=(990, 270),
        ),
    ),
    # The displayed threshold is the current screenshot value; compaction does not reset task usage.
    "designer-ai-settings": (
        RuleCard(
            title="本次设置：窗口达到 90% 时压缩",
            lines=(
                "按自上次成功压缩后的累计模型 Token 计算。",
                "成功压缩后，这项计数重新开始。",
            ),
            note="任务累计 Token 用量不会因此重置。",
            box=(1240, 220, 1840, 480),
            target=(1202, 373),
            frames=((536, 355, 1202, 390),),
            via=((1225, 345), (1225, 373)),
            badge=(1215, 410),
        ),
        RuleCard(
            title="Token 预算开关约束新任务",
            lines=(
                "开启后，新任务达到累计 Token 上限会停止，并可显式续跑。",
                "已运行任务继续使用启动时的配置。",
            ),
            note="保存设置后，改动从后续新任务开始生效。",
            box=(1240, 515, 1840, 790),
            target=(1078, 543),
            frames=((534, 512, 1202, 574),),
            via=((1225, 650), (1225, 543)),
            badge=(1215, 600),
        ),
    ),
    # Adaptation modes and rasterize behavior are described in the canvas settings implementation.
    "designer-canvas": (
        RuleCard(
            title="按目标屏幕选择适配方式",
            lines=(
                "自适应保持比例；撑满宽或高时，另一方向可能滚动。",
                "撑满全屏会分别适配宽高，画布比例可能改变。",
            ),
            note="无自适应按画布原尺寸显示。",
            box=(55, 245, 500, 520),
            target=(637, 555),
            frames=((637, 537, 1283, 575),),
            via=((600, 375), (600, 555)),
            badge=(600, 555),
        ),
        RuleCard(
            title="栅格化控制拖拽与缩放步长",
            lines=(
                "开启后，移动和缩放会按各自步长对齐。",
                "关闭时不会显示这两项步长输入。",
            ),
            note="底部磁铁是另一项吸附开关。",
            box=(1320, 300, 1840, 580),
            target=(1234, 618),
            frames=((967, 594, 1283, 660),),
            via=((1310, 445), (1310, 618)),
            badge=(1300, 618),
        ),
    ),
    # Search/category filter the library; drag/drop and double-click have distinct insertion behavior.
    "designer-components": (
        RuleCard(
            title="先用搜索或分类缩小列表",
            lines=(
                "按名称搜索，或切换类别定位目标组件。",
                "再从列表中选择要添加的组件。",
            ),
            note="筛选只改变列表，不会改动画布内容。",
            box=(800, 730, 1380, 1010),
            target=(96, 170),
            frames=((95, 154, 352, 196), (95, 201, 352, 239)),
            via=((70, 715), (70, 170)),
            badge=(70, 170),
        ),
        RuleCard(
            title="拖到画布内再松开",
            lines=(
                "拖拽卡片后，在画布范围内松开可按目标位置添加。",
                "双击卡片会添加到画布坐标原点。",
            ),
            note="拖到画布外松开，不会添加组件。",
            box=(1460, 420, 1905, 700),
            target=(1515, 790),
            frames=((168, 265, 354, 372),),
        ),
    ),
    # StaticDataConfig writes only through Save; mapping is conditional on the component definition.
    "designer-config": (
        RuleCard(
            title="先测试草稿，结果先看响应区",
            lines=(
                "测试会应用当前静态数据和过滤器。",
                "从「响应结果」检查返回的数据结构。",
            ),
            note="测试不会保存配置；改动后还要单独保存。",
            box=(390, 730, 970, 1000),
            target=(1494, 952),
            frames=((1493, 934, 1647, 971), (1658, 934, 1812, 971)),
            via=((980, 720), (1480, 720), (1480, 952)),
        ),
        RuleCard(
            title="数据字段还要映射到组件",
            lines=(
                "在「映射」中绑定返回字段。",
                "先核对响应，再调整字段对应。",
            ),
            note="不支持映射的组件不会显示此入口。",
            box=(990, 730, 1450, 1000),
            target=(1880, 228),
            frames=((1858, 208, 1904, 249),),
            via=((1475, 720), (1830, 720), (1830, 228)),
            badge=(1830, 228),
        ),
    ),
    # Dragging into a target inherits its parent; only self/descendant loops are rejected.
    "designer-layers": (
        RuleCard(
            title="拖到目标前后可排序或换组",
            lines=(
                "拖动手柄，把条目放到目标行前或后。",
                "源图层会进入目标所在的列表。",
            ),
            note="不要把分组拖进自身或后代。",
            box=(380, 730, 950, 1000),
            target=(104, 252),
            frames=((86, 234, 355, 271),),
            via=((70, 720), (70, 252), (86, 252)),
            badge=(69, 252),
        ),
        RuleCard(
            title="右侧操作可改名、隐藏、锁定",
            lines=(
                "隐藏会让组件在画布中不可见。",
                "锁定后，组件不能移动或缩放。",
            ),
            note="取消锁定后，才能继续移动或缩放。",
            box=(990, 730, 1550, 1000),
            target=(341, 252),
            frames=((271, 239, 352, 265),),
            via=((1555, 720), (1555, 252), (385, 252)),
            badge=(385, 252),
        ),
    ),
    # Server save and local recovery are separate paths. HotKeyImpl.exportProject/importProject
    # use ZIP; export secret validation requires encryption for common API/database references.
    "designer-project-menu": (
        RuleCard(
            title="“保存项目”写入服务器",
            lines=(
                "从此菜单手动保存后，顶部显示保存状态和时间。",
                "也可使用当前平台的保存快捷键。",
            ),
            note="浏览器快照仅用于本地恢复，不等同服务器保存。",
            box=(80, 735, 650, 1000),
            target=(1748, 84),
            frames=((1730, 65, 1903, 104),),
            via=((650, 700), (1670, 700), (1670, 84)),
            badge=(1710, 84),
        ),
        RuleCard(
            title="本地快照只用于恢复",
            lines=(
                "当前浏览器每 5 分钟记录一次，最多保留 10 条。",
                "从此菜单打开列表并选择要恢复的快照。",
            ),
            note="恢复后要手动保存，才会更新服务器项目。",
            box=(670, 735, 1240, 1000),
            target=(1748, 244),
            frames=((1730, 225, 1903, 263),),
            via=((1240, 680), (1690, 680), (1690, 244)),
            badge=(1710, 244),
        ),
        RuleCard(
            title="跨设备迁移，用 ZIP 项目包",
            lines=(
                "含公共 API 或数据库时，必须加密导出。",
                "导入会将包内项目数据写入当前项目。",
            ),
            note="导入加密包须使用原导出口令。",
            box=(1260, 735, 1830, 1000),
            target=(1748, 165),
            frames=((1730, 112, 1903, 185),),
            via=((1830, 660), (1710, 660), (1710, 165)),
            badge=(1710, 165),
        ),
    ),
    # The preview action saves first; the opened page uses the saved project and environment resources.
    "designer-preview": (
        RuleCard(
            title="进入预览前会先保存",
            lines=(
                "Web 端保存成功后，才会继续打开新标签页预览。",
                "保存失败时不会进入预览。",
            ),
            note="若没有打开预览，检查浏览器是否拦截新标签页。",
            box=(80, 855, 950, 1060),
            target=(250, 95),
            frames=((252, 72, 508, 124),),
            via=((60, 825), (60, 95)),
            badge=(215, 95),
        ),
        RuleCard(
            title="预览读取已保存项目",
            lines=(
                "画面按画布尺寸、屏幕适配和全局滤镜展示。",
                "用于检查保存后的展示效果。",
            ),
            note="数据源和第三方资源取决于预览环境能否访问。",
            box=(990, 750, 1850, 950),
            target=(1618, 550),
            via=((1665, 730),),
            badge=(1655, 650),
        ),
    ),
    # Defaults, limits, and optional description match NewProjectDialog controls.
    "project-create": (
        RuleCard(
            title="先命名，再补充描述",
            lines=(
                "项目名称最多 50 字。",
                "描述最多 200 字，可以留空。",
            ),
            note="默认名称是「未命名项目」。",
            box=(45, 300, 455, 600),
            target=(804, 435),
            frames=((804, 415, 1402, 454), (804, 501, 1404, 614)),
            via=((470, 435), (770, 435)),
            badge=(770, 435),
        ),
        RuleCard(
            title="画布默认 1920 × 1080",
            lines=(
                "可按设计需要修改宽、高；两项最小值均为 300 px。",
                "宽高分别设置，不需要保持固定比例。",
            ),
            note="宽或高低于 300 px 时不能创建。",
            box=(1460, 610, 1905, 920),
            target=(1390, 679),
            frames=((804, 659, 1095, 700), (1112, 659, 1402, 700)),
            badge=(1430, 679),
        ),
    ),
}


def draw_publish_rules(draw: ImageDraw.ImageDraw) -> None:
    heading_font = ImageFont.truetype(FONT_PATH, 31)
    title_font = ImageFont.truetype(FONT_PATH, 26)
    body_font = ImageFont.truetype(FONT_PATH, 23)
    number_font = ImageFont.truetype(NUMBER_FONT_PATH, 22)
    muted = (202, 216, 232, 255)
    amber = (255, 205, 126, 255)
    accent = (95, 218, 235, 255)

    def wrap(text: str, width: int) -> list[str]:
        result: list[str] = []
        line = ""
        for character in text:
            if line and draw.textlength(line + character, font=body_font) > width:
                result.append(line)
                line = character
            else:
                line += character
        if line:
            result.append(line)
        return result

    draw.text((52, 205), "发布前，先确认选择会带来什么结果", font=heading_font, fill=WHITE)
    draw.text((52, 251), "入口：设计器右上角 → 发布。按 1—4 检查后提交。", font=body_font, fill=muted)
    for number, rule in enumerate(PUBLISH_RULES, start=1):
        draw.line(rule.leader, fill=accent, width=3, joint="curve")
        draw.rounded_rectangle(rule.control, radius=8, outline=accent, width=2)

        left, top, right, bottom = rule.box
        draw.rounded_rectangle(
            rule.box, radius=14, fill=(10, 22, 39, 250),
            outline=(71, 109, 133, 255), width=2,
        )
        draw.line((left + 20, top + 18, left + 20, top + 48), fill=accent, width=4)
        draw.text((left + 35, top + 17), f"{number}  {rule.title}", font=title_font, fill=WHITE)
        y = top + 66
        for paragraph in rule.lines:
            for line in wrap(paragraph, right - left - 48):
                draw.text((left + 24, y), line, font=body_font, fill=muted)
                y += 34
        y += 12
        draw.line((left + 24, y - 8, right - 24, y - 8), fill=(49, 72, 94, 255), width=1)
        for line in wrap(rule.caution, right - left - 48):
            draw.text((left + 24, y), line, font=body_font, fill=amber)
            y += 34
        if y > bottom - 12:
            raise ValueError(f"Publish rule {number} overflows its annotation box")

        x, y = rule.badge
        draw.ellipse((x - 17, y - 17, x + 17, y + 17), fill=(15, 63, 82, 255), outline=accent, width=2)
        draw.text((x, y), str(number), anchor="mm", font=number_font, fill=WHITE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="folder containing the original 1920x1080 designer WebP screenshots",
    )
    return parser.parse_args()


def annotate_publish(source_dir: Path, output_dir: Path) -> Path:
    name = "designer-publish"
    src = source_dir / f"{name}.webp"
    with Image.open(src) as original:
        if original.size != EXPECTED_SIZE:
            raise ValueError(
                f"expected {name} source to be 1920x1080; got {original.size} at {src}. "
                "The source is not resized or cropped."
            )
        image = original.convert("RGBA")

    overlay = Image.new("RGBA", EXPECTED_SIZE, (0, 0, 0, 0))
    draw_publish_rules(ImageDraw.Draw(overlay))
    result = Image.alpha_composite(image, overlay).convert("RGB")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / f"{name}.webp"
    result.save(destination, format="WEBP", lossless=True, method=6)
    with Image.open(destination) as saved:
        if saved.size != EXPECTED_SIZE:
            raise AssertionError(f"bad output size for {destination}: {saved.size}")
    return destination


def main() -> None:
    args = parse_args()
    source_dir = args.source_dir
    if not source_dir.is_absolute():
        source_dir = REPO_ROOT / source_dir

    for name, cards in RULE_CARDS.items():
        destination = render(name, cards, source_dir=source_dir, output_dir=OUTPUT_DIR)
        print(f"{destination}: {EXPECTED_SIZE}")

    destination = annotate_publish(source_dir, OUTPUT_DIR)
    print(f"{destination}: {EXPECTED_SIZE}")


if __name__ == "__main__":
    main()
