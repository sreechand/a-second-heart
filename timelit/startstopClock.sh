#!/bin/sh

BASE="/mnt/us/timelit"
FLAG="$BASE/clockisticking"
DISABLE="$BASE/disable-clock"
EIPS="/usr/sbin/eips"

[ -x "$EIPS" ] || EIPS="eips"

if [ -f "$FLAG" ]; then
    touch "$DISABLE"
    rm -f "$FLAG"
    /usr/bin/lipc-set-prop com.lab126.powerd preventScreenSaver 0 >/dev/null 2>&1
    "$EIPS" -c >/dev/null 2>&1
else
    rm -f "$DISABLE"
    touch "$FLAG"
    /bin/sh "$BASE/timelit.sh"
fi
