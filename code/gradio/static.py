DEEPSEEK_API_KEY = "sk-9147b6e1d7e642ac8b492d6f1d2d191a"
DEEPSEEK_API_URL = "https://api.deepseek.com"
SYSPROMPT = f"""
    Based on the document line given by the user, generate a QA pair in JSON format.
    Only return valid JSON, nothing else
    Each QA pair should have:
    - question: a clear question
    - thought: reasoning about how to answer
    - answer: complete and concise
    - references: list of supporting sentences from the line
    
    JSON format example:
    {{
        "question": "...",
        "thought": "...",
        "answer": "...",
        "references": ["..."]
    }}
"""