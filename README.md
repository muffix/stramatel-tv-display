# Stramatel Hockey Scoreboard Renderer

Small Python app that reads Stramatel hockey/floorball serial data, parses the 54‑byte frames, and serves a minimal web UI showing clock, scores, period, penalties, and timeouts. It also exposes a vMix-friendly JSON endpoint so you can feed graphics directly into vMix (see the vMix section below). A bundled test stream lets you demo without hardware.

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

## vMix Data Source

The server exposes `http://<host>:8000/vmix.json`, returning a single-row JSON array with keys:

`Clock, Period, HomeScore, AwayScore, Running, Horn, HomeTimeout, AwayTimeout, HomePenalties, AwayPenalties, HomePensActive, AwayPensActive, LastUpdated`

Add in vMix:
1. Data Sources Manager → Add → JSON  
2. URL: `http://<host>:8000/vmix.json`  
3. Pick a suitable refresh rate, e.g. 100ms-500ms
4. In Title Editor, map fields to the column names above (or use column order).

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
