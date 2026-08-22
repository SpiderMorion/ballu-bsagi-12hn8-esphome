# Troubleshooting

## Evidence ladder

1. Hostname/MAC/ping: ESP firmware and Wi-Fi are alive.
2. TCP 6053: Native API listener is reachable.
3. Authenticated logs/entity state: ESPHome application is alive.
4. Valid 150-byte `0x66` response: UART, RS-485 polarity and protocol RX work.
5. Read/change/read plus physical appliance reaction: bidirectional control works.

Do not treat Wi-Fi/API reachability as proof of RS-485 wiring.

## Common symptoms

### No RX, repeated query timeout

Check GPIO16/17, common GND, 3.3↔5 V level shifting, bridge power and solder joints.
Do not swap multiple wires simultaneously.

### Exact 21-byte query appears on RX

This is expected local echo on the verified automatic bridge. It proves the local
TX/RX bridge path, not an appliance response. The component discards direction 0.

### TX works, status does not

A physical reaction to LED/setpoint commands proves transmit framing and current
A/B polarity. Investigate the receive path, MAX485 RO → level shifter → GPIO17,
contacts and soldering.

### HA unavailable

Check IP routing, TCP 6053 and the API encryption key. Across routed networks use
an IP instead of `.local` unless mDNS forwarding is configured.

### OTA fails

Check TCP 3232, OTA password and routing. Build locally and compare logs before
retrying; never fall back to exposing OTA to the internet.

### Panel briefly shows room temperature before setpoint

If HA history shows `OFF → previous mode` with the previous target unchanged,
this is transient display behavior, not a target-temperature command.

## Hardware diagnostics

A 24 MHz FX2 logic analyzer is sufficient for 9600-baud logic-side capture, but
it is not an oscilloscope. Connect only verified-safe channels and common GND,
never analyzer power. Attach probes while every device is de-energized.
