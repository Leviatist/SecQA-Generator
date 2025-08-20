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
│   │   │   ├── fileParser.py                  # 文件解析 Parser类（库）
│   │   │   ├── genQA.py                       # QA pair生成主程序
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
│   │   └── Meta-Llama-3-8B-Instruct.Q4_0.gguf # 本次生成的训练数据
├── output/
│   │   └── generated_QA_attack.json           # 本次生成的训练数据
├── info.txt
├── README.md
└── .gitignore
```
## Todo
1. 对每个Row生成多行训练数据
2. gradio界面，加一个AI自动调整提示词
3. Rag