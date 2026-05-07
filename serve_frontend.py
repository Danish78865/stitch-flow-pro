#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend files
"""

import http.server
import socketserver
import os
import webbrowser
from threading import Timer

# Set the port
PORT = 3000

# Change to the current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Redirect to index.html if root is requested
        if self.path == '/':
            self.path = '/index.html'
        
        # Add CORS headers
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        # Serve the file
        try:
            with open(self.path[1:], 'rb') as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404, "File Not Found")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Frontend server running at http://localhost:{PORT}")
        print(f"📁 Serving files from: {os.getcwd()}")
        print(f"🔗 Backend API running at: http://localhost:8000")
        print(f"🌐 Open your browser and navigate to: http://localhost:{PORT}/login.html")
        print("Press Ctrl+C to stop the server")
        
        # Open browser after a short delay
        def open_browser():
            webbrowser.open(f'http://localhost:{PORT}/login.html')
        
        Timer(1.5, open_browser).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
