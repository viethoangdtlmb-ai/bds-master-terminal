"""
Update Quick-Load templates
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    v = f.read()

# 1. Replace Buttons
old_buttons_start = v.find('<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:24px" id="templates-row">')
old_buttons_end = v.find('</div>', old_buttons_start + 50) + 6

new_buttons = '''<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:24px" id="templates-row">
      <button class="btn btn-secondary btn-sm" onclick="loadTemplate('chungcu', event)">🏢 Chung cư</button>
      <button class="btn btn-secondary btn-sm" onclick="loadTemplate('shophouse', event)">🏬 Shophouse</button>
      <button class="btn btn-secondary btn-sm" onclick="loadTemplate('bietthu', event)">🏡 Biệt thự - Liền kề</button>
      <button class="btn btn-secondary btn-sm" onclick="loadTemplate('datnen', event)">🏜️ Đất nền vùng ven</button>
      <button class="btn btn-secondary btn-sm" onclick="loadTemplate('nghiduong', event)">🏖️ BĐS nghỉ dưỡng</button>
      <button class="btn btn-secondary btn-sm" onclick="loadTemplate('vanphong', event)">💼 Văn phòng cho thuê</button>
    </div>'''

if old_buttons_start != -1:
    v = v[:old_buttons_start] + new_buttons + v[old_buttons_end:]
    print('✅ Replaced buttons')

# 2. Replace TEMPLATES object
old_templates_start = v.find('const TEMPLATES = {')
if old_templates_start == -1: old_templates_start = v.find('var TEMPLATES = {')
old_templates_end = v.find('};', old_templates_start) + 2

new_templates = '''const TEMPLATES = {
  chungcu:   { name:'Chung Cư Tiết Kiệm', type:'chung-cu', district:'Hà Đông', area:68, year:2020, cost:3.2, market:3.8, goal:'cho-thue', loanpct:70, debt:1.8, rate:7.5, prefmonths:2, floatrate:12.5, grace:0, loanterm:20, rentstatus:'dang-thue', rent:12, mgmt:2, maint:8, delivery:0, rentExpected:0 },
  shophouse: { name:'Shophouse Làng Vân', type:'shophouse', district:'Hoài Đức', area:80, year:2022, cost:9, market:8.5, goal:'cho-thue', loanpct:60, debt:4.8, rate:8.5, prefmonths:6, floatrate:13, grace:8, loanterm:18, rentstatus:'dang-thue', rent:20, mgmt:3.5, maint:15, delivery:0, rentExpected:0 },
  bietthu:   { name:'Biệt Thự Vườn', type:'biet-thu', district:'Nam Từ Liêm', area:200, year:2019, cost:15, market:22, goal:'tu-o', loanpct:50, debt:5, rate:8.0, prefmonths:0, floatrate:13, grace:0, loanterm:15, rentstatus:'trong', rent:0, mgmt:5, maint:20, delivery:0, rentExpected:0 },
  datnen:    { name:'Đất Nền Bắc Quốc Oai', type:'dat-nen', district:'Thạch Thất', area:120, year:2021, cost:3.5, market:3.2, goal:'tang-gia', loanpct:50, debt:1.5, rate:9, prefmonths:3, floatrate:13.5, grace:0, loanterm:15, rentstatus:'trong', rent:0, mgmt:0, maint:5, delivery:0, rentExpected:0 },
  nghiduong: { name:'Villa Biển Nghỉ Dưỡng', type:'biet-thu', district:'', area:250, year:2018, cost:12, market:11, goal:'cho-thue', loanpct:60, debt:6, rate:8.5, prefmonths:0, floatrate:14, grace:0, loanterm:10, rentstatus:'dang-thue', rent:35, mgmt:12, maint:30, delivery:0, rentExpected:0 },
  vanphong:  { name:'Sàn Văn Phòng HH', type:'nha-rieng', district:'Cầu Giấy', area:150, year:2016, cost:8, market:10, goal:'cho-thue', loanpct:40, debt:1.5, rate:9, prefmonths:0, floatrate:12.5, grace:0, loanterm:10, rentstatus:'dang-thue', rent:45, mgmt:8, maint:15, delivery:0, rentExpected:0 }
};'''

if old_templates_start != -1:
    v = v[:old_templates_start] + new_templates + v[old_templates_end:]
    print('✅ Replaced TEMPLATES object')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(v)
