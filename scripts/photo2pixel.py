"""
photo2pixel.py — 照片转像素数据
将任意照片缩放+颜色量化，输出 ai-painter 画板可用的像素矩阵。

用法:
  python photo2pixel.py <图片路径> --size 32 --colors 8

输出 JSON:
  { "size": 32, "palette": {"#xxx": [...], ...}, "total": N }
"""
import argparse, json, sys
from pathlib import Path
from collections import Counter

try:
    from PIL import Image
except ImportError:
    print("需要 Pillow: pip install Pillow", file=sys.stderr)
    sys.exit(1)


# 画板 36 色调色板（与 pixel-canvas.html 一致）
CANVAS_PALETTE = [
    "#111111","#333333","#555555","#777777","#999999","#CCCCCC","#FFFFFF",
    "#8B0000","#CC3333","#FF6B6B","#E8553A","#F0A040","#FFD080",
    "#F0C840","#FFE082","#1B5E20","#4CAF50","#8BC34A","#C8E6C9",
    "#0D47A1","#4A90D9","#64B5F6","#B3E5FC","#7B1FA2","#AB47BC",
    "#F06292","#F8BBD0","#CD6E58","#8D6E63","#5D4037",
    "#FFCC80","#FFD54F","#CFD8DC","#90A4AE","#607D8B",
]


def hex_to_rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"


def color_distance(c1, c2):
    """RGB 欧几里得距离（加权，人眼感知优化）"""
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    r_mean = (r1 + r2) // 2
    dr = r1 - r2
    dg = g1 - g2
    db = b1 - b2
    # 加权 RGB 距离（感知优化）
    return ((2 + r_mean / 256) * dr * dr +
            4 * dg * dg +
            (2 + (255 - r_mean) / 256) * db * db)


def nearest_canvas_color(rgb, palette_rgb):
    """找到画板调色板中最接近的颜色"""
    best = None
    best_dist = float("inf")
    for i, prgb in enumerate(palette_rgb):
        d = color_distance(rgb, prgb)
        if d < best_dist:
            best_dist = d
            best = i
    return CANVAS_PALETTE[best]


def quantize_image(img, n_colors):
    """将图片颜色量化到 n 种"""
    if n_colors >= 256:
        return img
    # Pillow 的 quantize 方法
    return img.quantize(colors=n_colors, method=Image.Quantize.MEDIANCUT).convert("RGB")


def photo_to_pixel(image_path, size=32, n_colors=8):
    """
    将照片转换为像素数据矩阵。
    返回: { "size": N, "pixels": { "#颜色": [[r,c],...] }, "preview": "ASCII预览" }
    """
    img = Image.open(image_path).convert("RGB")

    # 裁剪为正方形（取中心）
    w, h = img.size
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    img = img.crop((left, top, left + s, top + s))

    # 缩放到目标尺寸（NEAREST = 像素感）
    img = img.resize((size, size), Image.NEAREST)

    # 颜色量化
    img = quantize_image(img, min(n_colors, 256))

    # 获取像素数据
    pixels = img.load()

    # 调色板 RGB 预计算
    palette_rgb = [hex_to_rgb(c) for c in CANVAS_PALETTE]

    # 收集所有颜色
    color_count = Counter()
    pixel_data = {}
    for r in range(size):
        for c in range(size):
            rgb = pixels[c, r]  # PIL: (col, row)
            canvas_color = nearest_canvas_color(rgb, palette_rgb)
            color_count[canvas_color] += 1
            if canvas_color not in pixel_data:
                pixel_data[canvas_color] = []
            pixel_data[canvas_color].append([r, c])

    # ASCII 预览
    ascii_preview = []
    for r in range(size):
        row = ""
        for c in range(size):
            rgb = pixels[c, r]
            hex_c = nearest_canvas_color(rgb, palette_rgb)
            # 用简写符号
            brightness = (rgb[0] + rgb[1] + rgb[2]) // 3
            if brightness < 50:
                row += "@"
            elif brightness < 100:
                row += "#"
            elif brightness < 150:
                row += "x"
            elif brightness < 200:
                row += "."
            else:
                row += " "
        ascii_preview.append(row)

    return {
        "size": size,
        "colors": n_colors,
        "total_pixels": sum(len(v) for v in pixel_data.values()),
        "color_distribution": dict(color_count.most_common()),
        "pixels": pixel_data,
        "ascii_preview": ascii_preview,
    }


def main():
    parser = argparse.ArgumentParser(description="照片转像素数据")
    parser.add_argument("image", help="图片路径")
    parser.add_argument("--size", type=int, default=32, choices=[16, 24, 32, 48])
    parser.add_argument("--colors", type=int, default=8, help="量化颜色数")
    parser.add_argument("--preview", action="store_true", help="显示ASCII预览")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径")
    args = parser.parse_args()

    if not Path(args.image).exists():
        print(f"文件不存在: {args.image}", file=sys.stderr)
        sys.exit(1)

    result = photo_to_pixel(args.image, args.size, args.colors)

    if args.preview:
        print(f"尺寸: {result['size']}×{result['size']}")
        print(f"量化: {result['colors']} 色 → 实际映射 {len(result['pixels'])} 色")
        print(f"像素: {result['total_pixels']}")
        print(f"颜色分布: {dict(list(result['color_distribution'].items())[:5])}")
        print("\nASCII 预览:")
        for row in result["ascii_preview"]:
            print(row)

    # 输出 JSON（不含 ASCII 预览以节省体积）
    out = {k: v for k, v in result.items() if k != "ascii_preview"}
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False)
    else:
        # 只输出像素数据（精简版）
        print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
