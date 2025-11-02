import os
import fitz
import io
import logging
from PIL import Image, ImageEnhance
import pytesseract
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class AdvancedOCRProcessor:
    def __init__(self):
        # Tesseract配置
        self.tesseract_path = r"D:\Program Files\Tesseract-OCR\tesseract.exe"
        self.tessdata_path = r"D:\Program Files\Tesseract-OCR\tessdata"
        self.setup_tesseract()

        print("🎯 OCR处理器初始化完成")
        print(f"📅 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def setup_tesseract(self):
        """配置Tesseract"""
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
        os.environ['TESSDATA_PREFIX'] = self.tessdata_path

        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Tesseract版本: {version}")
        except:
            print("❌ Tesseract未正确配置")

    def enhance_image(self, image):
        """高级图像增强"""
        # 转换为RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 一系列增强处理
        enhancements = [
            ('对比度', 2.2),
            ('锐度', 1.8),
            ('亮度', 1.1),
            ('色彩饱和度', 1.2)
        ]

        for name, factor in enhancements:
            try:
                if name == '对比度':
                    enhancer = ImageEnhance.Contrast(image)
                elif name == '锐度':
                    enhancer = ImageEnhance.Sharpness(image)
                elif name == '亮度':
                    enhancer = ImageEnhance.Brightness(image)
                elif name == '色彩饱和度':
                    enhancer = ImageEnhance.Color(image)

                image = enhancer.enhance(factor)
                print(f"    🔧 {name}增强: {factor}x")
            except Exception as e:
                print(f"    ⚠ {name}增强失败: {e}")

        return image

    def pdf_to_optimized_images(self, pdf_path, dpi=400):
        """优化PDF转换"""
        try:
            doc = fitz.open(pdf_path)
            images = []

            print(f"📊 PDF信息:")
            print(f"  页数: {len(doc)}")
            print(f"  元数据: {doc.metadata}")

            for page_num in range(len(doc)):
                page = doc[page_num]

                # 获取页面尺寸信息
                rect = page.rect
                print(f"  第{page_num + 1}页尺寸: {rect.width:.1f} x {rect.height:.1f}")

                # 高质量转换
                mat = fitz.Matrix(dpi / 72, dpi / 72)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))

                images.append(image)
                print(f"✅ 第 {page_num + 1} 页转换完成")

            doc.close()
            return images

        except Exception as e:
            print(f"❌ PDF转换失败: {e}")
            return []

    def smart_ocr(self, image, page_num):
        """智能OCR识别"""
        print(f"  🔍 第{page_num}页文字识别:")
        print("  " + "─" * 35)

        # 图像增强
        enhanced_image = self.enhance_image(image)

        # 保存处理前后的对比（可选）
        if page_num == 1:  # 只保存第一页作为样例
            enhanced_image.save(f"enhanced_page_{page_num}.png")
            print(f"    💾 增强图像已保存: enhanced_page_{page_num}.png")

        # OCR识别策略
        strategies = [
            {'lang': 'chi_sim+eng', 'name': '中英混合'},
            {'lang': 'chi_sim', 'name': '纯中文'},
            {'lang': 'eng', 'name': '纯英文'}
        ]

        best_result = ""
        best_strategy = ""

        for strategy in strategies:
            try:
                text = pytesseract.image_to_string(enhanced_image, lang=strategy['lang'])

                if text.strip():
                    chinese_count = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
                    total_chars = len(text.strip())

                    print(f"    {strategy['name']}: {total_chars}字符, {chinese_count}中文")

                    # 选择最好的结果（中文内容多的优先）
                    if chinese_count > sum(1 for char in best_result if '\u4e00' <= char <= '\u9fff'):
                        best_result = text
                        best_strategy = strategy['name']

            except Exception as e:
                print(f"    ⚠ {strategy['name']}失败: {e}")

        if best_result:
            print(f"    🎯 使用策略: {best_strategy}")
            return best_result.strip()
        else:
            return ""

    def clean_text(self, text):
        """文本清理和格式化"""
        if not text:
            return ""

        # 分割行并清理
        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            if line:
                # 移除过多的空格
                line = ' '.join(line.split())
                cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def analyze_content(self, text):
        """内容分析"""
        if not text:
            return {}

        analysis = {
            'total_chars': len(text),
            'chinese_chars': sum(1 for char in text if '\u4e00' <= char <= '\u9fff'),
            'english_chars': sum(1 for char in text if char.isalpha() and char.isascii()),
            'digit_chars': sum(1 for char in text if char.isdigit()),
            'lines': text.count('\n') + 1,
            'questions': text.count('?') + text.count('？'),
            'options': text.count('A.') + text.count('B.') + text.count('C.') + text.count('D.')
        }

        return analysis

    def process_pdf(self, pdf_path, output_path=None):
        """处理PDF主函数"""
        print(f"\n📖 开始处理: {os.path.basename(pdf_path)}")
        print("=" * 60)

        start_time = datetime.now()

        if not os.path.exists(pdf_path):
            print(f"❌ 文件不存在: {pdf_path}")
            return None

        # 转换PDF
        images = self.pdf_to_optimized_images(pdf_path)
        if not images:
            return None

        all_results = []
        total_analysis = {
            'total_chars': 0, 'chinese_chars': 0, 'english_chars': 0,
            'digit_chars': 0, 'lines': 0, 'questions': 0, 'options': 0
        }

        # 处理每一页
        for i, image in enumerate(images):
            page_num = i + 1
            print(f"\n📄 处理第 {page_num}/{len(images)} 页:")

            # OCR识别
            text = self.smart_ocr(image, page_num)

            if text:
                # 清理文本
                cleaned_text = self.clean_text(text)

                # 分析内容
                analysis = self.analyze_content(cleaned_text)

                # 更新总统计
                for key in total_analysis:
                    total_analysis[key] += analysis[key]

                # 构建页面内容
                page_header = f"\n{'=' * 60}\n第 {page_num} 页 (分析结果↓)\n{'=' * 60}"
                page_stats = f"📊 本页统计: {analysis['total_chars']}字符, {analysis['chinese_chars']}中文, {analysis['lines']}行"
                page_content = f"{page_header}\n{page_stats}\n{cleaned_text}\n"

                all_results.append(page_content)
                print(f"✅ 第{page_num}页完成")
            else:
                page_content = f"\n{'=' * 60}\n第 {page_num} 页\n{'=' * 60}\n[未识别到文本]\n"
                all_results.append(page_content)
                print(f"⚠ 第{page_num}页未识别到文本")

        # 合并结果
        final_text = "\n".join(all_results)

        # 添加总结信息
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        summary = f"""
{'=' * 80}
📋 处 理 总 结
{'=' * 80}
📅 处理时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')} → {end_time.strftime('%H:%M:%S')}
⏱ 耗时: {processing_time:.1f}秒
📄 总页数: {len(images)}
📊 内容统计:
   📝 总字符数: {total_analysis['total_chars']}
   🔤 中文字符: {total_analysis['chinese_chars']}
   🔠 英文字符: {total_analysis['english_chars']}
   🔢 数字字符: {total_analysis['digit_chars']}
   📏 总行数: {total_analysis['lines']}
   ❓ 问题数量: {total_analysis['questions']}
   ◯ 选项数量: {total_analysis['options']}
{'=' * 80}
"""
        final_text = summary + final_text

        # 保存结果
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(final_text)
                print(f"\n💾 结果已保存: {output_path}")

                # 保存统计信息
                stats_path = os.path.splitext(output_path)[0] + "_统计.txt"
                with open(stats_path, 'w', encoding='utf-8') as f:
                    f.write(summary)
                print(f"📊 统计信息: {stats_path}")

            except Exception as e:
                print(f"❌ 保存失败: {e}")

        return final_text

    def show_detailed_preview(self, result_text):
        """显示详细预览"""
        if not result_text:
            return

        print(f"\n🎉 处理完成！")
        print("=" * 60)

        # 提取总结信息
        lines = result_text.split('\n')
        summary_lines = [line for line in lines if
                         '处理总结' in line or '=' in line or any(marker in line for marker in ['📅', '⏱', '📄', '📊'])]

        for line in summary_lines[:15]:
            print(line)

        # 显示内容样本
        print(f"\n📋 内容样本:")
        print("-" * 50)

        content_lines = [line for line in lines if line.strip() and not line.startswith('=') and not any(
            marker in line for marker in ['📅', '⏱', '📄', '📊'])]

        sample_count = 0
        for line in content_lines:
            if line.strip() and sample_count < 8:
                print(f"  {line}")
                sample_count += 1
            elif sample_count >= 8:
                print("  ...")
                break


def main():
    """主函数"""
    print("=" * 80)
    print("                 高 级 PDF 文 字 提 取 工 具")
    print("=" * 80)

    # 创建处理器
    processor = AdvancedOCRProcessor()

    # 处理PDF
    pdf_path = "C:/Users/HP/Pictures/5.pdf"
    output_path = "高级提取结果.txt"

    result = processor.process_pdf(pdf_path, output_path)

    # 显示结果
    if result:
        processor.show_detailed_preview(result)
    else:
        print("❌ 提取失败")


if __name__ == "__main__":
    main()