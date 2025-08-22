import pdfplumber
import pandas as pd
import os

class FileParser:
    def __init__(self, file_path, preview_rows=30):
        """
        通用文件解析器
        :param file_path: 文件路径
        :param preview_rows: 每个文件/Sheet 预览的行数，默认 1000 行
        """
        self.file_path = file_path
        self.preview_rows = preview_rows
        self.extracted_text = ""

    def extract_text(self):
        """根据文件类型提取文本"""
        if self.file_path == None:
            return ''
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext in [".xlsx", ".xls"]:
            self.extracted_text = self._extract_excel()
        elif ext == ".csv":
            self.extracted_text = self._extract_csv()
        elif ext in [".txt", ".md"]:
            self.extracted_text = self._extract_txt()
        elif ext == ".pdf":
            self.extracted_text = self._extract_pdf()
        else:
            raise ValueError(f"❌ 不支持的文件类型: {ext}")
        return self.extracted_text

    # ========================
    # 文件类型内部处理方法
    # ========================
    def _extract_excel(self):
        text = ""
        try:
            excel_data = pd.ExcelFile(self.file_path)
            # fuc2: markdown_table = df.to_markdown(index=False) # index=False表示不显示行索引
            for sheet in excel_data.sheet_names:
                df = pd.read_excel(self.file_path, sheet_name=sheet)
                text += f"\n=== Sheet: {sheet} ===\n"
                text += df.head(self.preview_rows).to_string(index=False)
            return text
        except Exception as e:
            raise RuntimeError(f"❌ Excel 解析出错: {str(e)}")

    def _extract_csv(self):
        try:
            df = pd.read_csv(self.file_path)
            text = df.head(self.preview_rows).to_string(index=False)
            return text
        except Exception as e:
            raise RuntimeError(f"❌ CSV 解析出错: {str(e)}")

    def _extract_txt(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            text = "".join(lines[:self.preview_rows])
            return text
        except Exception as e:
            raise RuntimeError(f"❌ 文本文件解析出错: {str(e)}")
        
    def _extract_pdf(self):
        text = ""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                total_pages = len(pdf.pages)
                preview_pages = min(self.preview_rows, total_pages)  # 这里用 preview_rows 控制页数预览
                for i in range(preview_pages):
                    page = pdf.pages[i]
                    text += f"\n=== Page {i+1} ===\n"
                    text += page.extract_text() or "[⚠️ 无法提取文本]"
            return text
        except Exception as e:
            raise RuntimeError(f"❌ PDF 解析出错: {str(e)}")