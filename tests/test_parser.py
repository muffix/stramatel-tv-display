from typing import List


from parser import (
    END,
    FRAME_LEN,
    SPORT_HOCKEY,
    START,
    FrameStream,
    parse_clock,
    parse_hockey,
    penalties_active,
    parse_penalty,
    parse_1digit,
    parse_2digits,
)


def _digits(s: str) -> List[int]:
    return [ord(c) for c in s]


def make_hockey_frame(
    clock: str = "0604",
    home_score: str = "03",
    away_score: str = "11",
    period: str = "2",
    running: bool = True,
    horn: bool = False,
    home_pen_mask: int = 0x34,
    away_pen_mask: int = 0x36,
    home_timeouts: str = "1",
    away_timeouts: str = "0",
    home_penalties: List[str | None] | None = None,
    away_penalties: List[str | None] | None = None,
) -> bytes:
    """Build a 54-byte hockey frame with predictable contents."""
    home_penalties = home_penalties or ["200", "030", None]
    away_penalties = away_penalties or ["145", None, None]

    buf = [0x00] * FRAME_LEN
    buf[0] = START
    buf[1] = SPORT_HOCKEY

    # Clock (bytes 4..7)
    clock_bytes = _digits(clock)
    buf[4 : 4 + len(clock_bytes)] = clock_bytes

    # Scores
    buf[9:11] = _digits(home_score)
    buf[12:14] = _digits(away_score)

    buf[14] = ord(period)
    buf[15] = home_pen_mask
    buf[16] = away_pen_mask
    buf[17] = ord(home_timeouts)
    buf[18] = ord(away_timeouts)
    buf[19] = 0x31 if horn else 0x30
    buf[20] = 0x31 if running else 0x30

    def put_penalty(base: int, value: str | None):
        if value is None:
            buf[base : base + 3] = [0x20, 0x20, 0x20]
        else:
            buf[base : base + 3] = _digits(value)

    put_penalty(22, home_penalties[0])
    put_penalty(25, home_penalties[1])
    put_penalty(28, home_penalties[2])
    put_penalty(35, away_penalties[0])
    put_penalty(38, away_penalties[1])
    put_penalty(41, away_penalties[2])

    buf[53] = END
    return bytes(buf)


def test_parse_digit():
    assert parse_1digit(ord("1")) == 1
    assert parse_1digit(ord("a")) is None


def test_parse_2digits():
    assert parse_2digits(ord("4"), ord("2")) == 42
    assert parse_2digits(ord("0"), ord("2")) == 2
    assert parse_2digits(ord(" "), ord("2")) == 2


def test_parse_clock_modes():
    assert parse_clock(*_digits("420 ")) == "42.0"  # sub-minute with tenths
    assert parse_clock(*_digits(" 604")) == "6:04"
    assert parse_clock(*_digits("0604")) == "06:04"


def test_parse_penalties():
    assert parse_penalty(*_digits("123")) == "1:23"
    assert parse_penalty(*_digits("023")) == "0:23"


def test_penalties_active_map():
    assert penalties_active(0x31) == [1]
    assert penalties_active(0x36) == [2, 3]
    assert penalties_active(0x20) == []


def test_parse_hockey_core_fields():
    frame = make_hockey_frame()
    parsed = parse_hockey(frame)

    assert parsed["ok"] is True
    assert parsed["type"] == "hockey"
    assert parsed["clock"] == "06:04"
    assert parsed["home"]["score"] == 3
    assert parsed["away"]["score"] == 11
    assert parsed["period"] == 2
    assert parsed["running"] is True
    assert parsed["horn"] is False
    assert parsed["home"]["timeouts"] == 1
    assert parsed["away"]["timeouts"] == 0
    assert parsed["home"]["penalties_active"] == [2]
    assert parsed["away"]["penalties_active"] == [2, 3]
    assert parsed["home"]["penalty_clocks"] == ["2:00", "0:30", None]
    assert parsed["away"]["penalty_clocks"] == ["1:45", None, None]


def test_frame_stream_resync_with_chatter():
    fs = FrameStream()
    good = make_hockey_frame()
    noise = b"\x00\x01\x02garbage"

    # Feed noise then partial frame to ensure it waits
    fs.feed(noise + good[:10])
    assert fs.next_frame() is None

    # Feed the rest and an extra good frame; it should emit in order
    fs.feed(good[10:] + good)
    out1 = fs.next_frame()
    out2 = fs.next_frame()
    assert out1 == good
    assert out2 == good
    assert fs.next_frame() is None


def test_parse_hockey_subminute_clock():
    frame = make_hockey_frame(clock="420 ")
    parsed = parse_hockey(frame)
    assert parsed["clock"] == "42.0"
