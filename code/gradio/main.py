import gradio as gr
import requests
import pandas as pd
from openai import OpenAI
from fileParser import FileParser
from static import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, SYSPROMPT

def query_deepseek(sys_prompt, user_text, file_path):
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)
    content = FileParser(file_path).extract_text()
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_text + content[:1000]},
        ],
        stream=False
        )
    reasoning_content = response.choices[0].message.reasoning_content
    content = response.choices[0].message.content

    return reasoning_content, content

def updateSysprompt(input):
    sys_prompt = input
    return sys_prompt

with gr.Blocks() as demo:
    gr.Markdown("## DeepSeek 查询 GUI")
    with gr.Row():
        with gr.Column(scale=1):  # 默认系统提示词
            output = gr.Textbox(label="当前系统提示词", value=SYSPROMPT, interactive=False, lines=19, min_width=100)  # 输出框，不可编辑
        with gr.Column(scale=1):  # 中
            sys_prompt = gr.Textbox(label="修改系统提示词", placeholder="输入要更新的系统提示词", lines=16, min_width=300)
            update_button = gr.Button("更新系统提示词")
        with gr.Column(scale=1):  # 右
            user_input = gr.Textbox(label="输入文本", placeholder="在这里输入查询文本", lines=16, min_width=300)
            run_button = gr.Button("查询")
    file_input = gr.File(label="拖拽文件上传", file_types=[".xlsx", ".xls"], min_width=100, elem_id="file-box")
    with gr.Row():
        with gr.Column(scale=1):  # 默认系统提示词
            chain_output = gr.Textbox(label="思维链", lines=16)
        with gr.Column(scale=1):  # 中
            result_output = gr.Textbox(label="最终结果", lines=16)

    update_button.click(updateSysprompt, inputs = sys_prompt, outputs = output)
    
    run_button.click(query_deepseek, 
                     inputs=[sys_prompt, user_input, file_input],
                     outputs=[chain_output, result_output])

demo.launch(share=True)
