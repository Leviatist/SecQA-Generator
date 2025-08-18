import json
import re

def extract_strict_json(content, required_fields=None):
    """
    尝试从模型输出中提取严格 JSON 并校验字段
    
    Args:
        content (str): 模型返回的文本
        required_fields (list[str], optional): 必须包含的字段，默认 ["question", "thought", "answer", "references"]
    
    Returns:
        dict or None: 返回解析后的 JSON dict，如果不合法返回 None
    """
    if required_fields is None:
        required_fields = ["question", "thought", "answer", "references"]

    # 去掉首尾空格
    content = content.strip()

    # 用正则提取最外层 JSON
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if not match:
        return None

    try:
        qa_pair = json.loads(match.group())
    except json.JSONDecodeError:
        return None

    # 校验字段完整性
    if all(field in qa_pair for field in required_fields) and isinstance(qa_pair.get("references", None), list):
        return qa_pair
    else:
        return None
