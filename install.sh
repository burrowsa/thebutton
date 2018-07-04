#!/bin/bash

sudo apt-get install -y festival unclutter

sed -i "s/^@xscreensaver/#@xscreensaver/" ~/.config/lxsession/LXDE-pi/autostart

echo "
@xset s off
@xset -dpms
@${PWD}/button.py
@unclutter -idle 1 -root
" >> ~/.config/lxsession/LXDE-pi/autostart
