"""Draw instructional callouts on native 1920x1080 WebP documentation captures."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO_ROOT / "docs/assets/web-2026-10/originals"
OUTPUT_DIR = REPO_ROOT / "docs/assets/web-2026-10"
SIZE = (1920, 1080)
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
NUMBER_FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"
WHITE = (242, 250, 255, 255)
MUTED = (202, 216, 232, 255)
ACCENT = (95, 218, 235, 255)
AMBER = (255, 205, 126, 255)

Point = tuple[int, int]
Rect = tuple[int, int, int, int]


@dataclass(frozen=True)
class RuleCard:
    title: str
    lines: tuple[str, ...]
    note: str
    box: Rect
    target: Point
    frames: tuple[Rect, ...] = ()
    via: tuple[Point, ...] = ()
    badge: Point | None = None


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    result: list[str] = []
    for paragraph in text.split("\n"):
        line = ""
        for character in paragraph:
            if line and draw.textlength(line + character, font=font) > width:
                result.append(line)
                line = character
            else:
                line += character
        result.append(line)
    return result


def edge_toward(box: Rect, point: Point) -> Point:
    left, top, right, bottom = box
    center_x, center_y = (left + right) / 2, (top + bottom) / 2
    dx, dy = point[0] - center_x, point[1] - center_y
    scale_x = (right - left) / 2 / abs(dx) if dx else float("inf")
    scale_y = (bottom - top) / 2 / abs(dy) if dy else float("inf")
    scale = min(scale_x, scale_y)
    if scale == float("inf"):
        return right, round(center_y)
    return round(center_x + dx * scale), round(center_y + dy * scale)


def validate(cards: tuple[RuleCard, ...]) -> None:
    for index, card in enumerate(cards):
        left, top, right, bottom = card.box
        if not (0 <= left < right <= SIZE[0] and 0 <= top < bottom <= SIZE[1]):
            raise ValueError(f"Card {index + 1} is outside the image: {card.box}")
        if not card.lines or not card.note:
            raise ValueError(f"Card {index + 1} needs a usage rule and a practical boundary")
        for point in (card.target, card.badge or card.target):
            x, y = point
            if not (18 <= x < SIZE[0] - 18 and 18 <= y < SIZE[1] - 18):
                raise ValueError(f"Card {index + 1} has a clipped target marker: {point}")
        for frame in card.frames:
            a, b, c, d = frame
            if not (0 <= a < c <= SIZE[0] and 0 <= b < d <= SIZE[1]):
                raise ValueError(f"Card {index + 1} has an invalid control frame: {frame}")
        for other_index, other in enumerate(cards):
            for x, y in (other.target, other.badge or other.target):
                if left - 18 <= x <= right + 18 and top - 18 <= y <= bottom + 18:
                    raise ValueError(f"Card {index + 1} hides target {other_index + 1}")
            if other_index <= index:
                continue
            a, b, c, d = other.box
            if max(left, a) < min(right, c) and max(top, b) < min(bottom, d):
                raise ValueError(f"Cards {index + 1} and {other_index + 1} overlap")


def render(
    name: str,
    cards: tuple[RuleCard, ...],
    *,
    title: str = "",
    subtitle: str = "",
    heading_at: Point = (52, 190),
    source_dir: Path = SOURCE_DIR,
    output_dir: Path = OUTPUT_DIR,
    source_name: str | None = None,
) -> Path:
    validate(cards)
    source = source_dir / f"{source_name or name}.webp"
    with Image.open(source) as original:
        if original.size != SIZE:
            raise ValueError(f"{source}: {original.size}; expected {SIZE}; no resizing allowed")
        image = original.convert("RGBA")
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    title_font = ImageFont.truetype(FONT_PATH, 26)
    body_font = ImageFont.truetype(FONT_PATH, 23)
    number_font = ImageFont.truetype(NUMBER_FONT_PATH, 22)
    heading_font = ImageFont.truetype(FONT_PATH, 31)

    # Draw connectors first so each explanatory card remains legible.
    for card in cards:
        badge_point = card.badge or card.target
        start = edge_toward(card.box, card.via[0] if card.via else badge_point)
        points = (start, *card.via, badge_point, card.target) if card.badge else (start, *card.via, card.target)
        draw.line(points, fill=ACCENT, width=3, joint="curve")
        for frame in card.frames:
            draw.rounded_rectangle(frame, radius=8, outline=ACCENT, width=2)

    if title:
        draw.text(heading_at, title, font=heading_font, fill=WHITE)
    if subtitle:
        draw.text((heading_at[0], heading_at[1] + 45), subtitle, font=body_font, fill=MUTED)

    for number, card in enumerate(cards, start=1):
        left, top, right, bottom = card.box
        draw.rounded_rectangle(card.box, radius=14, fill=(10, 22, 39, 250), outline=(71, 109, 133, 255), width=2)
        draw.line((left + 20, top + 18, left + 20, top + 48), fill=ACCENT, width=4)
        heading_lines = wrap(draw, f"{number}  {card.title}", title_font, right - left - 58)
        y = top + 17
        for line in heading_lines:
            draw.text((left + 35, y), line, font=title_font, fill=WHITE)
            y += 36
        y += 13
        for paragraph in card.lines:
            for line in wrap(draw, paragraph, body_font, right - left - 48):
                draw.text((left + 24, y), line, font=body_font, fill=MUTED)
                y += 34
        y += 12
        draw.line((left + 24, y - 8, right - 24, y - 8), fill=(49, 72, 94, 255), width=1)
        for line in wrap(draw, card.note, body_font, right - left - 48):
            draw.text((left + 24, y), line, font=body_font, fill=AMBER)
            y += 34
        if y > bottom - 12:
            raise ValueError(f"{name} card {number} overflows by {y - bottom + 12}px: {card.title}")
        x, y = card.badge or card.target
        draw.ellipse((x - 17, y - 17, x + 17, y + 17), fill=(15, 63, 82, 255), outline=ACCENT, width=2)
        draw.text((x, y), str(number), anchor="mm", font=number_font, fill=WHITE)

    result = Image.alpha_composite(image, overlay).convert("RGB")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / f"{name}.webp"
    result.save(destination, format="WEBP", lossless=True, method=6)
    return destination
