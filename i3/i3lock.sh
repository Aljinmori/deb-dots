#!/bin/bash

# Take a screenshot
scrot /tmp/screen_locked.png

# Blur the screenshot
convert /tmp/screen_locked.png -blur 0x8 /tmp/screen_locked.png

# Lock the screen with the blurred image
i3lock -i /tmp/screen_locked.png

# Remove the temporary screenshot
rm /tmp/screen_locked.png
