# Draws a bowl of ramen with steam and a sprinkle of toppings, writes /output/entry.png
import math, os, random
from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
random.seed(7)
img = Image.new("RGB", (W, H))
px = img.load()
# warm background: vignette from cream centre to dark wood edge
for y in range(H):
    for x in range(W):
        d = math.hypot((x - W/2) / (W/2), (y - H/2) / (H/2))
        t = min(1.0, d / 1.2)
        r = int(236 * (1 - t) + 70 * t)
        g = int(214 * (1 - t) + 40 * t)
        b = int(180 * (1 - t) + 25 * t)
        px[x, y] = (r, g, b)

layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
# bowl shadow and bowl
d.ellipse((150, 560, 874, 900), fill=(30, 15, 8, 140))
d.ellipse((160, 430, 864, 880), fill=(245, 245, 240, 255))
d.ellipse((190, 460, 834, 830), fill=(200, 60, 40, 255))
# broth
d.ellipse((215, 480, 809, 800), fill=(214, 140, 50, 255))
d.ellipse((240, 500, 784, 770), fill=(232, 170, 80, 255))
# noodles as wavy strokes
for i in range(60):
    cx = random.uniform(300, 720)
    cy = random.uniform(560, 700)
    pts = []
    for k in range(12):
        a = k / 11 * math.pi * 2
        pts.append((cx + math.cos(a + i) * 26 + random.uniform(-3, 3),
                    cy + math.sin(a * 2 + i) * 8))
    d.line(pts, fill=(246, 214, 120, 255), width=7, joint="curve")
# egg halves
for ex, ey in [(400, 560), (610, 600)]:
    d.ellipse((ex - 62, ey - 46, ex + 62, ey + 46), fill=(255, 255, 250, 255))
    d.ellipse((ex - 30, ey - 22, ex + 30, ey + 22), fill=(255, 150, 30, 255))
# chashu slices and nori
for sx, sy in [(330, 690), (520, 700), (690, 650)]:
    d.rounded_rectangle((sx - 60, sy - 28, sx + 60, sy + 28), 18, fill=(160, 60, 40, 255))
    d.rounded_rectangle((sx - 48, sy - 18, sx + 48, sy + 18), 12, fill=(200, 110, 80, 255))
d.polygon([(560, 470), (640, 470), (640, 540), (560, 540)], fill=(20, 40, 25, 255))
# green onion rings
for _ in range(40):
    cx, cy = random.uniform(300, 720), random.uniform(500, 650)
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), outline=(120, 200, 90, 255), width=3)
# chopsticks
d.line([(120, 250), (620, 520)], fill=(150, 90, 40, 255), width=18)
d.line([(150, 250), (650, 530)], fill=(170, 110, 60, 255), width=14)
layer = layer.filter(ImageFilter.GaussianBlur(1.2))
img = Image.alpha_composite(img.convert("RGBA"), layer)

# steam
steam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(steam)
for sx in (380, 500, 620):
    pts = [(sx + 25 * math.sin(t / 18.0), 420 - t) for t in range(0, 200, 4)]
    sd.line(pts, fill=(255, 255, 255, 150), width=18, joint="curve")
steam = steam.filter(ImageFilter.GaussianBlur(12))
img = Image.alpha_composite(img, steam)

os.makedirs("/output", exist_ok=True)
img.convert("RGB").save("/output/entry.png", "PNG", optimize=True)
