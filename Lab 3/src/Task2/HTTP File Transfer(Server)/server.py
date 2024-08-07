import http.server
import socketserver
import os
import threading

# Define the Folder Name where the Incoming file from Client will be stored
path = 'FilesFromClient'
try:
    os.makedirs(path)
except FileExistsError:
    pass

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

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
            data = self.rfile.read(int(self.headers['Content-Length']))
            # data = self.rfile.read(content_length)
            
            file_name = self.headers['File-Name']
            file_path = os.path.join(os.getcwd(), "FilesFromClient/" + file_name)
            
            with open(file_path, 'wb') as f:
                f.write(data)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'File uploaded successfully.')
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {e}")

# Connection
HOST_IP = '192.168.0.100'
HOST_PORT = 12348

# Create a threaded server
server = ThreadedHTTPServer((HOST_IP, HOST_PORT), FileServer)

print(f"Server started on port {HOST_PORT}")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Server stopped.")
    server.shutdown()
