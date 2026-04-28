#!/usr/bin/env python3
"""
Servidor HTTPS com certificado auto-assinado para PWA
Uso: python servidor_seguro.py
"""

import http.server
import ssl
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuração
PORT = 8443
CERT_FILE = "localhost.crt"
KEY_FILE = "localhost.key"

def gerar_certificado():
    """Gera certificado auto-assinado se não existir"""
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print("🔐 Gerando certificado SSL auto-assinado...")
        import subprocess
        
        # Comando OpenSSL para gerar certificado
        cmd = [
            'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
            '-keyout', KEY_FILE, '-out', CERT_FILE,
            '-days', '365', '-nodes',
            '-subj', '/C=PT/ST=Setubal/L=Setubal/O=Lisnave/OU=IT/CN=localhost'
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print("✅ Certificado gerado com sucesso!")
        except subprocess.CalledProcessError:
            print("❌ Erro ao gerar certificado. Instale OpenSSL:")
            print("   Windows: https://slproweb.com/products/Win32OpenSSL.html")
            print("   Ou use chocolatey: choco install openssl")
            return False
        except FileNotFoundError:
            print("❌ OpenSSL não encontrado. Por favor instale OpenSSL.")
            return False
    return True

def verificar_ip():
    """Retorna o IP local da máquina"""
    import socket
    try:
        # Conectar a um DNS para obter IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=".", **kwargs)
    
    def end_headers(self):
        # Headers para PWA
        self.send_header('Service-Worker-Allowed', '/')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Logs mais limpos
        print(f"📱 {self.address_string()} - {format % args}")

def main():
    print("🚀 Iniciando Servidor HTTPS para PWA Lisnave")
    print("=" * 50)
    
    # Verificar se estamos na pasta correta
    if not Path("index.html").exists():
        print("❌ Erro: index.html não encontrado nesta pasta!")
        print("   Execute este script na pasta: c:\\Users\\andre.bras\\Desktop\\ant")
        return
    
    # Gerar certificado
    if not gerar_certificado():
        return
    
    # Obter IP
    ip_local = verificar_ip()
    
    # Configurar servidor
    Handler = CustomHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            # Configurar SSL
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            
            print(f"✅ Servidor iniciado com sucesso!")
            print(f"🌐 URLs disponíveis:")
            print(f"   Local: https://localhost:{PORT}")
            print(f"   Rede: https://{ip_local}:{PORT}")
            print()
            print("📱 Para instalar no telemóvel:")
            print(f"   1. Conecte o telemóvel à mesma WiFi")
            print(f"   2. Abra no browser: https://{ip_local}:{PORT}")
            print("   3. Aceite o certificado (avançado → prosseguir)")
            print("   4. Click em 'Instalar app' ou 'Adicionar ao ecrã inicial'")
            print()
            print("⚠️  Aviso: O certificado é auto-assinado, precisará aceitar o risco")
            print("🛑 Para parar: Ctrl+C")
            print("=" * 50)
            
            # Tentar abrir browser automaticamente
            try:
                webbrowser.open(f"https://localhost:{PORT}")
            except:
                pass
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Porta {PORT} já está em uso!")
            print(f"   Tente: netstat -ano | findstr :{PORT}")
            print(f"   Ou use outra porta editando PORT = {PORT}")
        else:
            print(f"❌ Erro: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
