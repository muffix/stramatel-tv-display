# AGENTS.md

This project is a minimal Python app that reads Stramatel RS-485 hockey/floorball frames, parses 54-byte packets, and serves a web UI plus a vMix-friendly JSON endpoint.

## High-level flow
- `main.py`: CLI entry point; parses args, starts data source thread, runs `ThreadingHTTPServer`.
- `server.py`: HTTP handler, state storage, serial/fake data threads, `/state` + `/state/stream` (SSE) + `/vmix.json` + static assets.
- `parser.py`: frame resync (`FrameStream`), digit/clock/penalty parsing, hockey frame decoding.

## Endpoints
- `/` -> redirect to `/static/index.html`
- `/state` -> live JSON state (polling)
- `/state/stream` -> server-sent events stream of the same state
- `/vmix.json` -> array-of-objects for vMix ingestion
- `/static/*` -> UI assets

## UI
- `static/index.html`, `static/app.js`, `static/style.css` implement a dark, high-contrast scoreboard view.
- Client uses SSE (`EventSource` on `/state/stream`) to render clock, scores, period, penalties, and timeouts.

## Data sources
- Real serial input via `pyserial` at 19200 8N1.
- Fake data loop from `tests/data/stramatel_hockey_testdata_v3_raw_with_chatter.bin`.

## Tests
- `tests/test_parser.py` validates digit/clock/penalty parsing and frame resync behavior.

## Docs
- `docs/stramatel_frames_all_sports.md` is a structured transcription of the Stramatel protocol tables.
- `docs/STRAMATEL codes.pdf` contains the original protocol tables and wiring details.

## Dependencies
- Python >= 3.14 (per `pyproject.toml`)
- Runtime: `pyserial`
- Dev/test: `pytest`

## Notes
- The parser currently focuses on hockey/floorball (`SPORT_HOCKEY` code).
- State is protected by a global lock; `latest_state` starts as `{\"ok\": false}` until frames arrive.
