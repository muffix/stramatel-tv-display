#!/usr/bin/env python3
"""Stramatel floorball scoreboard simulator (RS-485 frame emitter)."""

from __future__ import annotations

import argparse
import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Iterable, Optional

import serial
from pynput import keyboard

START = 0xF8
END = 0x0D
FRAME_LEN = 54
SPORT_HOCKEY = 0x35  # Hockey / Floorball

PERIOD_MS = 20 * 60 * 1000
HORN_MS = 1000
TICK_HZ_DEFAULT = 10


def _digits(s: str) -> list[int]:
    return [ord(c) for c in s]


def _active_mask(active_slots: Iterable[int]) -> int:
    key = tuple(sorted(active_slots))
    return {
        (1,): 0x31,
        (1, 2): 0x32,
        (1, 2, 3): 0x33,
        (2,): 0x34,
        (3,): 0x35,
        (2, 3): 0x36,
        (1, 3): 0x37,
    }.get(key, 0x20)


def _format_clock_ms(ms: int) -> list[int]:
    ms = max(0, ms)
    if ms < 60_000:
        seconds = ms // 1000
        tenths = (ms % 1000) // 100
        if seconds < 10:
            d1 = 0x20
            d2 = ord(str(seconds))
        else:
            s = f"{seconds:02d}"
            d1, d2 = ord(s[0]), ord(s[1])
        return [d1, d2, ord(str(tenths)), 0x20]

    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    if minutes < 10:
        m1 = 0x20
        m2 = ord(str(minutes))
    else:
        m = f"{minutes:02d}"
        m1, m2 = ord(m[0]), ord(m[1])
    s = f"{seconds:02d}"
    return [m1, m2, ord(s[0]), ord(s[1])]


