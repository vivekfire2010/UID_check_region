# api/region.py

from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import requests

def get_player_info(Id):    
    url = "https://shop2game.com/api/auth/player_id_login"
    headers = {
        # ... [keep your headers the same] ...
    }
    payload = {
        "app_id": 100067,
        "login_id": f"{Id}",
        "app_server_id": 0,
    }
    response = requests.post(url, headers=headers, json=payload)
    return response

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        uid = query.get("uid", [None])[0]

        if not uid:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Please provide a UID"}).encode())
            return

        response = get_player_info(uid)

        try:
            if response.status_code == 200:
                data = response.json()
                if not data.get('nickname') and not data.get('region'):
                    result = {"message": "UID not found, please check the UID"}
                else:
                    result = {
                        "uid": uid,
                        "nickname": data.get('nickname', ''),
                        "region": data.get('region', '')
                    }
            else:
                result = {"message": "UID not found, please check the UID"}
        except Exception:
            result = {"message": "UID not found, please check the UID"}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
      
