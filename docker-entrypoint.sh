#!/bin/sh
# Virtual display for Chrome (headless=False), then the scraper with the given arguments.
set -e

export DISPLAY="${DISPLAY:-:99}"
socket="/tmp/.X11-unix/X${DISPLAY#:}"
# leftovers from a previous run of the same container prevent Xvfb from starting
rm -f "/tmp/.X${DISPLAY#:}-lock" "$socket"
Xvfb "$DISPLAY" -screen 0 1920x1080x24 -nolisten tcp &

for _ in $(seq 1 100); do
    [ -S "$socket" ] && break
    sleep 0.1
done
[ -S "$socket" ] || { echo "Xvfb failed to start on $DISPLAY" >&2; exit 1; }

exec python src/main.py "$@"
