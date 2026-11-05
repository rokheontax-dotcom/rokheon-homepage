"""카톡·SNS에 링크를 보낼 때 보이는 공유 이미지(1200×630)를 만든다.

실행:  python 공유이미지_만들기.py   (이 폴더에서, Pillow 필요)
세무사법 시행령 제33조 제1항에 따라 사무소명과 세무사 성명을 함께 표시한다.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
W, H = 1200, 630
BLACK, CREAM_BG, GOLD, MUTED = "#111111", "#f2efe4", "#b8914a", "#5e5c55"


def font(size, weight):
    f = ImageFont.truetype(r"C:\Windows\Fonts\NotoSansKR-VF.ttf", size)
    f.set_variation_by_axes([weight])
    return f


# 작게 그린 뒤 줄이면 글자와 선의 가장자리가 매끄럽다.
S = 2
img = Image.new("RGB", (W * S, H * S), CREAM_BG)
d = ImageDraw.Draw(img)

# 메인 화면과 같은 검정 면 + 테두리 면
d.rectangle([700 * S, 170 * S, 1200 * S, 500 * S], fill=BLACK)
d.rectangle([640 * S, 300 * S, 1120 * S, 660 * S], outline=BLACK, width=3 * S)

# 대표 사진: 아래쪽 흐려지는 부분은 화면 밖으로 내보낸다.
person = Image.open(ROOT / "이미지/대표_메인.webp").convert("RGBA")
pw = 560 * S
person = person.resize((pw, round(person.height * pw / person.width)), Image.LANCZOS)
img.paste(person, (640 * S, 26 * S), person)

# 로고
logo = Image.open(ROOT / "이미지/로고_가로.png").convert("RGBA")
lw = 300 * S
logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
img.paste(logo, (64 * S, 60 * S), logo)

# 문구
y = 196
for line in ("법대 출신 세무사가", "처음부터 끝까지", "직접 상담합니다."):
    d.text((64 * S, y * S), line, font=font(60 * S, 900), fill=BLACK)
    y += 84

d.rectangle([64 * S, 468 * S, 124 * S, 472 * S], fill=GOLD)
d.text((64 * S, 490 * S), "대표 세무사 이훈성", font=font(30 * S, 700), fill=BLACK)
d.text((64 * S, 534 * S), "인천 서해구 · 032-545-4263", font=font(24 * S, 500), fill=MUTED)

img = img.resize((W, H), Image.LANCZOS)
out = ROOT / "이미지/공유이미지.jpg"
img.save(out, quality=88, optimize=True, progressive=True)
print(out, out.stat().st_size // 1024, "KB")
