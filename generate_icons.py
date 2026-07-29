import struct, zlib, math, os

OUT_DIR = os.path.join(os.path.dirname(__file__), "icons")

def lerp(a, b, t):
    return a + (b - a) * t

def bg_color(x, y, size):
    # warm diagonal gradient: deep coral -> golden orange
    t = (x + y) / (2 * size)
    r = lerp(0xFF, 0xFF, t)
    g = lerp(0x6B, 0xA6, t)
    b = lerp(0x4A, 0x1B, t)
    return int(r), int(g), int(b)

def make_icon(size, path, sun_scale=0.34, ray=True):
    cx, cy = size / 2, size / 2
    sun_r = size * sun_scale
    pixels = bytearray()
    for y in range(size):
        row = bytearray()
        for x in range(size):
            r, g, b = bg_color(x, y, size)
            dx, dy = x - cx, y - cy
            dist = math.hypot(dx, dy)
            # sun disc (soft white with slight yellow tint), anti-aliased edge
            edge = sun_r
            if dist < edge:
                aa = min(1.0, (edge - dist) / 2.0)
                sr, sg, sb = 255, 250, 235
                r = int(lerp(r, sr, aa))
                g = int(lerp(g, sg, aa))
                b = int(lerp(b, sb, aa))
            elif ray:
                # rays: 8 soft spokes
                ang = math.atan2(dy, dx)
                spoke = abs(math.sin(ang * 4))
                ray_outer = sun_r * 1.9
                if dist < ray_outer and spoke > 0.86:
                    fall = 1.0 - (dist - sun_r) / (ray_outer - sun_r)
                    fall = max(0.0, fall) * (spoke - 0.86) / 0.14
                    sr, sg, sb = 255, 250, 235
                    r = int(lerp(r, sr, fall * 0.9))
                    g = int(lerp(g, sg, fall * 0.9))
                    b = int(lerp(b, sb, fall * 0.9))
            row += bytes((r, g, b, 255))
        pixels += row
    write_png(path, size, size, pixels)

def write_png(path, width, height, rgba_bytes):
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    raw = bytearray()
    stride = width * 4
    for y in range(height):
        raw.append(0)
        raw += rgba_bytes[y * stride:(y + 1) * stride]
    idat = zlib.compress(bytes(raw), 9)
    with open(path, "wb") as f:
        f.write(sig)
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", idat))
        f.write(chunk(b"IEND", b""))

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    make_icon(192, os.path.join(OUT_DIR, "icon-192.png"))
    make_icon(512, os.path.join(OUT_DIR, "icon-512.png"))
    make_icon(180, os.path.join(OUT_DIR, "apple-touch-icon.png"), sun_scale=0.38, ray=False)
    print("done")
