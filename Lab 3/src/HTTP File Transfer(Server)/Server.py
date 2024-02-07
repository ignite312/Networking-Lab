import http.server
import socketserver
import os

class FileServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get the requested file path from the URL
            file_path = self.translate_path(self.path)
            
            # Check if the file exists
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Set headers
                self.send_response(200)
                self.send_header("Content-type", "application/octet-stream")
                self.send_header("Content-Disposition", f"attachment; filename=\"{os.path.basename(file_path)}\"")
                self.end_headers()
                
                # Open the file and send its contents to the client
                with open(file_path, "rb") as file:
                    self.wfile.write(file.read())
            else:
                # If the file does not exist, send a 404 error
                self.send_error(404, "File Not Found")
        except Exception as e:
            # If any error occurs, send a 500 error
            self.send_error(500, f"Internal Server Error: {e}")

#Connection
HOST_IP = '192.168.0.101'
HOST_PORT = 12346

with socketserver.TCPServer((HOST_IP, HOST_PORT), FileServer) as httpd:
    print(f"Server started on port {HOST_PORT}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
