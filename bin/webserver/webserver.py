import http.server
import os
import socketserver

PORT = 8080

web_dir = os.path.join('logs')
os.chdir(web_dir)
Handler = http.server.SimpleHTTPRequestHandler


def run_webserver():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()(("", PORT), Handler)


if __name__ == '__main__':
    run_webserver()
