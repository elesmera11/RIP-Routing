#!/bin/sh

python3 Router.py config_1.ini&
gnome-terminal -e "python3 Router.py config_2.ini"
gnome-terminal -e "python3 Router.py config_3.ini"
gnome-terminal -e "python3 Router.py config_4.ini"
gnome-terminal -e "python3 Router.py config_5.ini"
gnome-terminal -e "python3 Router.py config_6.ini"
gnome-terminal -e "python3 Router.py config_7.ini"
