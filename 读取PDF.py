import sys
import importlib
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfpage import PDFTextExtractionNotAllowed


# 对本地保存的pdf文件进行读取和写入到txt文件当中


# 定义解析函数
def pdftotxt(path,new_name):
    # 创建一个文档分析器
    parser = PDFParser(path)
    # 创建一个PDF文档对象存储文档结构
    document =PDFDocument(parser)
    # 判断文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储资源
        resmag =PDFResourceManager()
        # 设定参数进行分析
        laparams =LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(resmag)
        device =PDFPageAggregator(resmag,laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(resmag, device)
        # 处理每一页
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout =device.get_result()
            for y in layout:
                if(isinstance(y,LTTextBoxHorizontal)):
                    with open("%s"%(new_name),'a',encoding="utf-8") as f:
                        f.write(y.get_text()+"\n")

# 获取文件的路径
path =open( "C:/Users/HP/Pictures\微信图片_20250929220709_41_72.pdf",'rb')
pdftotxt(path,"pdfminer111.txt")