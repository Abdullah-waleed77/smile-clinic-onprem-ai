from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import urllib.request

PASSWORD = "CHANGE_ME"
OLLAMA = "http://127.0.0.1:11434/api/chat"

class Guard(BaseHTTPRequestHandler):

    # يعرض صفحة الشات
    def do_GET(self):
        if self.path in ("/", "/chat.html"):
            with open("chat.html", "rb") as f:
                page = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(page)
        else:
            self.send_error(404)

    # يستلم السؤال ويفحص كلمة السر
    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return

        if self.headers.get("X-API-Key") != PASSWORD:
            print("BLOCKED - wrong password from:", self.client_address[0])
            self.send_response(401)
            self.end_headers()
            return

        print("ALLOWED - request from:", self.client_address[0])
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as r:
            answer = r.read()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(answer)

print("Guard is running on port 8080")
ThreadingHTTPServer(("0.0.0.0", 8080), Guard).serve_forever()