# 项目简介
1. 实现了一个基于gradio的gui界面，用户拖拽文件输入，问询大模型得到输出，用户需要调整系统提示词
2. QA pair写入json文件，包含四部分"question"  "thought"  "answer"  "references"
3. 用户拖拽输入的文件包括excel,pdf两种（暂定）
4. 
## 项目构成
```
gradio/
├──archived/                                   # 原始文件存档
│   │   ├── demo.py                            
│   │   ├── enterprise-attack.xlsx
│   │   └── generated_QA_attack.json                     
├── code/
│   │   ├── genData/  
│   │   │   ├── API.py                         # 存放Deepseek API
│   │   │   ├── fileParser.py                  # 文件解析 Parser类（库）
│   │   │   ├── genQA_DeepSeek.py              # QA pair生成主程序，使用DeepSeek API
│   │   │   ├── genQA_GPT4ALL.py               # QA pair生成主程序，使用本地大模型
│   │   │   ├── static.py                      # 静态信息（库）
│   │   │   └── utils.py                       # 工具函数（库）
│   │   ├── gradio/  
│   │   │   ├── fileParser.py                  # 文件解析 Parser类
│   │   │   ├── main.py                        # 主程序入口
│   │   │   └── static.py                      # 静态信息（库）
│   │   ├── setEnv/  
│   │   │   └── setEnv.sh                      # conda环境配置
│   │   ├── utils/  
│   │   │   └── getToken.py                    # 统计数据Tokens数
├── data/
│   │   ├── example_output/
│   │   │   └── generated_QA_attack.json       # 训练数据样例
│   │   ├── raw/
│   │   │   └── enterprise-attack.xlsx         # 表格文件原始存档
├── model/
│   │   ├── Meta-Llama-3-8B-Instruct.Q4_0.gguf # 本地大模型
│   │   └── Modelfile.txt                      # Ollama的配置文件
├── output/
│   │   └── generated_QA_attack.json           # 本次生成的训练数据
├── info.txt
├── README.md
└── .gitignore
```
## Todo
1. Rag
## 如何使用这个项目
### 自动生成QA pair
#### 方法1：使用deepseek API
1. 在genData下新建一个API.py文件（已有则不用），配置好自己的API key和URL，形式类似于：
```
DEEPSEEK_API_KEY = "xxx"
DEEPSEEK_API_URL = "https://api.deepseek.com"
```
2. 配置好该项目的环境，直接运行即可
Notice: API_KEY要小心避免被外人知晓
#### 方法2：使用本地大模型 
1. 前往 [Ollama官网](https://ollama.com/download)下载Ollama
2. 在该项目的Model文件夹打开终端，依次输入：
```
ollama create llama3-8b-instruct -f Modelfile
ollama run llama3-8b-instruct
```
3. 配置好该项目需要的环境，直接运行即可
### gradio界面
#### 功能简介
gradio界面目前支持的功能如下：
1. 实时预览系统提示词，并可自由修改
2. 用户输入文件和用户提示词，大模型给出输出
3. 输入文件目前支持: xls, xlsx, csv, pdf 
4. 用户输入自己对于输出的看法，Deepseek给出修正的系统提示词