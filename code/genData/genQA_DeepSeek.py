import json
import pandas as pd
from openai import OpenAI
from utils import extract_strict_json
from fileParser import FileParser
from API import DEEPSEEK_API_URL, DEEPSEEK_API_KEY
from static import INPUT_PATH, OUTPUT_PATH, SYSPROMPT

# 初始化 DeepSeek 客户端
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)

parser = FileParser(INPUT_PATH)

rows = parser.extract_text()

results = []

for idx, row_text in enumerate(rows):
    for j in range(10):
        print(f"[INFO] Generating QA for {idx*10+1}/{len(rows)*10}...")

        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": SYSPROMPT},
                    {"role": "user", "content": row_text}
                ],
                temperature=0.3
            )

            content = response.choices[0].message.content
            qa_pair = extract_strict_json(content)
            results.append(qa_pair)

        except Exception as e:
            print(f"[ERROR] Failed to generate QA for row {idx}: {e}")
            continue

# 写入 JSON 文件
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f"[INFO] QA pairs saved to {OUTPUT_PATH}")