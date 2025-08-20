import gradio as gr
import requests
import pandas as pd
from openai import OpenAI
from fileParser import FileParser
from static import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, SYSPROMPT

# 查询 deepseek
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

# 更新系统提示词
def updateSysprompt(input):
    sys_prompt = input
    return sys_prompt

# 根据用户反馈自动生成新的系统提示词
def generate_sys_prompt_from_feedback(original_sys_prompt, feedback):
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": "你是一个prompt工程专家，用户将给你一个当前的系统提示词和一段反馈，请你输出一个更好的系统提示词。"},
            {"role": "user", "content": f"原系统提示词如下：\n{original_sys_prompt}\n\n用户反馈如下：\n{feedback}\n\n请你基于这些生成一个新的系统提示词，尽量满足用户的意图。"},
        ],
        stream=False
    )
    new_prompt = response.choices[0].message.content
    return new_prompt

with gr.Blocks() as demo:
    gr.Markdown("## DeepSeek 查询 GUI")

    with gr.Row():
        with gr.Column(scale=1):
            latest_sys_prompt = gr.Textbox(label="当前系统提示词", value=SYSPROMPT, interactive=False, lines=19, min_width=100)

        with gr.Column(scale=1):
            sys_prompt = gr.Textbox(label="修改系统提示词", placeholder="输入要更新的系统提示词", lines=16, min_width=300)
            update_button = gr.Button("更新系统提示词")

        with gr.Column(scale=1):
            user_input = gr.Textbox(label="输入文本", placeholder="在这里输入查询文本", lines=16, min_width=300)
            run_button = gr.Button("查询")

    file_input = gr.File(label="拖拽文件上传", file_types=[".xlsx", ".xls", ".csv", ".pdf"], min_width=100, elem_id="file-box")

    with gr.Row():
        with gr.Column(scale=1):
            chain_output = gr.Textbox(label="思维链", lines=24)
        with gr.Column(scale=1):
            result_output = gr.Textbox(label="最终结果", lines=24)

    # 用户反馈部分
    gr.Markdown("### 📝 对当前输出结果的反馈")
    feedback_input = gr.Textbox(label="请输入你对当前输出的反馈", placeholder="例如：结果不够详细 / 想更专业 / 想更口语化", lines=5)
    gen_prompt_button = gr.Button("根据反馈生成新的系统提示词")

    # 绑定事件
    update_button.click(
        updateSysprompt, 
        inputs=sys_prompt, 
        outputs=[latest_sys_prompt] 
    )

    run_button.click(
        query_deepseek, 
        inputs=[latest_sys_prompt, user_input, file_input], 
        outputs=[chain_output, result_output]
    )

    gen_prompt_button.click(
        generate_sys_prompt_from_feedback,
        inputs=[sys_prompt, feedback_input],
        outputs=[latest_sys_prompt] 
    )

    demo.launch(share=True)