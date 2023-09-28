import http.server
import socketserver
import random
import subprocess
from libs.color import *

tagn1 = f"{c.cyan('[')}{c.yellow('1')}{c.cyan(']')}"
tagn2 = f"{c.cyan('[')}{c.yellow('2')}{c.cyan(']')}"
hashtag = f"{c.cyan('[')}{c.yellow('#')}{c.cyan(']')}"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        request_info = f"{c.yellow('<--')} {c.yellow('|')} {c.cyan('Request Code')} {c.yellow('|')} {c.purple('IP')} {c.yellow('|')} {c.yellow('-->')}"
        
        request_line = f"{c.yellow('<--')} | {c.cyan(format % args)} | {c.green(self.headers.get('User-Agent', 'Unknown').split('(')[0].strip())} | {c.purple(self.client_address[0])} | {c.yellow('-->')}"
        print(request_line)

    def do_GET(self):
        if self.path.endswith('.php'):
            # Se a solicitação é para um arquivo PHP, execute-o usando o interpretador PHP
            try:
                output = subprocess.check_output(['php', self.path], stderr=subprocess.STDOUT, universal_newlines=True)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(output.encode())
            except subprocess.CalledProcessError as e:
                # Se ocorrer um erro ao executar o PHP, retorne um código de erro
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"Erro ao executar o PHP: {e.output}".encode())
        else:
            # Se não for um arquivo PHP, deixe o tratamento padrão lidar com a solicitação
            super().do_GET()

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
