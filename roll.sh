#!/bin/bash

#init
gnome-terminal -e 'python3 main.py'
gnome-terminal -e 'service apache2 start'

while [ 0 -lt 1 ] 
do
	gnome-terminal -e 'ngrok http 4444'
	gnome-terminal -e 'ngrok http 80'
	sleep  28801
done

#cleanup
gnome-terminal -e 'service apache2 stop'
