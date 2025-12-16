# Stramatel RS-485 “TV Interface” Serial Protocol (UFBE09046)

This is a **coding-agent-friendly** description of the Stramatel *“Interface TV RS485”* protocol described in `STRAMATEL codes.pdf`.

It covers:
- Link layer / framing and robust resync (RS-485 “chatter” exists)
- Byte encoding rules (digits, flags, UTF-16 text)
- **All documented frame layouts** (not only hockey/floorball)
- A practical parsing strategy and suggested JSON output shapes

---

## 1) Physical layer and wiring (TV RS485 interface module)

The TV RS-485 interface module exposes a 4-wire cable (colors from the PDF):

- **Blue**: GND (Masse)
- **White**: Tx+  
- **Yellow**: Tx−  
- **Red**: not connected

You can connect this to a standard RS-485 USB dongle (A/B/GND). If your dongle labels are **A/B**, note that vendors sometimes swap A/B naming; if you see garbage, swap A/B.

---

## 2) Serial settings

- **19200 baud**
- **8 data bits**
- **no parity**
- **1 stop bit** (19200 8N1)

---

## 3) Framing and resync

### 3.1 Fixed-length frames
All “TV interface” frames are exactly **54 bytes**:

- `frame[0] == 0xF8` (START)
- `frame[53] == 0x0D` (END)

### 3.2 RS-485 chatter / interleaving
The PDF warns that additional RS-485 traffic can be present (data exchange between control desks). Do not attempt to decode that traffic as “TV frames”.

**Recommended resync algorithm:**

1. Read bytes continuously into a ring buffer.
2. Scan for `0xF8`. If found:
   - if you have at least 54 bytes from that position, check `buf[i+53] == 0x0D`
   - if yes: emit `buf[i:i+54]` as a frame and advance to `i+54`
   - else: advance by 1 byte and keep scanning

This reliably discards chatter and re-synchronizes quickly.

---

## 4) Byte encoding rules (common across frames)

### 4.1 Digits and blanks
Most numeric “digits” are transmitted as:
- ASCII digits `0x30..0x39` (`'0'..'9'`)
- or `0x20` (space) meaning “blank / not displayed / unknown”

When parsing digits, treat space as **None** (or as 0 if you want a forgiving decoder).

### 4.2 Flags
Unless otherwise stated, flags use:
- `0x31` → ON / true
- any other value → OFF / false

Special cases:
- **Possession ball**: `0x31` = Home/Locaux, `0x32` = Away/Visiteurs, other = none/off.
- **Handball “penalties in progress”** (note 8): `0x31..0x37` is a bitmask-like encoding (see §9.2).

### 4.3 UTF-16 text
Frames that carry text (team names, player names, scrolling messages) use UTF-16 “Octet 1 / Octet 2” pairs.
In practice, treat each pair as **big-endian UTF-16** (`utf-16-be`) and strip trailing spaces.

---

## 5) Common field helpers

### 5.1 Parse a “4-digit clock” field (bytes `[4:8]`)

Many frames carry a 4-byte clock at offsets `4..7` (positions 5..8 in the PDF).

There are two common display modes:

#### Mode A: MMSS (normal)
If all 4 bytes are digits: interpret as **MM:SS**.

Example:
- bytes `b"1945"` → `"19:45"`

#### Mode B: sub-minute seconds + tenths (when the scoreboard shows tenths)

Some scoreboards switch display under 1 minute and transmit **seconds and tenths** using **3 digits**,
followed by a trailing space:

- `d1` = tens of seconds (`S_tens`)
- `d2` = ones of seconds (`S_ones`)
- `d3` = tenths (`t`)
- `d4` = **space** (`0x20`)

Example:
- bytes `b"420 "` → `"42.0"`

**Detection rule (per device behavior):**
- If and only if the **last clock byte** (`d4`) is a space (`0x20`), treat the clock as `SS.t`.
- Otherwise, interpret the 4 digits as `MMSS` → `MM:SS`.

Because this is definitive, you should not attempt heuristic detection beyond checking `d4 == 0x20`.
### 5.2 Parse a 3-digit penalty clock (MSS)
Penalty clocks are usually 3 digits (minute + seconds):
- `MSS` → `M:SS`
- Example: bytes `b"200"` → `"2:00"`

---

