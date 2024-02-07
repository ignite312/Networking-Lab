import http.server
import socketserver
import os

class FileServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            file_path = self.translate_path(self.path)
            
            # Check if the file exists
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Set headers
                self.send_response(200)
                self.send_header("Content-type", "application/octet-stream")
                self.send_header("Content-Disposition", f"attachment; filename=\"{os.path.basename(file_path)}\"")
                self.end_headers()
                
                with open(file_path, "rb") as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, "File Not Found")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {e}")
            
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            
            file_name = self.headers['File-Name']
            file_path = os.path.join(os.getcwd(), "Files/" + file_name)
            
            with open(file_path, 'wb') as f:
                f.write(data)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'File uploaded successfully.')
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {e}")

#Connection
HOST_IP = '192.168.0.101'
HOST_PORT = 12347

with socketserver.TCPServer((HOST_IP, HOST_PORT), FileServer) as httpd:
    print(f"Server started on port {HOST_PORT}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")