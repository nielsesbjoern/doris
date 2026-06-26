#!/usr/bin/env python3
"""Local preview server with clean URLs (no .html suffix)."""
from __future__ import annotations

import http.server
import os
import socketserver
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PORT = int(os.environ.get("PORT", "8080"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path, _, qs = self.path.partition("?")
        path = unquote(path.split("#")[0])
        local = path.lstrip("/")
        if path in ("", "/"):
            self.path = "/index.html" + (f"?{qs}" if qs else "")
        elif not (ROOT / local).is_file() and (ROOT / f"{local}.html").is_file():
            self.path = f"/{local}.html" + (f"?{qs}" if qs else "")
        elif local.endswith("/") and (ROOT / local / "index.html").is_file():
            self.path = f"/{local}index.html" + (f"?{qs}" if qs else "")
        return super().do_GET()

    def log_message(self, fmt, *args):
        print(f"[dev] {args[0]} {args[1]} {args[2]}")


def main() -> None:
    os.chdir(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving Doris at http://localhost:{PORT}", flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
