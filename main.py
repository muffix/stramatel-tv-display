"""CLI entry point that wires the parser and HTTP server components together."""

from __future__ import annotations

import argparse
import logging
from http.server import ThreadingHTTPServer

from serial.tools import list_ports

from server import Handler, start_source_thread


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--com",
        help="COM port (e.g. COM3). If omitted, dummy data is served instead.",
    )
    parser.add_argument(
        "--fake-data",
        action="store_true",
        help="Ignore serial input and stream frames from bundled test data.",
    )
    parser.add_argument("--http", default="0.0.0.0", help="HTTP bind address")
    parser.add_argument("--port", type=int, default=8000, help="HTTP port")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

    if not args.com:
        logging.info("Available serial ports:")
        for port in list_ports.comports():
            logging.info("  %s - %s", port.device, port.description)

    start_source_thread(args.com, use_fake=args.fake_data)

    with ThreadingHTTPServer((args.http, args.port), Handler) as server:
        logging.info(
            "Open http://%s:%s/ in a browser (fullscreen on your output)",
            args.http,
            args.port,
        )
        server.serve_forever()


if __name__ == "__main__":
    main()
