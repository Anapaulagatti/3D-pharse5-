#!/usr/bin/env python3
"""Serve the saved showcase on this computer and open its real browser view."""
import argparse
import errno
import functools
import http.server
import pathlib
import threading
import webbrowser


def main():
    parser = argparse.ArgumentParser(description="View the existing Korean Arena v0.3 showcase through HTTP.")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--no-browser", action="store_true", help="Do not open a browser automatically")
    args = parser.parse_args()
    directory = pathlib.Path(__file__).resolve().parent
    if not (directory / "index.html").is_file():
        parser.error("index.html must be next to start.py; extract the complete ZIP first")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as error:
        if error.errno != errno.EADDRINUSE:
            raise
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    address = f"http://127.0.0.1:{server.server_port}/"
    print(f"Korean Arena v0.3 — browser view on this computer: {address}", flush=True)
    print("Keep this window open. Press Ctrl+C to stop. No Node, Blender or internet needed.", flush=True)
    if not args.no_browser:
        timer = threading.Timer(0.3, webbrowser.open, args=(address,))
        timer.daemon = True
        timer.start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShowcase stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
