"""HTTP server and data-source wiring for the Stramatel scoreboard renderer."""

from __future__ import annotations

import json
import logging
import mimetypes
import pathlib
import threading
import time
from http.server import BaseHTTPRequestHandler
from typing import Iterator, Optional, TypedDict

import serial

from parser import (
    SPORT_HOCKEY,
    FrameStream,
    parse_hockey,
)

STATIC_DIR = pathlib.Path(__file__).with_name("static")
DATA_DIR = pathlib.Path(__file__).parent / "tests" / "data"


class TeamState(TypedDict, total=False):
    score: Optional[int]
    timeouts: Optional[int]
    penalties_active: list[int]
    penalty_clocks: list[Optional[str]]


class ScoreboardState(TypedDict, total=False):
    ok: bool
    reason: str
    ts: float
    type: str
    clock: Optional[str]
    period: Optional[int]
    horn: bool
    running: bool
    home: TeamState
    away: TeamState


state_lock = threading.Lock()
latest_state: ScoreboardState = {"ok": False, "reason": "no data yet"}


class Handler(BaseHTTPRequestHandler):
    """Minimal HTTP handler serving current state and static assets."""

    server_version = "StramatelHTTP/1.0"

    def do_GET(self) -> None:  # noqa: N802  (BaseHTTPRequestHandler API)
        if self.path == "/" or self.path.startswith("/index"):
            self._redirect("/static/index.html")
            return

        if self.path == "/state":
            self._send_json()
            return

        if self.path.startswith("/static/"):
            self._send_static()
            return

        self.send_error(404)

    def log_message(self, fmt: str, *args: object) -> None:
        logging.info("%s - %s", self.address_string(), fmt % args)

    def _redirect(self, location: str) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def _send_json(self) -> None:
        with state_lock:
            payload = json.dumps(latest_state).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def _send_static(self) -> None:
        rel = self.path[len("/static/") :]
        if ".." in rel or rel.startswith("/"):
            self.send_error(400)
            return

        path = STATIC_DIR / rel
        if not path.is_file():
            self.send_error(404)
            return

        ctype, _ = mimetypes.guess_type(str(path))
        ctype = ctype or "application/octet-stream"
        data = path.read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


def reader_thread(com_port: str) -> None:
    """Continuously read frames from a serial port and update latest_state."""
    global latest_state
    with serial.Serial(
        com_port, 19200, bytesize=8, parity="N", stopbits=1, timeout=0.1
    ) as ser:
        with state_lock:
            latest_state = {
                "ok": False,
                "reason": f"connected to {com_port}, waiting for frames",
            }
        _consume_stream(_serial_chunks(ser))


def dummy_data_thread() -> None:
    """Feed frames from the bundled fixture file to simulate the scoreboard."""
    data_file = DATA_DIR / "stramatel_hockey_testdata_v3_raw_with_chatter.bin"
    _consume_stream(_file_chunks(data_file), frame_delay=0.5)


def start_source_thread(
    com_port: Optional[str], use_fake: bool = False
) -> threading.Thread:
    """Start either a serial reader or dummy data feeder."""
    if use_fake or not com_port:
        if com_port and use_fake:
            logging.info("Ignoring --com because --fake-data was requested")
        logging.info("Using bundled dummy data")
        target, args = dummy_data_thread, ()
    else:
        logging.info("Starting serial reader on %s", com_port)
        target, args = reader_thread, (com_port,)

    thread = threading.Thread(target=target, args=args, daemon=True)
    thread.start()
    return thread


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _consume_stream(chunks: Iterator[bytes], frame_delay: float = 0.0) -> None:
    """Common frame-consumption loop used by both real and fake sources."""
    global latest_state
    fs = FrameStream()

    for chunk in chunks:
        if not chunk:
            continue
        fs.feed(chunk)
        while True:
            frame = fs.next_frame()
            if frame is None:
                break
            if frame[1] == SPORT_HOCKEY:
                parsed = parse_hockey(frame)
                with state_lock:
                    latest_state = parsed
                if frame_delay:
                    time.sleep(frame_delay)


def _serial_chunks(ser: serial.Serial) -> Iterator[bytes]:
    """Yield data read from the serial port."""
    while True:
        data = ser.read(4096)
        if data:
            yield data


def _file_chunks(path: pathlib.Path) -> Iterator[bytes]:
    """Yield data blocks from a file, looping forever."""
    with path.open("rb") as fixture:
        while True:
            data = fixture.read(4096)
            if not data:
                fixture.seek(0)
                continue
            yield data
