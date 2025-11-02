from PIL import Image
import os


def jpg_to_pdf_pil(jpg_path, output_folder):
    """
    使用PIL将JPG转换为PDF
    """
    try:
        # 检查输入文件是否存在
        if not os.path.exists(jpg_path):
            print(f"错误：图片文件不存在 - {jpg_path}")
            return

        # 检查输出文件夹是否存在
        if not os.path.exists(output_folder):
            print(f"错误：输出文件夹不存在 - {output_folder}")
            return

        # 生成输出PDF文件路径
        file_name = os.path.splitext(os.path.basename(jpg_path))[0] + ".pdf"
        pdf_path = os.path.join(output_folder, file_name)

        # 打开图片
        image = Image.open(jpg_path)

        # 转换为RGB模式（如果需要）
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 保存为PDF
        image.save(pdf_path, "PDF", resolution=100.0)
        print(f"转换成功: {jpg_path} -> {pdf_path}")

    except Exception as e:
        print(f"转换失败: {e}")


# 使用示例 - 修正后的调用方式
jpg_to_pdf_pil("C:/Users/HP/Desktop/9.jpeg", "C:/Users/HP/Pictures")