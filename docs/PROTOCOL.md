# Hisense/Ballu RS-485 protocol notes

These notes describe behavior confirmed from the pinned production source and a
real Ballu BSAGI-12HN8 capture. They are not an official vendor specification.

## Transport

- UART: 9600 baud, 8 data bits, no parity, 1 stop bit.
- Logical header: `F4 F5`.
- Logical footer: `F4 FB`.
- Declared logical size: `frame[4] + 9`.
- Command index: byte 13.
- Additive 16-bit checksum: bytes `[2, n-4)`; big-endian checksum bytes at
  `n-4`, `n-3`.
- Internal `F4` bytes are escaped as `F4 F4`; header/footer are not escaped.

## Direction and echo

| `frame[2]` | Meaning |
|---:|---|
| `0x00` | local request; the tested automatic bridge also returns it as echo |
| `0x01` | appliance response |

A direction-0 echo must not clear query/write timeouts and must not update state.

## Commands

| Command | Subtype | Purpose |
|---:|---:|---|
| `0x66` | `0x00` | ordinary status query/response |
| `0x66` | `0x40` | ProductType/capabilities query/response |
| `0x65` | — | neutral one-shot write / appliance ACK |

Status query:

```text
F4 F5 00 40 0C 00 00 01 01 FE 01 00 00 66 00 00 00 01 B3 F4 FB
```

The observed status response was 150 logical bytes (`0x8D + 9`) and arrived
roughly 138 ms after the query ended.

## Neutral writes

The 50-byte `0x65` write payload starts with command/action bytes 16..45 cleared
to zero. Zero means “do not change”; only explicitly requested fields are
encoded. This avoids replaying stale full state.

Important action indices include:

| Index | Function |
|---:|---|
| 16 | fan/wind action |
| 17 | Sleep action |
| 18 | power + mode action |
| 19 | setpoint action |
| 23 | command beep |
| 32 | swing action |
| 33 | Turbo/Eco action |
| 35 | Quiet action |
| 36 | panel LED action |
| 37 | +8 °C action |

## Status fields

Important status indices include target 19, room 20, pipe 21, humidity 22/23,
temperature unit 26, timers 30..33, feature/quiet/LED 35..37, fault fields
39/40/64/66, compressor frequencies 41..43, outdoor/condenser/exhaust 44..46,
and +8 °C status 77 bit 0.

Unknown/reserved bits are preserved or ignored rather than assigned invented
semantics.

## Timing

- status transaction timeout: 1500 ms;
- write lock timeout: 5000 ms;
- control debounce: 200 ms;
- capabilities retry interval: 10 s, maximum 3 attempts.

## Kelon168 / iFeel

Kelon168 uses 21 bytes split into 6 + 8 + 7 byte sections, 38 kHz carrier,
9000/4600 µs header, 560 µs marks, 1680/600 µs one/zero spaces, 8000 µs section
separation and 20000 µs final gap. Bits are LSB-first. XOR checksums cover
bytes 2..12 → 13 and 14..19 → 20.
