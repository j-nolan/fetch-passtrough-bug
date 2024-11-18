from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class ChunkedHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.headers.get('Content-Type') != 'text/plain':
            self.send_error(400, "Invalid Content-Type. Expected 'text/plain'")
            return

        filename = 'uploaded-file.txt'
        with open(filename, 'wb') as f:
            while True:
                chunk_size_line = self.rfile.readline().strip()
                chunk_size = int(chunk_size_line, 16)

                if chunk_size == 0:
                    break

                chunk = self.rfile.read(chunk_size)
                f.write(chunk)
                print(f"Wrote chunk of length {chunk_size}")

                # Read and discard the CRLF at the end of the chunk
                self.rfile.read(2)

        # Send response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"File '{filename}' uploaded successfully".encode('utf-8'))

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ChunkedHTTPRequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()