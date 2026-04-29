#!/usr/bin/env python3
"""
Servidor Python para sincronização do Lisnave Gas Tracker
Alternativa ao Node.js se não tiver Node.js instalado
"""

import http.server
import socketserver
import json
import sqlite3
import threading
import time
from urllib.parse import urlparse, parse_qs
import os

# Database setup
DB_FILE = 'lisnave_data.db'

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cylinders (
            id TEXT PRIMARY KEY,
            type TEXT,
            zoneId TEXT,
            lat REAL,
            lng REAL,
            status TEXT,
            ts TEXT,
            worker TEXT,
            pres INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default workers if empty
    cursor.execute("SELECT COUNT(*) FROM workers")
    if cursor.fetchone()[0] == 0:
        default_workers = ['J. Ferreira','M. Santos','R. Costa','A. Lopes','C. Mendes','P. Sousa']
        for worker in default_workers:
            cursor.execute("INSERT INTO workers (name) VALUES (?)", (worker,))
    
    conn.commit()
    conn.close()

# WebSocket clients storage
websocket_clients = []

def broadcast_to_all(message):
    """Broadcast message to all connected WebSocket clients"""
    msg = json.dumps(message)
    for client in websocket_clients[:]:
        try:
            client.send(msg)
        except:
            websocket_clients.remove(client)

def load_all_data():
    """Load all data from database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cylinders ORDER BY created_at")
    cylinders = []
    for row in cursor.fetchall():
        cylinders.append({
            'id': row[0], 'type': row[1], 'zoneId': row[2], 'lat': row[3], 'lng': row[4],
            'status': row[5], 'ts': row[6], 'worker': row[7], 'pres': row[8]
        })
    
    cursor.execute("SELECT name FROM workers ORDER BY name")
    workers = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return {'cylinders': cylinders, 'workers': workers}

class WebSocketHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        # Serve static files
        if parsed.path in ['/', '/index.html']:
            self.serve_file('index.html')
        elif parsed.path == '/index_sync.html':
            self.serve_file('index_sync.html')
        elif parsed.path.startswith('/api/'):
            self.handle_api_get()
        else:
            # Try to serve static file
            self.serve_static(parsed.path[1:])
    
    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith('/api/'):
            self.handle_api_post()
        else:
            self.send_error(404)
    
    def do_PUT(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith('/api/'):
            self.handle_api_put()
        else:
            self.send_error(404)
    
    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith('/api/'):
            self.handle_api_delete()
        else:
            self.send_error(404)
    
    def serve_file(self, filename):
        """Serve a file"""
        try:
            with open(filename, 'rb') as f:
                content = f.read()
            
            content_type = 'text/html'
            if filename.endswith('.js'):
                content_type = 'application/javascript'
            elif filename.endswith('.css'):
                content_type = 'text/css'
            elif filename.endswith('.json'):
                content_type = 'application/json'
            elif filename.endswith('.png'):
                content_type = 'image/png'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)
    
    def serve_static(self, filename):
        """Serve static files with proper content types"""
        if os.path.exists(filename):
            self.serve_file(filename)
        else:
            self.send_error(404)
    
    def handle_api_get(self):
        """Handle GET requests to API"""
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/cylinders':
            data = load_all_data()
            self.send_json_response(data['cylinders'])
        elif parsed.path == '/api/workers':
            data = load_all_data()
            self.send_json_response(data['workers'])
        else:
            self.send_error(404)
    
    def handle_api_post(self):
        """Handle POST requests to API"""
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/cylinders':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            cylinder = json.loads(post_data.decode('utf-8'))
            
            # Save to database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO cylinders 
                (id, type, zoneId, lat, lng, status, ts, worker, pres, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                cylinder['id'], cylinder['type'], cylinder['zoneId'], cylinder['lat'], cylinder['lng'],
                cylinder['status'], cylinder['ts'], cylinder['worker'], cylinder['pres']
            ))
            conn.commit()
            conn.close()
            
            # Broadcast to all clients
            data = load_all_data()
            broadcast_to_all({'type': 'dataUpdate', 'data': data})
            
            self.send_json_response({'success': True, 'cylinder': cylinder})
        else:
            self.send_error(404)
    
    def handle_api_put(self):
        """Handle PUT requests to API"""
        parsed = urlparse(self.path)
        path_parts = parsed.path.split('/')
        
        if len(path_parts) == 4 and path_parts[2] == 'cylinders':
            cylinder_id = path_parts[3]
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            cylinder = json.loads(put_data.decode('utf-8'))
            
            # Update in database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE cylinders SET 
                type=?, zoneId=?, lat=?, lng=?, status=?, ts=?, worker=?, pres=?, updated_at=CURRENT_TIMESTAMP 
                WHERE id=?
            ''', (
                cylinder['type'], cylinder['zoneId'], cylinder['lat'], cylinder['lng'],
                cylinder['status'], cylinder['ts'], cylinder['worker'], cylinder['pres'], cylinder_id
            ))
            conn.commit()
            conn.close()
            
            # Broadcast to all clients
            data = load_all_data()
            broadcast_to_all({'type': 'dataUpdate', 'data': data})
            
            self.send_json_response({'success': True, 'cylinder': cylinder})
        else:
            self.send_error(404)
    
    def handle_api_delete(self):
        """Handle DELETE requests to API"""
        parsed = urlparse(self.path)
        path_parts = parsed.path.split('/')
        
        if len(path_parts) == 4 and path_parts[2] == 'cylinders':
            cylinder_id = path_parts[3]
            
            # Delete from database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cylinders WHERE id=?", (cylinder_id,))
            conn.commit()
            conn.close()
            
            # Broadcast to all clients
            data = load_all_data()
            broadcast_to_all({'type': 'dataUpdate', 'data': data})
            
            self.send_json_response({'success': True})
        else:
            self.send_error(404)
    
    def send_json_response(self, data):
        """Send JSON response"""
        response = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-length', len(response))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response)

def run_server():
    """Run the HTTP server"""
    PORT = 8080
    
    # Initialize database
    init_db()
    
    # Create server
    handler = WebSocketHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Lisnave Gas Tracker Server (Python) running on port {PORT}")
        print(f"Access: http://localhost:{PORT}")
        print(f"Ready for real-time sync")
        print(f"Database: {os.path.abspath(DB_FILE)}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    run_server()
