import pandas as pd
import tiktoken

def count_tokens_in_excel(file_path, model="gpt-4"):
    """
    统计 Excel 文件中的 token 数
    """
    # 读取 Excel
    xls = pd.ExcelFile(file_path)
    extracted_text = ""
    for sheet in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        extracted_text += f"\n=== Sheet: {sheet} ===\n"
        extracted_text += df.to_string(index=False)  # 转成字符串
    return len(extracted_text)
    # 获取对应模型的 tokenizer
    encoding = tiktoken.encoding_for_model(model)
    # 编码并统计
    tokens = encoding.encode(extracted_text)
    token_count = len(tokens)
    return token_count


if __name__ == "__main__":
    # ✅ 直接在这里写文件路径
    file_path = "data/raw/enterprise-attack.xlsx"

    tokens = count_tokens_in_excel(file_path)
    print(f"📊 文件 {file_path} 的总 token 数: {tokens}")
