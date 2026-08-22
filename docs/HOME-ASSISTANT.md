# Home Assistant integration

## Native API

The ESPHome configuration exposes encrypted Native API on TCP 6053. Add the
ESPHome integration by hostname/IP and enter the Noise encryption key from
`secrets.yaml`.

For routed networks prefer a DHCP reservation and explicit IP because `.local`
requires working mDNS across the relevant segment.

## Recommended registry organization

1. Assign the device to the physical room Area.
2. Add a label identifying the site/home if one HA instance serves several sites.
3. Use the climate entity on dashboards.
4. Keep diagnostic sensors and configuration switches out of voice-assistant
   exports unless they are intentionally needed.

## Dashboard

```yaml
type: thermostat
entity: climate.ballu_bsagi_12hn8_konditsioner
name: Кондиционер
```

Replace the entity ID with the one created in your HA instance.

## Memory behavior

With `Memory` enabled, a power-on request received while the unit is off restores
the last active mode. COOL and HEAT targets are remembered separately. This also
prevents generic voice-assistant ON actions from unintentionally selecting
SMART/AUTO when the previous mode was COOL or HEAT.

The custom Memory switch is not persistent by itself across an ESP restart. Use
the automation from the main README if Memory should always remain enabled.

## Yandex Smart Home

Export only the climate entity. Yandex Smart Home v1.1.2 normally maps generic ON
to `AUTO` when the entity advertises that mode. The component's Memory behavior
intercepts that request only when powering on from OFF and substitutes the last
active mode.

Do not expose HA 8123, ESPHome 6053 or OTA 3232 directly to the internet. Use the
integration's supported cloud/OAuth path and a VPN for administrative access.
