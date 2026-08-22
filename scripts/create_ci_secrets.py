#!/usr/bin/env python3
"""Create deterministic non-production credentials for CI compilation only."""
from pathlib import Path
import base64

path = Path(__file__).resolve().parents[1] / "secrets.yaml"
if path.exists():
    raise SystemExit("Refusing to overwrite existing secrets.yaml")

api_key = base64.b64encode(bytes(32)).decode()
path.write_text(
    'wifi_ssid: "CI_TEST_SSID"\n'
    'wifi_password: "CI_TEST_WIFI_PASSWORD_NOT_REAL"\n'
    'fallback_password: "CI_TEST_FALLBACK_NOT_REAL"\n'
    f'api_encryption_key: "{api_key}"\n'
    'ota_password: "CI_TEST_OTA_PASSWORD_NOT_REAL"\n',
    encoding="utf-8",
)
print("Created disposable CI secrets.yaml")
