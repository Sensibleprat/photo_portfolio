#!/usr/bin/env python3
"""
Resilient Development HTTP Server
Handles concurrent local high-resolution image requests on macOS without
dropping connections due to socket buffer exhaustion (Errno 55: ENOBUFS).
"""

import sys
import os
import time
import errno
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(BASE_DIR, 'site')

class ResilientHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_DIR, **kwargs)

    def copyfile(self, source, outputfile):
        """Stream in 32KB chunks and handle socket buffer pressure gracefully on macOS"""
        bufsize = 32 * 1024
        while True:
            buf = source.read(bufsize)
            if not buf:
                break
            for attempt in range(10):
                try:
                    outputfile.write(buf)
                    break
                except OSError as e:
                    # Errno 55 is ENOBUFS ("No buffer space available" on macOS)
                    if e.errno in (errno.ENOBUFS, getattr(errno, 'EAGAIN', 35), getattr(errno, 'EWOULDBLOCK', 35)):
                        time.sleep(0.02 * (attempt + 1))
                    else:
                        raise

    def log_message(self, format, *args):
        # Only log non-200 / non-304 responses to keep logs clean
        if len(args) > 1 and str(args[1]) not in ('200', '304'):
            super().log_message(format, *args)

def run(port=8000):
    server_address = ('', port)
    ThreadingHTTPServer.allow_reuse_address = True
    httpd = ThreadingHTTPServer(server_address, ResilientHandler)
    print(f"Resilient server listening on http://localhost:{port} (serving {SITE_DIR})")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run(port)
