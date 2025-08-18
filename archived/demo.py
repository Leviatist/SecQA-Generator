import gradio as gr
import pandas as pd
import json
from openpyxl import load_workbook
import os
from openai import OpenAI
from tqdm import tqdm
import transformers

# 定义核心功能函数

def generate_and_save_questions(doc):
    prompt = """You are a JSON generator who generates machine-readable JSON.
    Based on the following document, follow the instruction below
    Document:
    %s
    Instruction:
    Generate 10 of unique question, thought, answer, and references from the above document in the following JSON format. 
    The answers must avoid words that are not specific (e.g., "many", "several", "few", etc.). 
    The answers must contain specific, verbose, self-contained, grammatically correct sentences that answer the question comprehensively. 
    The answers must strictly contain content from the document and no content from outside the document. There may be multiple references that contain verbatim text from the document to support the answers.
    JSON format:
    [
        {
            "question": "<generated question>",
            "thought": "<generated thought on what is needed to answer the question. Start with 'To answer the question, I need'>",
            "answer": "<generated answer>",
            "references": [
                "<verbatim text from document that supports the answer>",
                "<verbatim text from document that supports the answer>"
            ]
        }
    ]
    The first character of the response must be '[' and the last character must be ']'. No header text should be included.
    """ % (doc)

    client = OpenAI(api_key="sk-9147b6e1d7e642ac8b492d6f1d2d191a", 
                        base_url="https://api.deepseek.com")
    request = client.chat.completions.create(
    model = "deepseek-chat",
    messages=[
        {"role": "system", "content": prompt}
        # {"role": "user", "content": "根据文本提供的内容，生成问题-答案对，并以JSON格式保存"}
        # {"role": "user", "content": "Generate question-answer pairs in Chinese"+
        #  "in the following JSON format according to the document."},
    ],
    stream=False,
    max_tokens = 8192        
    )
    raw_questions = request.choices[0].message.content.strip()
    
    
    return raw_questions

def to_uppercase(text):
    return text.upper()

if __name__ == "__main__":
    # 创建 Gradio 接口
    with gr.Blocks() as demo:
        # 添加输入和输出组件
        input_text = gr.Textbox(label="输入文本")

        output_text = gr.Textbox(label="输出文本")
        file = gr.File(label="上传文件")
        # 绑定函数到按钮点击事件
        submit_button = gr.Button("执行")
        # submit_button.click(to_uppercase, inputs=input_text, outputs=output_text)
        submit_button.click(generate_and_save_questions, inputs=input_text, outputs=output_text)

    # 启动界面
    demo.launch(share=True)
