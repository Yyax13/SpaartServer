import http.server
import socketserver
import random
from libs.color import *

tagn1 = f"{c.cyan('[')}{c.yellow('1')}{c.cyan(']')}"
tagn2 = f"{c.cyan('[')}{c.yellow('2')}{c.cyan(']')}"
hashtag = f"{c.cyan('[')}{c.yellow('#')}{c.cyan(']')}"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        request_info = f"{c.yellow('<--')} {c.yellow('|')} {c.cyan('Request Code')} {c.yellow('|')} {c.purple('IP')} {c.yellow('|')} {c.yellow('-->')}"
        
        request_line = f"{c.yellow('<--')} | {c.cyan(format % args)} | {c.green(self.headers.get('User-Agent', 'Unknown').split('(')[0].strip())} | {c.purple(self.client_address[0])} | {c.yellow('-->')}"
        print(request_line)


port_choose = input(f"""
    {tagn1} {c.cyan('Random Port')}
    {tagn2} {c.cyan('Choose Port')}

    {hashtag} {c.cyan('Choose one')}: """)

if port_choose == "1":
    port = random.randint(10024, 80000)
elif port_choose == "2":
    port = int(input(f'    {hashtag} {c.cyan("Choose a port (more than 1024): ")}'))
    if port <= 1024:
        print(f"{c.red('Invalid port number!')} Please choose a port greater than 1024.")
        exit(1)
else:
    print(f"{c.red('Invalid choice!')} Exiting...")
    exit(1)

handler = CustomHTTPRequestHandler 

with socketserver.TCPServer(("", port), handler) as httpd:
    print(f"Servidor rodando em http://localhost:{port}")
    httpd.serve_forever()
