from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
SITE = Path(__file__).parent / "site"
os.chdir(SITE)
print("Open http://127.0.0.1:8000/")
ThreadingHTTPServer(("127.0.0.1", 8000), SimpleHTTPRequestHandler).serve_forever()
