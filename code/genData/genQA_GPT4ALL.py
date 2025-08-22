from openai import OpenAI
from utils import extract_strict_json
from fileParser import FileParser
from static import DEEPSEEK_API_URL, DEEPSEEK_API_KEY, INPUT_PATH, OUTPUT_PATH, SYSPROMPT

# 连接本地 Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama 默认 API 地址
    api_key="ollama"  # 随便填，Ollama 不校验
)

parser = FileParser(INPUT_PATH)

rows = parser.extract_text()

results = []

for idx, row_text in enumerate(rows):
    if idx == 10:
        break
    for j in range(10):
        print(f"[INFO] Generating QA for {idx*10+j+1}/{len(rows)*10}...")

        try:
            response = client.chat.completions.create(
                model="llama3-8b-instruct",  # 改成你在 Ollama 里可用的模型名
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

print("[DONE] QA generation finished.")
