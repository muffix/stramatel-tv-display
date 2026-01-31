# Floorball Scoreboard Simulator (Stramatel RS-485) — Specs & Plan

## Overview
Create a standalone Python script that simulates a Stramatel floorball scoreboard by emitting valid 54-byte frames over RS-485. The emitted frames must match the exact format expected by the existing parser (`parser.py`), so the current UI/server can consume it without changes.

Target script location: `scripts/floorball_sim.py`.

## Requirements
- **Transport**: RS-485 via serial port, 19200 8N1.
- **Frame cadence**: 10 Hz (every 100 ms).
- **Platform**: macOS, Windows, Linux.
- **Keyboard input**: use `pynput` for cross-platform control.
- **Floorball rules**: 3 periods, 20:00 each. No timeouts or other specials.
- **Penalties**: per team up to 3 slots, duration 2:00 or 5:00. First free slot used.
- **Clock**: must support tenths under 1:00 and exactly match current parser expectations.

## Frame Format (must match `parser.py` / `parse_hockey`)
- Length: **54 bytes**
- `frame[0] = 0xF8` (START)
- `frame[1] = 0x35` (SPORT_HOCKEY; used for hockey/floorball)
- `frame[53] = 0x0D` (END)

### Clock (bytes 4..7)
- **Normal** (>= 1:00): ASCII `MMSS` with optional leading space for tens of minutes.
- **Sub-minute** (< 1:00): ASCII `SSt ` where the final byte is a space (`0x20`), and tenths are encoded in byte 6.
- Must match `parse_clock`:
  - Example: `"0604" -> "06:04"`
  - Example: `" 604" -> "6:04"`
  - Example: `"420 " -> "42.0"`

### Scores
- Home: `frame[9]`, `frame[10]` (two ASCII digits)
- Away: `frame[12]`, `frame[13]`

### Period
- `frame[14]` = ASCII `1`, `2`, or `3`

### Penalties Active Masks
- Home: `frame[15]`
- Away: `frame[16]`
- Must match `penalties_active()` mapping:
  - `0x31` = [1]
  - `0x32` = [1,2]
  - `0x33` = [1,2,3]
  - `0x34` = [2]
  - `0x35` = [3]
  - `0x36` = [2,3]
  - `0x37` = [1,3]
  - default = `0x20` (no active penalties)

### Timeouts
- Home: `frame[17]`
- Away: `frame[18]`
- Not used; always `"0"` (ASCII)

### Horn / Running Flags
- `frame[19]`: horn (`0x31` true, `0x30` false)
- `frame[20]`: running (`0x31` true, `0x30` false)

### Penalty Clocks
- Home: `frame[22..30]` (3 slots × 3 bytes)
- Away: `frame[35..43]`
- Each slot is ASCII `MSS` (e.g., `200`, `030`, `500`) or spaces when empty.

## Game Model
- **Clock**: 20:00 countdown per period.
- **Periods**: 1..3 (manual set via keys).
- **Clock ticks**: advance every loop by elapsed ms, only when running.
- **Horn**: auto-trigger for ~1s at period end (optional, simple boolean based on monotonic time).

## Penalty Behavior
- Each team has 3 slots, stored as remaining milliseconds or `None`.
- New penalties fill the first free slot.
- 2:00 or 5:00 duration, count down only when clock is running.
- Slot clears automatically at 0:00; active mask recomputed from non-empty slots.

## CLI
Suggested args:
- `--com <port>` (required)
- `--clock MM:SS` (default 20:00)
- `--period 1-3` (default 1)
- `--home <score>` (default 0)
- `--away <score>` (default 0)
- `--running` (start immediately)
- `--tick-hz <int>` (default 10)
- `--verbose` (log frames)

## Keyboard Controls (proposed)
- `Space`: start/stop clock
- Home score: `q` (−1), `a` (+1)
- Away score: `w` (−1), `s` (+1)
- Add penalties:
  - Home +2:00 → `e`
  - Home +5:00 → `r`
  - Away +2:00 → `d`
  - Away +5:00 → `f`
- Period: `1`, `2`, `3`
- Reset clock to 20:00: `t`
- Quit: `Esc` or `Ctrl+C`

## Implementation Plan
1. **Data model**
   - `GameState` with `home`, `away`, `period`, `clock_ms`, `running`, `horn_until`.
   - `TeamState` with `score`, `penalties` (3 slots).
   - Shared `threading.Lock` for safe reads/writes.

2. **Clock/penalty ticking**
   - Tick loop based on monotonic time delta.
   - If running, decrement `clock_ms` and penalties.
   - On clock reaching 0, stop and trigger horn.

3. **Frame builder**
   - Encode clock to parser-compatible bytes (sub-minute format with trailing space).
   - Encode scores, period, active masks, penalties.
   - Write 54-byte frame to serial port.

4. **Keyboard input**
   - Use `pynput` listener in a background thread.
   - Map keys to state mutations as defined above.

5. **Main loop**
   - Initialize state from CLI.
   - Start keyboard listener.
   - Open serial port and emit frames at 10 Hz.
   - Optional verbose logging.

## Notes
- Keep code ASCII-only.
- Avoid altering existing app code; simulator is standalone.
- If needed later, add a `--dry-run` mode that prints frames instead of writing to serial.
