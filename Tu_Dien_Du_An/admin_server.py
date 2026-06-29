"""
Admin Server - Chạy lệnh: python admin_server.py
Sau đó mở: http://localhost:8001/admin.html
"""
import json
import re
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.stdout.reconfigure(encoding='utf-8')

DATA_JS_PATH = 'data.js'

def read_projects():
    """Đọc data.js và trả về list dự án dạng Python dict bằng cách dùng regex quét từng trường (hỗ trợ JS syntax)."""
    try:
        with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            
        start_match = re.search(r'const\s+projectsData\s*=\s*\[', content)
        if not start_match:
            return []
            
        start_idx = start_match.end() - 1
        depth = 0
        end_idx = start_idx
        for i, ch in enumerate(content[start_idx:]):
            if ch == '[': depth += 1
            elif ch == ']': depth -= 1
            if depth == 0:
                end_idx = start_idx + i + 1
                break
                
        projects_block = content[start_idx:end_idx]
        
        projects = []
        idx = 0
        while True:
            start_obj = projects_block.find('{', idx)
            if start_obj == -1:
                break
            
            # Tìm ngoặc đóng tương ứng
            obj_depth = 0
            end_obj = -1
            for i in range(start_obj, len(projects_block)):
                if projects_block[i] == '{':
                    obj_depth += 1
                elif projects_block[i] == '}':
                    obj_depth -= 1
                    if obj_depth == 0:
                        end_obj = i + 1
                        break
            
            if end_obj == -1:
                break
                
            obj_text = projects_block[start_obj:end_obj]
            
            # Dùng regex trích xuất các trường cơ bản
            def get_field(field_name):
                # Hỗ trợ cả nháy đơn, nháy kép, và backticks cho values, đồng thời hỗ trợ key có hoặc không có ngoặc kép
                m = re.search(r"['\"]?" + field_name + r"['\"]?\s*:\s*['\"`](.*?)['\"`]", obj_text)
                if m:
                    return m.group(1).strip()
                # Đối với số (như lat, lng)
                m = re.search(r"['\"]?" + field_name + r"['\"]?\s*:\s*([0-9.-]+)", obj_text)
                if m:
                    try:
                        return float(m.group(1))
                    except:
                        return m.group(1)
                return None

            proj_id = get_field('id')
            if proj_id:
                m_v = re.search(r"['\"]?verified['\"]?\s*:\s*(true|false)", obj_text, re.IGNORECASE)
                verified = True if (m_v and m_v.group(1).lower() == 'true') else False
                
                projects.append({
                    'id': proj_id,
                    'name': get_field('name') or 'Không tên',
                    'location': get_field('location') or '',
                    'lat': get_field('lat'),
                    'lng': get_field('lng'),
                    'developer': get_field('developer') or '',
                    'status': get_field('status') or '',
                    'verified': verified
                })
                
            idx = end_obj
            
        return projects
    except Exception as e:
        print(f"Lỗi đọc dự án: {e}")
        return []

