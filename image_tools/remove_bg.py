import os
import datetime
from rembg import remove
from PIL import Image

# 支持的图片格式
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}


def remove_background(input_path, output_root):
    """
    对输入图片去背景，并将结果保存到输出文件夹。

    参数:
        input_path (str): 输入图片的路径。
        output_root (str): 输出文件夹的根目录。
    """
    # 获取文件名和扩展名
    file_name = os.path.basename(input_path)
    name, ext = os.path.splitext(file_name)

    # 检查是否为支持的图片格式
    if ext.lower() not in SUPPORTED_EXTENSIONS:
        print(f"[跳过] 非支持的图片格式：{input_path}")
        return

    # 创建输出文件夹
    os.makedirs(output_root, exist_ok=True)
    time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    output_path = os.path.join(output_root, f"{name}_rembg_{time_str}{ext}")

    try:
        # 打开图片并去背景
        with open(input_path, "rb") as input_file:
            input_data = input_file.read()
            output_data = remove(input_data)

        # 保存结果图片
        with open(output_path, "wb") as output_file:
            output_file.write(output_data)

        print(f"[完成] {input_path} 去背景完成，结果保存到 {output_path}")

    except Exception as e:
        print(f"[错误] 无法处理图片：{input_path}，错误信息：{e}")


def process_folder(input_folder, output_root):
    """
    递归遍历文件夹，并对符合条件的图片进行去背景处理。

    参数:
        input_folder (str): 输入文件夹路径。
        output_root (str): 输出文件夹路径。
    """
    for root, _, files in os.walk(input_folder):
        for file in files:
            # 检查文件扩展名是否为图片格式
            if os.path.splitext(file)[-1].lower() not in SUPPORTED_EXTENSIONS:
                continue

            input_path = os.path.join(root, file)
            remove_background(input_path, output_root)


if __name__ == "__main__":
    # 输入文件夹
    input_folder = input("请输入图片文件夹路径：").strip()
    output_root = "output/remove_bg"  # 输出文件夹

    if not os.path.exists(input_folder):
        print(f"[错误] 输入文件夹不存在：{input_folder}")
    else:
        process_folder(input_folder, output_root)
        print(f"所有符合条件的图片已去背景完成，结果保存到 {output_root}")