## 6) Sport codes and frame catalogue

The **sport code** is `frame[1]` (position 2 in the PDF). Values below are **hex bytes** as written in the PDF tables.

| Sport code (hex) | Meaning / frame family |
|---:|---|
| `0x33` | Basket-ball main frame (team score + team fouls + player fouls) **and** Netball main frame (3-digit score) |
| `0x37` | “Points individuels” (Away) for basket/hand/hockey/football |
| `0x38` | “Points individuels” (Home) for basket/hand/hockey/football |
| `0x35` | Handball / Football / Hockey / Floorball main frame **and** Boxe main frame (different mapping for some bytes) |
| `0x36` | Volley-ball main frame |
| `0x39` | Tennis main frame |
| `0x3A` | Tennis de table main frame |
| `0x6C` | Badminton main frame |
| `0x9A` | Simple stopwatch frame |
| `0x99` | Time setting (“mise à l’heure”) |
| `0x9C` | Training mode (“entrainement”) |
| `0x66` | LED test frame |
| `0x4D` | Scrolling messages content (“MESSAGES”, `M`) |
| `0x43` | Scrolling messages configuration (“CONFIGURATION MESSAGES”, `C`) |
| `0x77` | Team names / Local players names |
| `0x62` | Team names / Away players names |

> Note: `0x35` is reused across several sports; choose the correct mapping based on the selected sport on the control desk.

---

## 7) Frame layouts (all documented frames)

Offsets below are **0-based** (`frame[0]` is START).

### 7.1 Basket-ball main frame (SPORT=0x33) — “Basket avec fautes individuelles”

Key fields:
- `frame[3]`: possession (note 4)
- `frame[4:8]`: clock (MMSS or sub-minute)
- `frame[8:11]`: home score (3 digits)
- `frame[11:14]`: away score (3 digits)
- `frame[14]`: period
- `frame[15]`: home team fouls
- `frame[16]`: away team fouls
- `frame[17]`: home timeouts count
- `frame[18]`: away timeouts count
- `frame[19]`: horn (note 5)
- `frame[20]`: running (start/stop) (note 6)

Timeout chrono is split:
- `frame[21]`: timeout-chrono digit1
- `frame[46]`: timeout-chrono digit2
- `frame[47]`: timeout-chrono digit3

Player fouls (1 digit each):
- `frame[22..33]` → home players 1..12 (12 bytes)
- `frame[34..45]` → away players 1..12 (12 bytes)

