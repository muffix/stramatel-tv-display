# Stramatel Hockey Scoreboard Renderer

Small Python app that reads Stramatel hockey/floorball serial data, parses the 54‑byte frames, and serves a minimal web UI showing clock, scores, period, penalties, and timeouts. It can also replay bundled test data for demoing without hardware.

## Requirements

- Python ≥ 3.14 (project targets 3.14 per `pyproject.toml`)
- `uv` (recommended) or any virtualenv tool
- Serial support: `pyserial`
- Dev/testing: `pytest`

## Install

```bash
# All deps (runtime + dev/test) into .venv
uv sync --group dev

# Runtime-only (omit dev extras)
uv sync
```

Notes:
- `uv sync` creates `.venv` automatically and respects `uv.lock`.

## Running (with hardware)

```bash
uv run python main.py --com COM3
```

Replace `COM3` with your serial device (e.g., `/dev/ttyUSB0` on Linux, `/dev/cu.usbserial123` on macOS). Open http://localhost:8000/ in a browser and fullscreen it on your display output.

## Running (demo without hardware)

Use bundled fixture data:

```bash
uv run python main.py --fake-data
```

This replays `tests/data/stramatel_hockey_testdata_v3_raw_with_chatter.bin` on a loop.

## Testing

```bash
uv run pytest
```

## Project Structure

- `parser.py` — frame constants, parsing helpers, `FrameStream`
- `server.py` — HTTP handler, shared state, data source threads (serial or fake)
- `main.py` — CLI wiring
- `static/` — UI assets (HTML/CSS/JS)
- `tests/` — parser unit tests and fixture data
