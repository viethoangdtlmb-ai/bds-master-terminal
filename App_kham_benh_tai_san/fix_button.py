import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Locate the line starting with "document.getElementById('result-' + sc.id).innerHTML = rows.map(r =>"
# and ending with "renderCompareTable(results);"
# We will use regex to find this block and replace it.

pattern = re.compile(
    r"(document\.getElementById\('result-' \+ sc\.id\)\.innerHTML = rows\.map\(r =>[\s\S]*?</div>`\)\.join\(''\);?\s*\}\);\s*)renderCompareTable\(results\);",
    re.MULTILINE
)

def replacer(match):
    # Check if the button is already there
    if "Lưu Kịch Bản Này" in match.group(1):
        return match.group(0) # Do nothing
    
    # Otherwise, inject the button
    # Replace the `).join('');` with `).join('') + <button...>`
    original_block = match.group(1)
    if "}).join('');" in original_block:
        new_block = original_block.replace("`).join('');", "`).join('') + `<button class=\"btn btn-primary btn-sm\" style=\"width:100%;margin-top:12px;background:rgba(255,255,255,0.05);color:${sc.color};border:1px solid ${sc.color}44\" onclick=\"saveToCart('${sc.id}')\">📍 Lưu Kịch Bản Này</button>`;")
    elif "`).join('')" in original_block:
        new_block = original_block.replace("`).join('')", "`).join('') + `<button class=\"btn btn-primary btn-sm\" style=\"width:100%;margin-top:12px;background:rgba(255,255,255,0.05);color:${sc.color};border:1px solid ${sc.color}44\" onclick=\"saveToCart('${sc.id}')\">📍 Lưu Kịch Bản Này</button>`")
    else:
        new_block = original_block
    
    return new_block + "window._LAST_SCENARIOS_RESULTS = results;\n      renderCompareTable(results);"

new_content = pattern.sub(replacer, content)

if new_content != content:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Injected Save button successfully")
else:
    print("Save button injection failed or already exists")