Shot clock (24"):
- `frame[48]`: shotclock digit1
- `frame[49]`: shotclock digit2
- `frame[50]`: horn 24" (note 5)
- `frame[51]`: start/stop 24" (note 6)
- `frame[52]`: display 24" (note 7)

Suggested JSON:
```json
{
  "sport": "basket",
  "clock": "19:45",
  "running": true,
  "horn": false,
  "possession": "home",
  "score": {"home": 102, "away": 98},
  "period": 4,
  "teamFouls": {"home": 3, "away": 5},
  "timeouts": {"home": 2, "away": 1},
  "timeoutClock": "0:30",
  "playerFouls": {"home":[...12], "away":[...12]},
  "shotClock": {"value": 24, "running": true, "horn": false, "display": true}
}
```

---

### 7.2 Points individuels frames (SPORT=0x38 home, SPORT=0x37 away)

These frames carry **individual points** per player (and still include 24" fields).

Common header fields:
- `frame[3]`: possession (only present/meaningful for SPORT=0x37 in the PDF; accept it but allow blank)
- `frame[4:8]`: clock
- `frame[19]`: horn
- `frame[20]`: running

Player points encoding:
- Each player uses **2 digits** (00–99).
- Players 1..13 are packed consecutively starting at `frame[22]`.
- Player 14 is placed earlier: `frame[11]` (digit1) and `frame[12]` (digit2) in the PDF table.

Timeout chrono and shotclock fields exist as in basketball:
- `frame[46]`, `frame[47]`: timeout chrono digits2..3
- `frame[48..52]`: 24" block

Because these frames can be **interleaved** with main frames (the PDF says they alternate in some sports), your decoder should merge them into a single “state”.

---

### 7.3 Handball / Football main frame (SPORT=0x35)

Key fields:
- `frame[4:8]`: clock
- `frame[9:11]`: home score (2 digits, positions 10–11)
- `frame[12]`: blank (`0x20`)
- `frame[13:15]`: away score (2 digits, positions 13–14)
- `frame[14]`: away score digit2 (yes, overlaps with above; keep the 2-digit interpretation)
- `frame[14]` is away digit2; `frame[13]` is away digit1
- `frame[14]` is also used in other sports; don’t reuse here.

More directly (recommended):
- home score digits: `frame[9]`, `frame[10]`
- away score digits: `frame[12]` is blank, `frame[13]`, `frame[14]` → use `frame[13]`, `frame[14]`

Other fields:
- `frame[14]`: away score digit2
- `frame[14]` also appears in other tables; ignore.

- `frame[14]` confusion aside, in practice you can parse:
  - `home = int(d10+d11)`
  - `away = int(d13+d14)`

- `frame[14]`: away digit2
- `frame[14]`: (same byte)

- `frame[14]`: yes.

Period:
- `frame[14]` is not period.
- `frame[14]` is digit2.

Period is `frame[14]`? No: period is position 15 → `frame[14]` indeed.
So: **period = frame[14]** (digit/space).

So for handball/football, score uses:
- home: `frame[9]` (pos10), `frame[10]` (pos11)
- away: `frame[12]` (pos13), `frame[13]` (pos14)
and `frame[14]` (pos15) is period.

Then:
- `frame[15]`: home “penalties in progress” (note 8)
- `frame[16]`: away “penalties in progress” (note 8)
- `frame[17]`: home timeouts count
- `frame[18]`: away timeouts count
- `frame[19]`: horn (note 5)
- `frame[20]`: running (note 6)
- `frame[21]`: (unused `0x20` in this table)

Penalty clocks (3 penalties per team, each 3 digits), same packing as hockey:
- Home penalty1: `frame[22:25]`
- Home penalty2: `frame[25:28]`
- Home penalty3: `frame[28:31]`
- Away penalty1: `frame[35:38]`
- Away penalty2: `frame[38:41]`
- Away penalty3: `frame[41:44]`

(Intermediate bytes `frame[31..34]` are usually spaces.)

Suggested JSON:
```json
{
  "sport": "handball",
  "clock": "12:34",
  "running": true,
  "score": {"home": 18, "away": 16},
  "period": 1,
  "timeouts": {"home": 1, "away": 0},
  "penaltiesInProgress": {"home": "first+second", "away": "none"},
  "penalties": {
    "home": ["2:00","0:00","0:00"],
    "away": ["0:00","0:00","0:00"]
  }
}
```

---

### 7.4 Hockey / Floorball main frame (SPORT=0x35)

This uses the **same penalty packing** as §7.3 and (for most fields) matches the hockey/floorball table.

Key fields:
- `frame[4:8]`: clock (MMSS or sub-minute)
- score:
  - home: `frame[9]`, `frame[10]` (2 digits)
  - away: `frame[12]`, `frame[13]` (2 digits)
- `frame[14]`: period
- `frame[15]`: home penalties in progress (note 8)
- `frame[16]`: away penalties in progress (note 8)
- `frame[17]`: home timeouts count
- `frame[18]`: away timeouts count
- `frame[19]`: horn
- `frame[20]`: running

Penalty clocks:
- Home: `frame[22:31]` (3×3 digits)
- Away: `frame[35:44]` (3×3 digits)

---

### 7.5 Boxe main frame (SPORT=0x35) — different bytes for warnings

Boxe shares the same start/end and clock, but:
- `frame[10]` (pos11) holds **home warnings** (“avertissements”) instead of score digit2.
- `frame[13]` (pos14) holds **away warnings**.

Other bytes in the boxe column are often `0x20` (space). Implement boxe as a separate decoder that at minimum extracts:
- clock
- period (`frame[14]`)
- warnings (`frame[10]`, `frame[13]` if digits)

---

### 7.6 Netball main frame (SPORT=0x33)

Netball uses sport code `0x33` but the table differs from basket.

Key fields:
- `frame[3]`: possession (note 4)
- `frame[4:8]`: clock
- score is documented as “digit 2” and “digit 3” in the PDF table:
  - home: `frame[9]` (pos10), `frame[10]` (pos11)
  - away: `frame[12]` (pos13), `frame[13]` (pos14)
Treat as **2-digit score** (or 3-digit with implicit leading 0).

Other fields:
- `frame[14]`: period
- horn/running at `frame[19]` / `frame[20]`

---

### 7.7 Volley-ball main frame (SPORT=0x36)

Key fields:
- `frame[4:8]`: clock
- score (points in current rally/game): home `frame[9:11]` (2 digits), away `frame[12:14]` (2 digits)
- `frame[14]`: set number (current set)
- `frame[15]`: home sets won
- `frame[16]`: away sets won
- `frame[17]`: home timeouts count
- `frame[18]`: away timeouts count
- `frame[19]`: horn
- `frame[20]`: running
- `frame[21]`: display clock/chrono (note 9)

Per-set points (up to 4 sets), each is 2 digits:
- Set1: home `frame[24:26]`, away `frame[26:28]`
- Set2: home `frame[28:30]`, away `frame[30:32]`
- Set3: home `frame[32:34]`, away `frame[34:36]`
- Set4: home `frame[36:38]`, away `frame[38:40]`

Service and winner flags:
- `frame[50]`: service (note 10)
- `frame[51]`: winner (note 11)

(Other bytes are typically spaces.)

---

### 7.8 Tennis main frame (SPORT=0x39)

Key fields:
- `frame[4:8]`: clock
- score (points): home `frame[9:11]` (2 digits), away `frame[12:14]` (2 digits)
- `frame[14]`: set number
- `frame[15]`: home sets won
- `frame[16]`: away sets won
- `frame[20]`: running
- `frame[21]`: display clock/chrono (note 9)

Games:
- Current set games won (2 digits each):
  - home `frame[22]`, `frame[23]`
  - away `frame[35]`, `frame[36]`
- Games per set (1..4), 2 digits each, packed similarly to volley (see PDF table):
  - Set1: `frame[24:28]` (H two digits, A two digits)
  - Set2: `frame[28:32]`
  - Set3: `frame[37:41]`
  - Set4: `frame[41:45]`

Service / winner / tie-break:
- `frame[50]`: service (note 10)
- `frame[51]`: winner (note 11)
- `frame[52]`: tie-break in progress (note 12)

---

### 7.9 Tennis de table main frame (SPORT=0x3A)

Key fields:
- `frame[4:8]`: clock
- score (points): home `frame[9:11]` (2 digits), away `frame[12:14]` (2 digits)
- `frame[14]`: set number
- `frame[15]`: home sets won
- `frame[16]`: away sets won
- `frame[20]`: running
- `frame[21]`: display clock/chrono (note 9)

Per-set points (up to 4 sets), 2 digits each:
- Set1: home `frame[24:26]`, away `frame[26:28]`
- Set2: home `frame[28:30]`, away `frame[30:32]`
- Set3: home `frame[32:34]`, away `frame[34:36]`
- Set4: home `frame[36:38]`, away `frame[38:40]`

Service / winner:
- `frame[50]`: service (note 10)
- `frame[51]`: winner (note 11)

---

### 7.10 Badminton main frame (SPORT=0x6C)

Badminton is similar to tennis de table:
- clock at `frame[4:8]`
- score at `frame[9:11]` and `frame[12:14]`
- set at `frame[14]`
- sets won at `frame[15]` and `frame[16]`
- per-set points packed as in §7.9
- service `frame[50]`, winner `frame[51]`, tie-break `frame[52]` (note 12)

---

### 7.11 Simple stopwatch frame (SPORT=0x9A)

This frame mainly contains:
- clock digits at `frame[4:8]`
- horn at `frame[19]`
- running at `frame[20]`
- display clock/chrono at `frame[21]`

All other bytes are usually spaces.

---

### 7.12 Time setting frame (SPORT=0x99) — “Mise à l’heure”
This frame carries:
- `frame[4:8]`: current hour/minute digits (“Heure” digit1..4)
- display-on schedule digits at `frame[9:13]`
- display-off schedule digits at `frame[14:18]`
Most other bytes are spaces.

---

### 7.13 Training frame (SPORT=0x9C) — “Entrainement”
Carries:
- `frame[4:8]`: training chrono digits
- `frame[9:11]`: cycles digits
- `frame[19]`: horn
- `frame[20]`: running
- `frame[21]`: display clock/chrono (note 9)
- `frame[50]`: “Exercice/Repos” (note 13)

---

### 7.14 LED test frame (SPORT=0x66)
Carries:
- `frame[3]`: mode test (note 14)
- `frame[5]`: home test line
- `frame[6]`: away test line
- `frame[19]`: horn

---

### 7.15 Scrolling messages content frame (SPORT=0x4D, “M”)

Fields:
- `frame[2]`: frame index
- `frame[3]`: message number
- `frame[4:8]`: clock digits
- `frame[8..]`: UTF-16 characters (pairs) for message text
- horn at `frame[19]`, running at `frame[20]`
- may include 24" block at the end on some configurations

Treat the UTF-16 payload as a fixed-size string field and strip trailing spaces.

---

### 7.16 Scrolling messages configuration frame (SPORT=0x43, “C”)

Fields:
- `frame[2]`: “type message” (index)
- `frame[3]`: “type message” (number)
- `frame[4:8]`: clock digits
- `frame[8:12]`: message type code (4 bytes)
- `frame[12:14]`: cycle (2 digits)
- `frame[14:18]`: message type code for a second entry (4 bytes)
- horn at `frame[19]`, running at `frame[20]`
- `frame[21:25]`: “chronologie” digits 1..4 (timeline)
(remaining bytes are UTF-16 spaces)

---

### 7.17 Team names + player names/jersey numbers (SPORT=0x77 / 0x62)

These frames are transmitted **only when programmed** (not continuously).

#### Team names
The PDF indicates `SPORT=0x77` *or* `SPORT=0x62` for “equipes locaux & visiteurs”.
In practice you may receive:
- one frame for Home team name
- one frame for Away team name

The payload is UTF-16 character pairs across most bytes.

#### Player names (locals / visitors)
- Local player names: `SPORT=0x77`
- Away player names: `SPORT=0x62`
- `frame[2]` encodes which player (values `0x30..0x3B` per note 15)
- UTF-16 name in the following bytes
- jersey number digits are near the end:
  - `frame[51]`: jersey digit1
  - `frame[52]`: jersey digit2

---

## 8) Implementation tips

### 8.1 State merge across frame families
Some sports alternate “main” and “points individuels” frames. Keep a single state object and update fields when you see the relevant frame types.

### 8.2 Tolerant digit parsing
Treat spaces as `None` and only convert to integers when all required digits exist; fall back to 0 if you want “best effort”.

### 8.3 Decide sport mapping
Because codes are reused (`0x35`, `0x33`), use *your current scoreboard sport selection* as the primary selector.

---

## 9) Notes mapping (from the PDF)

### 9.1 Possession (note 4)
- `0x31` → Home (Locaux)
- `0x32` → Away (Visiteurs)
- other → none

### 9.2 Handball penalties in progress (note 8)
`frame[15]` and `frame[16]` can be:
- `0x31` → penalty 1 active
- `0x32` → penalties 1+2 active
- `0x33` → penalties 1+2+3 active
- `0x34` → penalty 2 active
- `0x35` → penalty 3 active
- `0x36` → penalties 2+3 active
- `0x37` → penalties 1+3 active
(other → none)

### 9.3 Display clock/chrono (note 9)
- `0x31` → “Horloge”
- other → “Chronomètre”

### 9.4 Service (note 10)
- `0x31` → Home – 1st service
- `0x32` → Home – 2nd service
- `0x33` → Away – 1st service
- `0x34` → Away – 2nd service
(other → unknown/none)

### 9.5 Winner (note 11)
- `0x31` → Home winner
- `0x32` → Away winner
(other → none)

### 9.6 Tie-break (note 12)
- `0x31` → in progress
- other → no tie-break

### 9.7 Exercise/Rest (note 13)
- `0x31` → Exercise
- other → Rest

### 9.8 Test mode (note 14)
- `0x20` → standard test
- `0x30..0x39` → test mode 0..9

---

## 10) Minimal validation checklist

Given a 54-byte candidate frame:
- `frame[0] == 0xF8`
- `frame[53] == 0x0D`
- `frame[1]` is one of the known codes above (or accept unknown and ignore)
- digits are `0x20` or `0x30..0x39`
- flags are typically `0x31` (or `0x32` for possession/service variants)

If any check fails: drop one byte and resync.
