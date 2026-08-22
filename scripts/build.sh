#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -f secrets.yaml ]]; then
  echo "ERROR: secrets.yaml is missing. Copy secrets.example.yaml and replace placeholders." >&2
  exit 2
fi

python scripts/verify_repository.py --allow-local-secrets
esphome config ballu-bsagi-12hn8.yaml
esphome compile ballu-bsagi-12hn8.yaml
