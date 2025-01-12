from http.server import BaseHTTPRequestHandler, HTTPServer
import ngrok
import time
import os

# get specified domain for HTTP tunnel from environment variable
http_domain = os.getenv('AUTO_NGROK_DOMAIN')
if http_domain is None:
    print('AUTO_NGROK_DOMAIN environment variable not set')
    exit(1)

# start ngrok HTTP tunnel for HTTP server
http_listener = ngrok.forward(8000, domain=http_domain, authtoken_from_env=True)
print(f'HTTP tunnel listening at {http_listener.url()}')

# start ngrok SSH tunnel
ssh_listener = ngrok.forward(22, 'tcp', authtoken_from_env=True)
print(f'SSH tunnel listening at {ssh_listener.url()}')

# HTTP server to fetch SSH tunnel url
class AutoNgrokServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(f'<html><body>SSH tunnel url: {ssh_listener.url()}</body></html>'.encode())
server = HTTPServer(('localhost', 8000), AutoNgrokServer)

# run server
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
print('Closing')
server.server_close()