def _format_penalty_ms(ms: Optional[int]) -> list[int]:
    if ms is None:
        return [0x20, 0x20, 0x20]
    ms = max(0, ms)
    seconds = ms // 1000
    minutes = min(9, seconds // 60)
    seconds = seconds % 60
    s = f"{minutes}{seconds:02d}"
    return _digits(s)


@dataclass
class TeamState:
    score: int = 0
    penalties: list[Optional[int]] = field(default_factory=lambda: [None, None, None])


@dataclass
class GameState:
    home: TeamState = field(default_factory=TeamState)
    away: TeamState = field(default_factory=TeamState)
    period: int = 1
    clock_ms: int = PERIOD_MS
    running: bool = False
    horn_until: float = 0.0
    log_next: bool = False
    log_reason: Optional[str] = None
    lock: threading.Lock = field(default_factory=threading.Lock)

    def toggle_running(self) -> None:
        with self.lock:
            self.running = not self.running

    def adjust_score(self, team: TeamState, delta: int) -> None:
        with self.lock:
            team.score = max(0, team.score + delta)

    def set_period(self, period: int) -> None:
        with self.lock:
            self.period = max(1, min(3, period))

    def reset_clock(self) -> None:
        with self.lock:
            self.clock_ms = PERIOD_MS
            self.running = False

    def add_penalty(self, team: TeamState, minutes: int) -> None:
        with self.lock:
            for idx in range(3):
                if team.penalties[idx] is None:
                    team.penalties[idx] = minutes * 60 * 1000
                    break

    def tick(self, delta_ms: int) -> None:
        with self.lock:
            if self.running and self.clock_ms > 0:
                self.clock_ms = max(0, self.clock_ms - delta_ms)
                if self.clock_ms == 0:
                    self.running = False
                    self.horn_until = time.monotonic() + (HORN_MS / 1000)

            if self.running:
                for team in (self.home, self.away):
                    for i, ms in enumerate(team.penalties):
                        if ms is None:
                            continue
                        ms = max(0, ms - delta_ms)
                        team.penalties[i] = ms if ms > 0 else None

    def horn_active(self) -> bool:
        with self.lock:
            horn_until = self.horn_until
        return time.monotonic() < horn_until

    def consume_log_request(self) -> Optional[str]:
        with self.lock:
            if not self.log_next:
                return None
            reason = self.log_reason or "key"
            self.log_next = False
            self.log_reason = None
            return reason

    def request_log_next(self, reason: str) -> None:
        with self.lock:
            self.log_next = True
            self.log_reason = reason


def build_frame(state: GameState) -> bytes:
    buf = [0x00] * FRAME_LEN
    buf[0] = START
    buf[1] = SPORT_HOCKEY

    with state.lock:
        clock_ms = state.clock_ms
        home_score = state.home.score
        away_score = state.away.score
        period = state.period
        running = state.running
        home_penalties = list(state.home.penalties)
        away_penalties = list(state.away.penalties)

    buf[4:8] = _format_clock_ms(clock_ms)

    hs = f"{min(99, home_score):02d}"
    as_ = f"{min(99, away_score):02d}"
    buf[9:11] = _digits(hs)
    buf[12:14] = _digits(as_)
    buf[14] = ord(str(period))

    home_active = [i + 1 for i, v in enumerate(home_penalties) if v is not None]
    away_active = [i + 1 for i, v in enumerate(away_penalties) if v is not None]
    buf[15] = _active_mask(home_active)
    buf[16] = _active_mask(away_active)

    buf[17] = ord("0")
    buf[18] = ord("0")

    buf[19] = 0x31 if state.horn_active() else 0x30
    buf[20] = 0x31 if running else 0x30

    for i, ms in enumerate(home_penalties):
        base = 22 + (i * 3)
        buf[base : base + 3] = _format_penalty_ms(ms)
    for i, ms in enumerate(away_penalties):
        base = 35 + (i * 3)
        buf[base : base + 3] = _format_penalty_ms(ms)

    buf[53] = END
    return bytes(buf)


def keyboard_listener(
    state: GameState, stop_event: threading.Event
) -> keyboard.Listener:
    def on_press(key: keyboard.Key | keyboard.KeyCode) -> bool | None:
        if key == keyboard.Key.space:
            state.toggle_running()
            state.request_log_next("key=Space")
            return None
        if key == keyboard.Key.esc:
            stop_event.set()
            return False

        if not isinstance(key, keyboard.KeyCode) or not key.char:
            return None

        k = key.char.lower()
        if k == "a":
            state.adjust_score(state.home, 1)
            state.request_log_next("key=a")
        elif k == "q":
            state.adjust_score(state.home, -1)
            state.request_log_next("key=q")
        elif k == "s":
            state.adjust_score(state.away, 1)
            state.request_log_next("key=s")
        elif k == "w":
            state.adjust_score(state.away, -1)
            state.request_log_next("key=w")
        elif k == "e":
            state.add_penalty(state.home, 2)
            state.request_log_next("key=e")
        elif k == "r":
            state.add_penalty(state.home, 5)
            state.request_log_next("key=r")
        elif k == "d":
            state.add_penalty(state.away, 2)
            state.request_log_next("key=d")
        elif k == "f":
            state.add_penalty(state.away, 5)
            state.request_log_next("key=f")
        elif k == "t":
            state.reset_clock()
            state.request_log_next("key=t")
        elif k in {"1", "2", "3"}:
            state.set_period(int(k))
            state.request_log_next(f"key={k}")

        return None

    return keyboard.Listener(on_press=on_press)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--com", required=True, help="Serial port (e.g. COM3)")
    parser.add_argument("--clock", default="20:00", help="Start clock MM:SS")
    parser.add_argument("--period", type=int, default=1)
    parser.add_argument("--home", type=int, default=0)
    parser.add_argument("--away", type=int, default=0)
    parser.add_argument("--running", action="store_true")
    parser.add_argument("--tick-hz", type=int, default=TICK_HZ_DEFAULT)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def parse_clock_arg(text: str) -> int:
    parts = text.strip().split(":")
    if len(parts) != 2:
        raise ValueError("Clock must be MM:SS")
    minutes = int(parts[0])
    seconds = int(parts[1])
    if minutes < 0 or seconds < 0 or seconds >= 60:
        raise ValueError("Invalid clock value")
    return (minutes * 60 + seconds) * 1000


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    state = GameState()
    state.clock_ms = parse_clock_arg(args.clock)
    state.period = max(1, min(3, args.period))
    state.home.score = max(0, args.home)
    state.away.score = max(0, args.away)
    state.running = bool(args.running)

    stop_event = threading.Event()
    listener = keyboard_listener(state, stop_event)
    listener.start()

    tick_hz = max(1, args.tick_hz)
    tick_sleep = 1.0 / tick_hz

    logging.info(
        "Controls: Space=start/stop, q/a home-/+, w/s away-/+, "
        "e/r home +2/+5, d/f away +2/+5, t reset clock, 1-3 set period, Esc quit"
    )

    with serial.Serial(
        args.com, 19200, bytesize=8, parity="N", stopbits=1, timeout=0.1
    ) as ser:
        last = time.monotonic()
        try:
            while not stop_event.is_set():
                now = time.monotonic()
                delta_ms = int((now - last) * 1000)
                last = now

                if delta_ms > 0:
                    state.tick(delta_ms)

                frame = build_frame(state)
                ser.write(frame)

                reason = state.consume_log_request()
                if reason:
                    logging.info("next frame (%s): %s", reason, frame.hex())

                if args.verbose:
                    with state.lock:
                        clock_ms = state.clock_ms
                        running = state.running
                    logging.info(
                        "clock_ms=%s running=%s frame=%s",
                        clock_ms,
                        running,
                        frame.hex(),
                    )

                time.sleep(tick_sleep)
        except KeyboardInterrupt:
            logging.info("Exiting")
        finally:
            stop_event.set()
            listener.stop()


if __name__ == "__main__":
    main()
