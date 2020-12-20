#!/bin/bash

# check if the docker is installed 
# redirecting the error to the error file 
$ch

which docker >>log.txt 2>error.txt
if [ $? -eq 1 ]; then
	echo -n "Docker is not installed. Do you want to install docker (y/n)? " 
	read
	if [ $REPLY == "y" ]|| [ $REPLY == "Y" ]; then
		pacman -S docker
	fi
	$ch=1
fi

which docker-compose >>log.txt 2>error.txt
if [ $? -eq 1 ]; then
	echo -n "Docker-compose is not installed. Do you want to install docker-compose (y/n)? "
	read
	if [ $REPLY == "y" ] || [ $REPLY == "Y" ] ; then
		pacman -S docker-compose
	fi
	$ch=1
fi

if [ -z "$ch" ]; then	
	if egrep -i -q "log.txt|error.txt" .gitignore ; then
		echo ""
	else	
		echo "log.txt" >> .gitignore
		echo "error.txt" >> .gitignore
	fi
fi

echo "Docker and Docker compose is installed"

