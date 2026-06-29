with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    line_num = i + 1
    # Line numbers from previous view_file:
    # 3129: window._IS_VIRTUAL_MODE = false;
    # 3130: function toggleVirtualMode()
    # 3133: }
    # 3134: function getVirtualPortfolio()
    # 3405: }
    # We want to keep lines up to 3133. Drop 3134 to 3405.
    
    if 3134 <= line_num <= 3405:
        continue
    new_lines.append(line)

with open("index.html", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Duplicates removed.")
