# Food picture: a ramen bowl with steam, drawn with the standard library only (zlib + struct PNG writer).
import math, os, random, struct, zlib
W = H = 1024
buf = bytearray(W * H * 3)

def put(x, y, c, a=1.0):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        if a >= 1.0:
            buf[i:i + 3] = bytes(c)
        else:
            for k in range(3):
                buf[i + k] = int(buf[i + k] * (1 - a) + c[k] * a)

def ell(cx, cy, rx, ry, c, a=1.0, inner=0.0):
    for y in range(max(0, int(cy - ry)), min(H, int(cy + ry) + 1)):
        for x in range(max(0, int(cx - rx)), min(W, int(cx + rx) + 1)):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if inner <= d <= 1.0:
                put(x, y, c, a)

def rect(x0, y0, x1, y1, c, rad=0):
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            put(x, y, c)

def dot_line(pts, r, c, a=1.0):
    for x0, y0 in pts:
        ell(x0, y0, r, r, c, a)

def png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += buf[y * W * 3:(y + 1) * W * 3]
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)

random.seed(7)
# warm vignette background
for y in range(H):
    for x in range(W):
        d = min(1.0, math.hypot((x - W / 2) / (W / 2), (y - H / 2) / (H / 2)) / 1.2)
        i = (y * W + x) * 3
        buf[i:i + 3] = bytes((int(236 * (1 - d) + 70 * d), int(214 * (1 - d) + 40 * d), int(180 * (1 - d) + 25 * d)))
ell(512, 720, 327, 150, (30, 15, 8), 0.55)          # shadow
ell(512, 655, 352, 225, (245, 245, 240))             # bowl rim
ell(512, 645, 322, 185, (200, 60, 40))               # red band
ell(512, 630, 297, 170, (214, 140, 50))              # broth
ell(512, 630, 272, 140, (232, 170, 80))
for i in range(60):                                  # noodles
    cx, cy = random.uniform(330, 690), random.uniform(580, 690)
    pts = [(cx + 26 * math.cos(k / 11 * 6.283 + i) + random.uniform(-3, 3),
            cy + 8 * math.sin(2 * k / 11 * 6.283 + i)) for k in range(12)]
    dot_line(pts, 4, (246, 214, 120))
for ex, ey in [(400, 585), (610, 615)]:              # soft-boiled eggs
    ell(ex, ey, 62, 46, (255, 255, 250))
    ell(ex, ey, 30, 22, (255, 150, 30))
for sx, sy in [(330, 690), (520, 700), (690, 650)]:  # chashu
    ell(sx, sy, 60, 28, (160, 60, 40))
    ell(sx, sy, 48, 18, (200, 110, 80))
rect(560, 470, 640, 540, (20, 40, 25))               # nori
for _ in range(40):                                  # spring onion rings
    cx, cy = random.uniform(330, 690), random.uniform(560, 650)
    ell(cx, cy, 8, 8, (120, 200, 90), 1.0, inner=0.5)
for k in range(0, 500, 3):                           # chopsticks
    t = k / 500
    dot_line([(120 + 500 * t, 250 + 270 * t)], 9, (150, 90, 40))
for sx in (380, 500, 620):                           # steam
    pts = [(sx + 25 * math.sin(t / 18.0), 420 - t) for t in range(0, 200, 5)]
    dot_line(pts, 10, (255, 255, 255), 0.35)
png("/output/entry.png")
