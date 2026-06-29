import re
import jsbeautifier # if available

def find_script_blocks(html):
    pattern = re.compile(r'<script.*?>([\s\S]*?)<\/script>', re.IGNORECASE)
    return pattern.findall(html)

def check_brackets(js_code):
    stack = []
    brackets = {'{': '}', '[': ']', '(': ')'}
    for char in js_code:
        if char in brackets:
            stack.append(char)
        elif char in brackets.values():
            if not stack:
                return f"Unmatched closing bracket {char}"
            top = stack.pop()
            if brackets[top] != char:
                return f"Mismatched bracket, expected {brackets[top]} but got {char}"
    if stack:
        return f"Unclosed brackets: {stack}"
    return "OK"

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

scripts = find_script_blocks(html)
for i, script in enumerate(scripts):
    res = check_brackets(script)
    print(f"Script {i}: {res}")

