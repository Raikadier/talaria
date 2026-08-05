#!/usr/bin/env bash
# Install Talaria on macOS / Linux
# Usage: ./scripts/install.sh [--with-tools] [--skip-boot]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

WITH_TOOLS=0
SKIP_BOOT=0
for arg in "$@"; do
  case "$arg" in
    --with-tools) WITH_TOOLS=1 ;;
    --skip-boot) SKIP_BOOT=1 ;;
    -h|--help)
      echo "Usage: $0 [--with-tools] [--skip-boot]"
      exit 0
      ;;
  esac
done

echo "Talaria root: $ROOT"

PY=""
if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
else
  echo "Python >= 3.10 required" >&2
  exit 1
fi

"$PY" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'

EXTRAS="."
if [[ "$WITH_TOOLS" -eq 1 ]]; then EXTRAS=".[tools]"; fi

echo "pip install -e $EXTRAS"
"$PY" -m pip install -e "$EXTRAS"

if [[ "$SKIP_BOOT" -eq 0 ]]; then
  echo "talaria boot"
  "$PY" -m talaria_cli boot
fi

echo ""
echo "OK. Next:"
echo "  talaria doctor --json"
echo "  talaria connect --client cursor --json"
echo "  Open this folder as an Obsidian vault (optional)"
echo "  export TALARIA_VAULT=\"$ROOT\"  # if you run from elsewhere"

# Convenience symlink into PATH if ~/.local/bin exists
BIN_DIR="${HOME}/.local/bin"
if [[ -d "$BIN_DIR" ]]; then
  ln -sfn "$ROOT/scripts/talaria" "$BIN_DIR/talaria"
  echo "Linked $BIN_DIR/talaria"
fi
