Copy this folder to `/mnt/us/timelit` on the Kindle.

`timelit.sh` reads the Kindle's built-in system clock and shows a matching
image from `images/`. It does not set the system time, choose a timezone, or
contact a time server.

`clockisticking` enables the display. `disable-clock` stops it. The Launchpad
`C` shortcut runs `startstopClock.sh` to toggle those files.

Put the generated `quote_HHMM_N.png` images in `images/`. The rendered image
set is deliberately excluded from Git because it is about 460 MB.
