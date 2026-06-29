with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

target = "const reinvestCF = (netProc * 1000) * (reinvestRate / 100) / 12;"
repl = "const reinvestRate = 8;\n            const reinvestCF = (netProc * 1000) * (reinvestRate / 100) / 12;"

if target in content:
    content = content.replace(target, repl)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed reinvestRate error")
else:
    print("Target not found")
