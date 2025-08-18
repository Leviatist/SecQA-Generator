# 1. 创建 conda 环境
conda create -n gradio python=3.10 -y

# 2. 激活环境
conda activate gradio

# 3. 安装需要的库
conda install pandas openpyxl tqdm -y     # 从 conda 装常见库
pip install gradio openai transformers    # gradio/openai/transformers 建议用 pip 装
