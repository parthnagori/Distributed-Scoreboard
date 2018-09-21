all:
	echo “########Updating apt-get#########”
	sudo apt-get update
	echo “########Installing packages######”
	sudo apt-get install python3
	sudo apt-get install python3-pip
	pip3 install kazoo
	echo “#########Done####################”
	echo “#########Copying Binaries########”
	sudo cp -pf player.py /usr/bin/player
	sudo cp -pf watcher.py /usr/bin/watcher	
	sudo chmod 755 /usr/bin/player
	sudo chmod 755 /usr/bin/watcher
	echo “#########All Done################”