def update_project_coords_in_file(proj_id, new_lat, new_lng):
    """Cập nhật trực tiếp tọa độ trong file data.js mà không làm mất comment hay thay đổi format của các phần khác (hỗ trợ cả JS và JSON syntax)."""
    try:
        with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        # Tìm vị trí bắt đầu của object dự án có id này
        # Hỗ trợ: id: 'abc', "id": "abc", 'id': 'abc'
        escaped_id = re.escape(proj_id)
        pattern = r"""(?:["']?id["']?\s*:\s*["'])""" + escaped_id + r"""["']"""
        match = re.search(pattern, content)
        if not match:
            print(f"[WARN] Khong tim thay id '{proj_id}' trong data.js")
            return False

        id_pos = match.start()
        
        # Tìm '{' ngược từ id_pos
        obj_start = content.rfind('{', 0, id_pos)
        if obj_start == -1:
            return False
            
        # Tìm '}' xuôi từ id_pos
        depth = 0
        obj_end = -1
        for i in range(obj_start, len(content)):
            if content[i] == '{':
                depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    obj_end = i + 1
                    break
                    
        if obj_end == -1:
            return False
            
        obj_content = content[obj_start:obj_end]
        
        # Thay thế hoặc chèn lat/lng
        lat_pattern = r"(['\"]?lat['\"]?\s*:\s*)[0-9.-]+"
        lng_pattern = r"(['\"]?lng['\"]?\s*:\s*)[0-9.-]+"
        
        # Kiểm tra xem có trường lat/lng trong object không
        has_lat = re.search(r"['\"]?lat['\"]?\s*:", obj_content)
        has_lng = re.search(r"['\"]?lng['\"]?\s*:", obj_content)
        
        # Xác định style nháy của id để giữ đồng bộ
        id_match = re.search(r"(['\"]?id['\"]?)\s*:", obj_content)
        id_quote = '"' if '"' in id_match.group(1) else "'" if "'" in id_match.group(1) else ""
        
        new_obj_content = obj_content
        
        # Xử lý LAT
        if has_lat:
            new_obj_content = re.sub(lat_pattern, r"\g<1>" + str(new_lat), new_obj_content)
        else:
            lat_key = f"{id_quote}lat{id_quote}: {new_lat}"
            id_value_pattern = r"(['\"]?id['\"]?\s*:\s*['\"].*?['\"])(,?)"
            new_obj_content = re.sub(id_value_pattern, r"\1,\n        " + lat_key + r"\2", new_obj_content)
            
        # Xử lý LNG
        if has_lng:
            new_obj_content = re.sub(lng_pattern, r"\g<1>" + str(new_lng), new_obj_content)
        else:
            lng_key = f"{id_quote}lng{id_quote}: {new_lng}"
            lat_value_pattern = r"(['\"]?lat['\"]?\s*:\s*[0-9.-]+)(,?)"
            new_obj_content = re.sub(lat_value_pattern, r"\1,\n        " + lng_key + r"\2", new_obj_content)
            
        # Ghi lại vào file
        new_file_content = content[:obj_start] + new_obj_content + content[obj_end:]
        with open(DATA_JS_PATH, 'w', encoding='utf-8') as f:
            f.write(new_file_content)
            
        return True
    except Exception as e:
        print(f"Lỗi cập nhật tọa độ: {e}")
        return False

