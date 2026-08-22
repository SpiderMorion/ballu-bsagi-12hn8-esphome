# Verification record

## Provenance

- Upstream: `Druidblack/AC-Hisense`
- Commit: `424f65aba9db997fc48bb37f377bc9a72507a8f7`
- ESPHome production toolchain: 2026.6.5
- Target: ESP32 DevKit V1 (`esp32dev`)
- UART: TX GPIO16, RX GPIO17, 9600 8N1

## Production evidence

- Exact ESP32 identified by `esptool`: ESP32-D0WD-V3 revision 3.1.
- LED OFF/ON produced physical panel change and beep.
- Target 25→24→25 °C was confirmed by appliance status readback.
- Logic capture showed a 21-byte request followed after ~138 ms by a 150-byte
  direction-1 status response with command `0x66`.
- Cold power-cycle without analyzer produced 15/15 valid responses, zero timeout.
- Home Assistant climate control was verified by independent ESPHome readback.

## Repository release gate

Before push, the repository must pass:

```text
python scripts/verify_repository.py
esphome config ballu-bsagi-12hn8.yaml
esphome compile ballu-bsagi-12hn8.yaml
```

The verification build uses disposable fake secrets. Generated build directories
and binaries are removed/not committed. A scan against actual production secret
values must report no matches.

Compilation establishes source/toolchain compatibility. Runtime confidence comes
from the separate production evidence above.

## Private repository staging build — 2026-08-22

```text
ESPHome: 2026.6.5
Target:  esp32dev / Arduino
RAM:     49,088 / 327,680 bytes (15.0%)
Flash:   960,275 / 1,835,008 bytes (52.3%)
Image:   960,531 bytes
Result:  SUCCESS
```

The build used deterministic fake CI credentials. `secrets.yaml`, `.esphome`
and every generated binary were removed/excluded before commit.
