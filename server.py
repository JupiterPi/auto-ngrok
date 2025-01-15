from http.server import BaseHTTPRequestHandler, HTTPServer
import ngrok
import os
import re
from datetime import datetime

def main():

    # get specified domain for HTTP tunnel from environment variable
    http_domain = os.getenv("AUTO_NGROK_DOMAIN")
    if http_domain is None:
        print("AUTO_NGROK_DOMAIN environment variable not set")
        exit(1)

    # start ngrok HTTP tunnel for HTTP server
    http_listener = ngrok.forward(8000, domain=http_domain, authtoken_from_env=True)
    print(f"HTTP tunnel listening at {http_listener.url()}")

    # start ngrok SSH tunnel
    ssh_listener = ngrok.forward(22, "tcp", authtoken_from_env=True)
    print(f"SSH tunnel listening at {ssh_listener.url()}")

    # construct page
    webpage_path = os.path.join(os.path.dirname(__file__), "webpage.html")
    html_page = open(webpage_path, "r").read()
    html_page = html_page.replace("{{ device }}", os.uname().nodename)
    url_parts = re.search("^tcp://(.*):(\\d+)$", ssh_listener.url())
    html_page = html_page.replace("{{ url }}", url_parts.group())
    html_page = html_page.replace("{{ domain }}", url_parts.group(1))
    html_page = html_page.replace("{{ port }}", url_parts.group(2))

    # HTTP server to fetch SSH tunnel url
    class AutoNgrokServer(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.wfile.write(html_page.replace("{{ timestamp }}", timestamp).encode())
    server = HTTPServer(("localhost", 8000), AutoNgrokServer)

    # run server
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    print("Closing")
    server.server_close()

if __name__ == "__main__":
    main()