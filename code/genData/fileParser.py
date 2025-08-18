import pandas as pd
import os

class FileParser:
    def __init__(self, file_path, preview_rows=10):
        """
        通用文件解析器
        :param file_path: 文件路径
        :param preview_rows: 每个文件/Sheet 预览的行数，默认 10 行
        """
        self.file_path = file_path
        self.preview_rows = preview_rows
        self.extracted_text = ""

    def extract_text(self):
        """根据文件类型提取文本"""
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext in [".xlsx", ".xls"]:
            self.extracted_text = self._extract_excel()
        elif ext == ".csv":
            self.extracted_text = self._extract_csv()
        elif ext in [".txt", ".md"]:
            self.extracted_text = self._extract_txt()
        else:
            raise ValueError(f"❌ 不支持的文件类型: {ext}")
        return self.extracted_text

    # ========================
    # 文件类型内部处理方法
    # ========================
    def _extract_excel(self):
        """
        读取 Excel 文件，每一行作为列表中的一个元素（字符串形式）。
        每个字段都带上列名，例如: "ColumnA: xxx | ColumnB: yyy"
        返回一个 list[str]。
        """
        try:
            excel_data = pd.ExcelFile(self.file_path)
            rows = []

            for sheet in excel_data.sheet_names:
                df = pd.read_excel(self.file_path, sheet_name=sheet)

                for idx, row in df.iterrows():
                    # 逐列拼接 "列名: 值"
                    row_items = []
                    for col, val in zip(df.columns, row.values):
                        if pd.notna(val):  # 跳过 NaN
                            row_items.append(f"{col}: {val}")

                    row_text = f"Sheet: {sheet}, Row {idx} | " + " | ".join(row_items)
                    rows.append(row_text)

            return rows

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