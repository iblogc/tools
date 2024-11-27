# Excel转图片工具

这是一个简单的Python工具，可以将Excel文件转换为长图片。

## 功能特点

- 支持.xlsx和.xls格式的Excel文件
- 自动调整列宽以适应内容
- 保持表格样式，包括表头和网格线
- 使用图形界面选择文件
- 自动将输出图片保存在Excel文件相同目录下

## 使用方法

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行程序：
```bash
python excel_to_image.py
```

3. 在弹出的文件选择窗口中选择要转换的Excel文件
4. 程序会自动将转换后的图片保存在与Excel文件相同的目录下，文件名相同但扩展名为.png

## 注意事项

- 确保系统已安装Python 3.x
- 如果要使用中文显示，确保系统安装了微软雅黑字体（msyh.ttc）
- 建议Excel文件不要过大，否则可能生成的图片尺寸会很大
