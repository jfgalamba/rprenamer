#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

import random
import time


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    def __init__(
            self, server_address,
            handler_class=SimpleHTTPRequestHandler, 
            *args, 
            **kargs
    ):
        super().__init__(server_address, handler_class, *args, **kargs)
#:

class SimpleSlowHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(
            self, 
            *args, 
            random_wait=False,
            secs=5,
            **kargs
    ):
        self.random_wait = random_wait
        self.secs = secs
        super().__init__(*args, **kargs)
    #:

    def do_GET(self):
        secs = random.randint(3, 8) if self.random_wait else self.secs
        time.sleep(secs)
        super().do_GET()
    #:
#:

if __name__ == '__main__':  
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Threaded HTTP server in Python')
    parser.add_argument(
        '-p', '--port',
        required=False,
        metavar='PORT',
        default=8000,
        type=int
    )
    parser.add_argument(
        '-s', '--slow',
        action='store_true',
        default=False,
        help='For testing purposes, slow requests (currently, only GETs) for pre-defined amount of time',
    )
    parser.add_argument(
        '-r', '--randomly-slow',
        action='store_true',
        default=False,
        help='For testing purposes, slow requests (currently, only GETs) for a random amount of time',
    )
    args = parser.parse_args()
    handler_class = SimpleHTTPRequestHandler
    if args.slow:
        print("[+] Using a SLOW request handler")
        handler_class = SimpleSlowHTTPRequestHandler 
    elif args.randomly_slow:
        print("[+] Using a RANDOMLY SLOW request handler")
        handler_class = lambda *args, **kargs: \
            SimpleSlowHTTPRequestHandler(*args, random_wait=True, **kargs)
    
    try:
        server = ThreadedHTTPServer(('', args.port), handler_class=handler_class)
        print(f"Starting server at port {args.port}. Stop with CTRL+C")
        server.serve_forever()
    except KeyboardInterrupt:
        print("[+] Exiting via CTRL+C")
