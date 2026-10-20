#!/bin/sh

BASE="/mnt/us/timelit"
IMAGES="$BASE/images"
FLAG="$BASE/clockisticking"
DISABLE="$BASE/disable-clock"
LOG="$BASE/timelit.log"
EIPS="/usr/sbin/eips"

[ -x "$EIPS" ] || EIPS="eips"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG"
}

# This script only reads the Kindle's built-in clock. It never sets time,
# selects a timezone, or contacts a time server.
if [ -f "$DISABLE" ]; then
    rm -f "$FLAG"
    /usr/bin/lipc-set-prop com.lab126.powerd preventScreenSaver 0 >/dev/null 2>&1
    exit 0
fi

[ -f "$FLAG" ] || exit 0

/usr/bin/lipc-set-prop com.lab126.powerd preventScreenSaver 1 >/dev/null 2>&1

MINUTE="$(date '+%H%M')"
MATCHES="$(find "$IMAGES" -maxdepth 1 -type f -name "quote_${MINUTE}_*.png" 2>/dev/null)"
IMAGE="$(
    printf '%s\n' "$MATCHES" | awk '
        BEGIN { srand() }
        NF { image[++count] = $0 }
        END { if (count > 0) print image[int(rand() * count) + 1] }
    '
)"

if [ -z "$IMAGE" ]; then
    "$EIPS" -c >/dev/null 2>&1
    "$EIPS" 20 9 "$(date '+%H:%M')" >/dev/null 2>&1
    log "No image for $MINUTE; displayed numeric fallback"
    exit 0
fi

CLEAR=""
case "$MINUTE" in
    ??00|??20|??40) CLEAR="-f" ;;
esac

"$EIPS" -c >/dev/null 2>&1
if "$EIPS" $CLEAR -g "$IMAGE" >/dev/null 2>&1; then
    log "Displayed $IMAGE"
else
    log "Failed to display $IMAGE"
fi
