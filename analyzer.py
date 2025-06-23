import json
import openai

TEMPLATE_PATH = 'prompt_template.txt'

with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    PROMPT_TEMPLATE = f.read()

def analyze_article(article: str) -> dict:
    prompt = PROMPT_TEMPLATE.replace('{article}', article)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.3,
    )
    content = response.choices[0].message.content
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        # fallback simple parser
        result = {
            'stance': None,
            'missing_perspectives': [],
            'balance_score': None,
        }
    return result
