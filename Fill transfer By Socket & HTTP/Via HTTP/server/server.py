from http.server import BaseHTTPRequestHandler, HTTPServer

class get_post_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            file_path = self.path[1:]
            with open(file_path, 'rb') as file:
                self.send_response(200)
                self.send_header("Content-type", "application/octet-stream")
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, 'File Not Found')

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        file_content = self.rfile.read(length)

        file_name = self.path[1:]
        with open(file_name, 'wb') as file:
            file.write(file_content)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('File uploaded successfully'.encode())

def start_server(port):
    server = HTTPServer(('', port), get_post_handler)
    print(f"HTTP server listening on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    port = 8080
    start_server(port)
