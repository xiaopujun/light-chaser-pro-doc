"""Render rule-based annotations on the ten native home screenshots."""

from __future__ import annotations

import argparse
from pathlib import Path

from annotation_rules import OUTPUT_DIR, SOURCE_DIR, RuleCard, render


CARDS: dict[str, tuple[RuleCard, ...]] = {
    # Evidence: ConsoleDashboard.tsx builds resourceBreakdown links and limits both
    # recentActivities and recentReleases with slice(0, 5).
    "home-console": (
        RuleCard(
            title="资源概览可直接跳转",
            lines=("点击对应资源项，进入该类资源的管理页。",),
            note="概览汇总资源数量；要看具体记录，请进入对应管理页。",
            box=(255, 790, 920, 1035),
            target=(515, 455),
            frames=((255, 305, 1199, 642),),
        ),
        RuleCard(
            title="近期记录各显示最多 5 条",
            lines=("最近更新、最近发布分别按更新时间排序展示。",),
            note="点击面板右上角“查看全部”，继续查看完整列表。",
            box=(935, 790, 1600, 1035),
            target=(1544, 425),
            frames=((1213, 304, 1896, 642),),
        ),
    ),
    # Evidence: ProjectList.tsx submits search on Enter and sets page size to 6;
    # NewProjectDialog.tsx starts at 1920x1080 and enforces a 300px minimum.
    "home-projects": (
        RuleCard(
            title="搜索后按回车提交",
            lines=("输入项目关键词并按回车，列表会重新查询并分页。",),
            note="每页最多显示 6 个当前账号可访问的项目。",
            box=(1195, 145, 1895, 430),
            target=(1604, 44),
            frames=((1448, 24, 1768, 65),),
            badge=(1604, 100),
        ),
        RuleCard(
            title="新项目从这里开始",
            lines=("填写项目名称和画布尺寸后提交；创建成功会进入设计器。",),
            note="画布宽、高均至少 300 px；默认尺寸为 1920 × 1080。",
            box=(1195, 610, 1895, 965),
            target=(1837, 44),
            frames=((1784, 24, 1897, 65),),
            via=((1910, 580), (1910, 100)),
            badge=(1837, 100),
        ),
    ),
    # Evidence: DataBasePanel.tsx saves the switch; DataBaseList.tsx renders the
    # SQL-script tag and offers testConnect; DbExecutorServiceImpl.executeSql
    # unconditionally rejects statements not beginning with SELECT.
    "home-datasource": (
        RuleCard(
            title="先保存可复用连接",
            lines=("选择数据库类型，填写地址和账号信息后提交。",),
            note="保存后可在连接列表中测试连通性并管理配置。",
            box=(1550, 126, 1905, 482),
            target=(1473, 280),
            frames=((417, 228, 1504, 303),),
            badge=(1525, 280),
        ),
        RuleCard(
            title="SQL 开关的限制",
            lines=("开启后，连接卡片会显示 SQL 脚本标记。",),
            note="SQL 须以 SELECT 开头。\n此开关不保证支持写操作。",
            box=(1550, 510, 1905, 965),
            target=(1468, 649),
            frames=((417, 608, 1504, 690),),
            badge=(1525, 649),
        ),
    ),
    # Evidence: ApiEditPanel.tsx test() sends the current request and displays its
    # response; saveItem() is a separate action. The method selector is GET/POST.
    "home-api": (
        RuleCard(
            title="配置公共 API",
            lines=("填写名称、URL 和请求方式。", "请求头与参数用 JSON 编辑。"),
            note="仅支持 GET 或 POST；保存后可在项目数据配置中选择。",
            box=(1550, 126, 1905, 482),
            target=(1478, 330),
            frames=((531, 312, 1507, 353),),
            badge=(1525, 330),
        ),
        RuleCard(
            title="测试和创建分两步",
            lines=("“测试”会发送当前请求，并把响应显示在测试结果区。",),
            note="测试不会保存配置；确认后还要点击“创建”。",
            box=(1550, 510, 1905, 965),
            target=(1457, 933),
            frames=((1218, 912, 1508, 956),),
            badge=(1525, 885),
        ),
    ),
    # Evidence: AiModelEditPanel.tsx has a configuration name, provider/address
    # controls and preserves a saved key when blank; designer AI chooses a model ID separately.
    "home-ai-models": (
        RuleCard(
            title="先选提供商",
            lines=("为配置命名，再选择提供商。", "按所选提供商填写服务地址。"),
            note="具体型号在设计器 AI 面板中选择。",
            box=(1550, 126, 1905, 482),
            target=(1479, 275),
            frames=((409, 203, 1512, 296),),
            badge=(1525, 275),
        ),
        RuleCard(
            title="编辑时可更换 API Key",
            lines=("新建配置时按所选提供商的提示填写密钥。",),
            note="已保存的 Key 不会明文回显；编辑时留空会保留原值。",
            box=(1550, 510, 1905, 965),
            target=(1478, 456),
            frames=((428, 436, 1492, 478),),
            badge=(1525, 456),
        ),
    ),
    # Evidence: ResourceManagement.tsx routes to four separate resource areas;
    # FontManagement.tsx accepts five font extensions and limits the queue to 10.
    "home-resources": (
        RuleCard(
            title="按资源类型进入工作区",
            lines=("字体、动态脚本、视频和 3D 模型分别进入各自管理页。",),
            note="数据库、API、AI 模型和服务器组件有独立侧栏入口。",
            box=(270, 635, 930, 995),
            target=(106, 270),
            frames=((10, 218, 208, 408),),
            badge=(230, 270),
        ),
        RuleCard(
            title="字体上传格式与数量有限",
            lines=("点“上传字体”，选择 .ttf / .otf / .woff / .woff2 / .eot。",),
            note="每次最多加入 10 个文件；成功后刷新字体列表。",
            box=(970, 635, 1640, 995),
            target=(1744, 51),
            frames=((1691, 32, 1790, 71),),
            badge=(1744, 100),
        ),
    ),
    # Evidence: HomeMenus.tsx gates the user menu by SYSTEM_ADMIN; UserController
    # protects list/create/delete endpoints; UserServiceImpl searches only name.
    "home-users": (
        RuleCard(
            title="创建账号并分配角色",
            lines=("点“新建用户”，填写账号信息并选择角色后提交。",),
            note="仅系统管理员可管理用户账号和角色。",
            box=(255, 610, 1000, 995),
            target=(1758, 54),
            frames=((1706, 34, 1800, 73),),
            badge=(1758, 95),
        ),
        RuleCard(
            title="查找用户时，请按姓名搜索",
            lines=("当前搜索只匹配姓名。",),
            note="虽然输入提示包含用户名和邮箱，但这两项目前不会命中。",
            box=(1050, 610, 1895, 995),
            target=(1530, 53),
            frames=((1404, 34, 1697, 73),),
            badge=(1530, 95),
        ),
    ),
    # Evidence: Setting.tsx lists four sections and changes the app locale;
    # HomeMenus.tsx adds Settings only for SYSTEM_ADMIN; miniI18n.setLocale stores locally.
    "home-settings": (
        RuleCard(
            title="左侧菜单切换设置分区",
            lines=("账号、通用、品牌、关于分别显示对应设置内容。",),
            note="所有用户都可从底部账号菜单进入。\n侧栏独立入口仅系统管理员可见。",
            box=(270, 590, 1000, 965),
            target=(347, 183),
            frames=((252, 161, 448, 204),),
            badge=(475, 183),
        ),
        RuleCard(
            title="切换应用显示语言",
            lines=("在“通用”页选择简体中文或 English，应用界面随之切换。",),
            note="语言选择保存在当前浏览器；换浏览器需重新设置。",
            box=(1050, 590, 1885, 965),
            target=(1835, 258),
            frames=((1667, 239, 1835, 279),),
            badge=(1860, 258),
        ),
    ),
    # Evidence: ReleaseManagement.tsx has no creation action and shows an empty
    # state; ReleaseEditPanel.tsx edits expiry/encryption and requires a password.
    "home-releases": (
        RuleCard(
            title="此页维护已有发布记录",
            lines=("新建或更新发布内容，请回到设计器的发布流程。",),
            note="列表为空时没有可编辑的发布记录。",
            box=(255, 610, 1000, 980),
            target=(1065, 266),
            frames=((1024, 201, 1110, 280),),
        ),
        RuleCard(
            title="记录出现后再管理状态",
            lines=("行内可编辑有效期、设置访问密码或切换发布状态。",),
            note="有效期按天；启用加密时必须填写密码。",
            box=(1050, 610, 1895, 980),
            target=(1460, 127),
            frames=((240, 107, 1898, 150),),
            badge=(1460, 173),
        ),
    ),
    # Evidence: RemoteComponentManagement.tsx validates .js/.mjs/.zip, distinguishes
    # upload from replacement, and refreshes the component list after success.
    "home-components": (
        RuleCard(
            title="上传服务器组件文件",
            lines=("点“上传”，选择 .js、.mjs 或 .zip 文件并提交。",),
            note="上传会新增一条服务器组件记录。",
            box=(255, 610, 1000, 980),
            target=(1754, 54),
            frames=((1707, 34, 1796, 73),),
            badge=(1754, 95),
        ),
        RuleCard(
            title="替换更新已有组件",
            lines=("已有记录可改名、替换文件或删除；替换会更新原记录。",),
            note="删除前确认页面不再引用它，否则相关页面可能无法正常渲染。",
            box=(1050, 610, 1895, 980),
            target=(1067, 264),
            frames=((1010, 190, 1125, 282),),
        ),
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source_dir",
        nargs="?",
        type=Path,
        default=SOURCE_DIR,
        help="folder containing the original home-*.webp screenshots",
    )
    args = parser.parse_args()

    for name, cards in CARDS.items():
        destination = render(name, cards, source_dir=args.source_dir, output_dir=OUTPUT_DIR)
        print(destination)


if __name__ == "__main__":
    main()
