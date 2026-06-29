with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the bad </div>
bad_str = "</div><!-- End Hidden Combo A+B --><button class=\"btn btn-primary\" style=\"display:none !important\" onclick=\"runComboSim()\" "
good_str = "<button class=\"btn btn-primary\" style=\"display:none !important\" onclick=\"runComboSim()\" "
if bad_str in content:
    content = content.replace(bad_str, good_str)
    print("Fixed bad div")

# 2. Hide combo-sim-section
target_section = """<div class="card" style="margin-top:24px;border-color:rgba(168,85,247,.25)" id="combo-sim-section">"""
repl_section = """<div class="card" style="margin-top:24px;border-color:rgba(168,85,247,.25); display:none !important" id="combo-sim-section">"""
if target_section in content:
    content = content.replace(target_section, repl_section)
    print("Hid combo sim section")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
