#!/usr/bin/env python3
"""
Servidor HTTP simple que responde Hola Mundo
"""
import http.server
import socketserver
import sys
import os
import json
from datetime import datetime

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

PORT = 3000

# Configuración de base de datos desde variables de entorno
DB_HOST = os.environ.get('DATABASE_HOST', 'mi-postgres-postgresql-primary.hoverdev-dev.svc.cluster.local')
DB_PORT = os.environ.get('DATABASE_PORT', '5432')
DB_NAME = os.environ.get('DATABASE_NAME', 'postgres')
DB_USER = os.environ.get('DATABASE_USER', 'postgres')
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD', '')

def get_users():
    """Conecta a PostgreSQL y obtiene los usuarios"""
    if not POSTGRES_AVAILABLE:
        return {"error": "psycopg2 no está instalado"}
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users")
        rows = cursor.fetchall()
        users = [{"id": row[0], "name": row[1]} for row in rows]
        cursor.close()
        conn.close()
        return {"users": users}
    except Exception as e:
        return {"error": str(e)}

class HolaMundoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Solicitud GET recibida PEPITO", file=sys.stdout)
        print(f"[{timestamp}] Path: {self.path}", file=sys.stdout)
        
        if self.path == '/startup':
            print(f"[{timestamp}] se llamo al endpoints /startup", file=sys.stdout)
            sys.stdout.flush()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'OK')
        elif self.path == '/liveness':
            print(f"[{timestamp}] se llamo al endpoints /liveness", file=sys.stdout)
            sys.stdout.flush()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'OK')
        elif self.path == '/readiness':
            print(f"[{timestamp}] se llamo al endpoints /readiness", file=sys.stdout)
            sys.stdout.flush()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'OK')
        elif self.path == '/users':
            print(f"[{timestamp}] se llamo al endpoints /users", file=sys.stdout)
            sys.stdout.flush()
            result = get_users()
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
        else:
            print(f"[{timestamp}] se llamo al endpoints raiz", file=sys.stdout)
            sys.stdout.flush()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<h1>Hola Mundo</h1>')
    
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} - {format%args}", file=sys.stdout)
        sys.stdout.flush()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), HolaMundoHandler) as httpd:
        print(f"Servidor corriendo en puerto {PORT}")
        print("Presiona Ctrl+C para detener")
        httpd.serve_forever()
