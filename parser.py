"""Parsing utilities for Stramatel hockey / floorball frames."""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

# Stramatel frame constants
START = 0xF8
END = 0x0D
FRAME_LEN = 54
SPORT_HOCKEY = 0x35  # Hockey / Floorball frame code


def penalties_active(code: int) -> List[int]:
    """Return penalty slots currently active for the given code byte."""
    return {
        0x31: [1],
        0x32: [1, 2],
        0x33: [1, 2, 3],
        0x34: [2],
        0x35: [3],
        0x36: [2, 3],
        0x37: [1, 3],
    }.get(code, [])


def digit(b: int) -> Optional[str]:
    """Convert a byte to a single digit string if valid."""
    return chr(b) if 0x30 <= b <= 0x39 else None


def parse_1digit(a: int) -> Optional[int]:
    a = digit(a)
    return int(a) if a is not None else None


def parse_2digits(a: int, b: int) -> Optional[int]:
    a, b = digit(a), digit(b)
    if a is None and b is None:
        return None
    if a is None:
        return int(b)
    return int(a + b)


def parse_clock(d1: int, d2: int, d3: int, d4: int) -> Optional[str]:
    """Parse 4-byte clock field into a human-readable string."""
    if d4 == 0x20:  # < 1 minute encoding: "SSt "
        a, b, t = map(parse_1digit, (d1, d2, d3))
        if None in (b, t):
            return None
        if a is None:
            a = ""
        return f"{a}{b}.{t}"  # e.g. "42.0"

    a, b, c, d = map(parse_1digit, (d1, d2, d3, d4))
    if None in (b, c, d):
        return None
    if a is None:
        a = ""
    return f"{a}{b}:{c}{d}"  # e.g. "06:04"


def parse_penalty(a: int, b: int, c: int) -> Optional[str]:
    a, b, c = map(digit, (a, b, c))
    if None in (a, b, c):
        return None
    return f"{a}:{b}{c}"


class FrameStream:
    """Streaming byte buffer that yields well-framed Stramatel packets."""

    def __init__(self) -> None:
        self.buf: bytearray = bytearray()

    def feed(self, data: bytes) -> None:
        self.buf.extend(data)

    def next_frame(self) -> Optional[bytes]:
        while True:
            if len(self.buf) < 1:
                return None
            if self.buf[0] != START:
                start_index = self.buf.find(bytes([START]))
                if start_index == -1:
                    self.buf.clear()
                    return None
                del self.buf[:start_index]
            if len(self.buf) < FRAME_LEN:
                return None
            candidate = bytes(self.buf[:FRAME_LEN])
            if candidate[-1] != END:
                del self.buf[:1]
                continue
            del self.buf[:FRAME_LEN]
            return candidate


def parse_hockey(frame: bytes) -> Dict[str, Any]:
    """Parse a single 54-byte hockey frame into a state dictionary."""
    clock = parse_clock(frame[4], frame[5], frame[6], frame[7])  # bytes 5..8
    home_score = parse_2digits(frame[9], frame[10])  # 10..11
    away_score = parse_2digits(frame[12], frame[13])  # 13..14
    period = parse_1digit(frame[14])  # 15

    home_pen_active = penalties_active(frame[15])  # 16
    away_pen_active = penalties_active(frame[16])  # 17
    home_to = parse_1digit(frame[17])  # 18
    away_to = parse_1digit(frame[18])  # 19

    horn = frame[19] == 0x31  # 20
    running = frame[20] == 0x31  # 21

    # Home penalties: 23..31 (3 digits each)
    hp1 = parse_penalty(frame[22], frame[23], frame[24])
    hp2 = parse_penalty(frame[25], frame[26], frame[27])
    hp3 = parse_penalty(frame[28], frame[29], frame[30])
    # Away penalties: 36..44
    ap1 = parse_penalty(frame[35], frame[36], frame[37])
    ap2 = parse_penalty(frame[38], frame[39], frame[40])
    ap3 = parse_penalty(frame[41], frame[42], frame[43])

    return {
        "ok": True,
        "ts": time.time(),
        "type": "hockey",
        "clock": clock,
        "period": period,
        "horn": horn,
        "running": running,
        "home": {
            "score": home_score,
            "timeouts": home_to,
            "penalties_active": home_pen_active,
            "penalty_clocks": [hp1, hp2, hp3],
        },
        "away": {
            "score": away_score,
            "timeouts": away_to,
            "penalties_active": away_pen_active,
            "penalty_clocks": [ap1, ap2, ap3],
        },
    }
