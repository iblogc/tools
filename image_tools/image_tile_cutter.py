import os
import datetime
from PIL import Image

# 支持的图片格式
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}


def crop_image_by_name(input_path, output_root):
    """
    根据图片文件名规则裁剪图片，并将裁剪后的图片保存到对应文件夹。

    文件名规则：xxx-4x3.jpg
    - xxx: 图片名称
    - 4x3: 表示将图片横向 4 等分，纵向 3 等分。

    参数:
        input_path (str): 输入图片文件的路径。
        output_root (str): 输出文件夹的根目录。
    """
    # 获取文件名和扩展名
    file_name = os.path.basename(input_path)
    name, ext = os.path.splitext(file_name)

    # 检查文件名规则
    if "-" not in name or "x" not in name.split("-")[-1]:
        print(f"[跳过] 文件名不符合规则：{input_path}")
        return

    # 提取图片名称和分割参数
    base_name, grid_spec = name.rsplit("-", 1)
    try:
        cols, rows = map(int, grid_spec.split("x"))
    except ValueError:
        print(f"[跳过] 文件名中的分割参数无效：{input_path}")
        return

    # 打开图片
    try:
        image = Image.open(input_path)
    except Exception as e:
        print(f"[错误] 无法打开图片：{input_path}，错误信息：{e}")
        return

    # 计算每个小图片的宽度和高度
    img_width, img_height = image.size
    tile_width = img_width // cols
    tile_height = img_height // rows

    # 创建输出文件夹
    # output_folder = os.path.join(output_root, base_name)
    output_folder = output_root
    os.makedirs(output_folder, exist_ok=True)

    # 裁剪图片并保存
    counter = 1
    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            top = row * tile_height
            right = left + tile_width
            bottom = top + tile_height
            cropped_image = image.crop((left, top, right, bottom))
            time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

            # 保存裁剪后的图片
            output_file = os.path.join(output_folder, f"{base_name}-{counter:02}_{time_str}.png")
            cropped_image.save(output_file)
            counter += 1

    print(f"[完成] {input_path} 已裁剪并保存到 {output_folder}")


def process_folder(input_folder, output_root):
    """
    递归遍历文件夹，并裁剪符合规则的图片。

    参数:
        input_folder (str): 输入文件夹路径。
        output_root (str): 裁剪后图片保存的根目录。
    """
    for root, _, files in os.walk(input_folder):
        for file in files:
            # 检查文件扩展名是否为图片格式
            if os.path.splitext(file)[-1].lower() not in SUPPORTED_EXTENSIONS:
                continue

            input_path = os.path.join(root, file)
            crop_image_by_name(input_path, output_root)


if __name__ == "__main__":
    # 输入文件夹
    input_folder = input("请输入图片文件夹路径：").strip()
    output_root = "output/image_tile_cutter"  # 输出文件夹根目录

    if not os.path.exists(input_folder):
        print(f"[错误] 输入文件夹不存在：{input_folder}")
    else:
        process_folder(input_folder, output_root)
        print(f"所有符合规则的图片已裁剪完成，结果保存到 {output_root}")