def delete_project_in_file(proj_id):
    try:
        with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        escaped_id = re.escape(proj_id)
        pattern = r"""(?:["']?id["']?\s*:\s*["'])""" + escaped_id + r"""["']"""
        match = re.search(pattern, content)
        if not match: return False

        id_pos = match.start()
        obj_start = content.rfind('{', 0, id_pos)
        if obj_start == -1: return False
        
        depth = 0
        obj_end = -1
        for i in range(obj_start, len(content)):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    obj_end = i + 1
                    break
        if obj_end == -1: return False
        
        after_obj = content[obj_end:]
        m = re.match(r'\s*,', after_obj)
        if m:
            obj_end += m.end()
        else:
            before_obj = content[:obj_start]
            m2 = re.search(r',\s*$', before_obj)
            if m2:
                obj_start = m2.start()

        new_content = content[:obj_start] + content[obj_end:]
        with open(DATA_JS_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print("Lỗi xóa dự án:", e)
        return False

def update_project_details_in_file(proj_id, details):
    try:
        with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        escaped_id = re.escape(proj_id)
        pattern = r"""(?:["']?id["']?\s*:\s*["'])""" + escaped_id + r"""["']"""
        match = re.search(pattern, content)
        if not match: return False

        id_pos = match.start()
        obj_start = content.rfind('{', 0, id_pos)
        if obj_start == -1: return False
        
        depth = 0
        obj_end = -1
        for i in range(obj_start, len(content)):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    obj_end = i + 1
                    break
        if obj_end == -1: return False
        
        obj_content = content[obj_start:obj_end]
        
        for key, val in details.items():
            if val is None: continue
            # Handle empty string properly
            val_str = f"'{val}'" if isinstance(val, str) else str(val)
            key_pattern = r"(['\"]?" + re.escape(key) + r"['\"]?\s*:\s*)(['\"`].*?['\"`]|[0-9.-]+)"
            if re.search(key_pattern, obj_content):
                obj_content = re.sub(key_pattern, r"\g<1>" + val_str, obj_content)
            else:
                id_match = re.search(r"(['\"]?id['\"]?)\s*:", obj_content)
                id_quote = '"' if '"' in id_match.group(1) else "'" if "'" in id_match.group(1) else ""
                new_key_str = f"{id_quote}{key}{id_quote}: {val_str}"
                id_value_pattern = r"(['\"]?id['\"]?\s*:\s*['\"].*?['\"])(,?)"
                obj_content = re.sub(id_value_pattern, r"\1,\n        " + new_key_str + r"\2", obj_content)
                
        new_content = content[:obj_start] + obj_content + content[obj_end:]
        with open(DATA_JS_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print("Lỗi update details:", e)
        return False

def verify_project_in_file(proj_id):
    try:
        with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        escaped_id = re.escape(proj_id)
        pattern = r"""(?:["']?id["']?\s*:\s*["'])""" + escaped_id + r"""["']"""
        match = re.search(pattern, content)
        if not match: return False

        id_pos = match.start()
        obj_start = content.rfind('{', 0, id_pos)
        if obj_start == -1: return False
        
        depth = 0
        obj_end = -1
        for i in range(obj_start, len(content)):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    obj_end = i + 1
                    break
        if obj_end == -1: return False
        
        obj_content = content[obj_start:obj_end]
        
        key_pattern = r"(['\"]?verified['\"]?\s*:\s*)(true|false)"
        if re.search(key_pattern, obj_content):
            obj_content = re.sub(key_pattern, r"\g<1>true", obj_content)
        else:
            id_match = re.search(r"(['\"]?id['\"]?)\s*:", obj_content)
            id_quote = '"' if '"' in id_match.group(1) else "'" if "'" in id_match.group(1) else ""
            new_key_str = f"{id_quote}verified{id_quote}: true"
            id_value_pattern = r"(['\"]?id['\"]?\s*:\s*['\"].*?['\"])(,?)"
            obj_content = re.sub(id_value_pattern, r"\1,\n        " + new_key_str + r"\2", obj_content)
                
        new_content = content[:obj_start] + obj_content + content[obj_end:]
        with open(DATA_JS_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print("Lỗi verify project:", e)
        return False

class AdminHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print("[HTTP]", self.address_string(), format % args)  # Bat log de debug

    def do_GET(self):
        parsed = urlparse(self.path)
        
        # API lấy danh sách dự án (bây giờ dùng regex cực kỳ an toàn)
        if parsed.path == '/api/projects':
            projects = read_projects()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(projects, ensure_ascii=False).encode('utf-8'))
            return
        
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        
        # API cập nhật tọa độ
        if parsed.path == '/api/update_coords':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode('utf-8'))
            
            proj_id = data.get('id')
            new_lat = data.get('lat')
            new_lng = data.get('lng')
            
            success = update_project_coords_in_file(proj_id, new_lat, new_lng)
            
            if success:
                print(f"OK saved: {proj_id} => {new_lat}, {new_lng}")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
            else:
                print(f"[ERR] update FAILED for proj_id='{proj_id}'")
                self.send_response(404)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "not_found"}')
            return

        # API cập nhật nội dung
        if parsed.path == '/api/update_project':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode('utf-8'))
            proj_id = data.get('id')
            details = {
                'name': data.get('name'),
                'location': data.get('location'),
                'developer': data.get('developer'),
                'status': data.get('status')
            }
            success = update_project_details_in_file(proj_id, details)
            if success:
                print(f"OK updated details: {proj_id}")
            else:
                print(f"[ERR] update details FAILED: {proj_id}")
            self.send_response(200 if success else 400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok' if success else 'error'}).encode('utf-8'))
            return

        # API xóa dự án
        if parsed.path == '/api/delete_project':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode('utf-8'))
            proj_id = data.get('id')
            success = delete_project_in_file(proj_id)
            if success:
                print(f"OK deleted: {proj_id}")
            else:
                print(f"[ERR] delete FAILED: {proj_id}")
            self.send_response(200 if success else 400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok' if success else 'error'}).encode('utf-8'))
            return
            
        # API verify dự án
        if parsed.path == '/api/verify_project':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode('utf-8'))
            proj_id = data.get('id')
            success = verify_project_in_file(proj_id)
            if success:
                print(f"OK verified: {proj_id}")
            else:
                print(f"[ERR] verify FAILED: {proj_id}")
            self.send_response(200 if success else 400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok' if success else 'error'}).encode('utf-8'))
            return
        
        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    port = 8001
    server = HTTPServer(('localhost', port), AdminHandler)
    print(f"🚀 Admin Server đang chạy tại: http://localhost:{port}/admin.html")
    print("📝 Bấm Ctrl+C để dừng server.")
    server.serve_forever()
