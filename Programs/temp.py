from PIL import Image

def png_to_eps(png_path, eps_path, dpi=300):
    """
    Convert PNG to EPS with RGB mode to avoid grayscale issues.
    png_path: 输入 PNG 文件路径
    eps_path: 输出 EPS 文件路径
    dpi: 输出分辨率（打印建议300）
    """
    # 打开PNG并强制转成RGB，避免被识别为灰度
    img = Image.open(png_path).convert("RGB")

    # 保存为EPS
    img.save(eps_path, format='EPS', dpi=(dpi, dpi))

    print(f"转换完成：{eps_path}")

# -----------使用示例-----------
png_to_eps("input.png", "output.eps", dpi=300)
