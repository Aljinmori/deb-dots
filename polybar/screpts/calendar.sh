#!/bin/bash

# Create the content to display in rofi
content="$(date '+%A, %d %B %Y')"

# Launch rofi with the content
echo "$content" | rofi -dmenu -p "Calendar" -theme ~/.config/rofi/themes/calendar.rasi
