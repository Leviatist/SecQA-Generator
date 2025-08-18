import json
import pandas as pd
from gpt4all import GPT4All
from utils import extract_strict_json 
from fileParser import FileParser
from static import INPUT_PATH, OUTPUT_PATH, SYSPROMPT
from tqdm import tqdm

# 初始化本地 GPT4All 模型
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf", model_path="model")

# 读取 Excel 行
parser = FileParser(INPUT_PATH)
rows = parser.extract_text()  # 每行数据是列表的一项

results = []

for idx, row_text in enumerate(tqdm(rows, desc="Generating QA pairs")):
    if idx==10:
        break
    # 构建 prompt：结合系统提示和当前行数据
    prompt = f"{SYSPROMPT}\nDocument line:\n{row_text}\n\nYou MUST generate a QA pair STRICTLY in JSON format."
    
    try:
        # 调用 GPT4All 生成
        content = model.generate(prompt)
        
        # 严格解析 JSON
        qa_pair = extract_strict_json(content)
        results.append(qa_pair)
        
    except Exception as e:
        print(f"[ERROR] Failed to generate QA for row {idx}: {e}")
        continue

# 写入 JSON 文件
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f"[INFO] QA pairs saved to {OUTPUT_PATH}")
