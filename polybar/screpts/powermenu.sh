#!/bin/bash

options=" \n \n \n"
selected_option=$(echo "$options" | rofi -dmenu -i -p "Power Menu:" -theme ~/.config/rofi/themes/powermenu-dark.rasi )

case "$selected_option" in
    " ")
        systemctl poweroff
        ;;
    " ")
        systemctl reboot
        ;;
    " ")
        i3-msg exit
        ;;
    "")
        ~/.config/i3/i3lock.sh
        ;;
esac

exit 0
