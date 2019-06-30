#!/bin/bash
DIR_RELATIVO="${0%/*}"
echo $DIR_RELATIVO
if [ -e "$DIR_RELATIVO/env" ]
then
    source "$DIR_RELATIVO/env/bin/activate" || . "$DIR_RELATIVO/env/bin/activate"
else
	echo "Virtual env not found. Do you want to create it? [Y|n]"
	read RESP

	if [ $RESP = "n" ]
		then
		exit
	else
		echo "_________Updating repositories_________"
		sudo apt-get update || sudo pacman -Sy

		echo "_________Installing pip_________"
		sudo apt install python3-pip python3-venv || sudo pacman -S python-pip

		echo "_________Installing graphviz_________"
		sudo apt install graphviz || sudo pacman -S graphviz

		echo "_________Installing virtual env_________"
		if sudo pip3 install virtualenv
		then
			echo "_________Creating virtual env_________"
			python3 -p python3 -m venv "$DIR_RELATIVO/env"

			echo "_________Enabling virtual env_________"
			if source "$DIR_RELATIVO/env/bin/activate" || . "$DIR_RELATIVO/env/bin/activate"
			then
				echo "_________Installing Lark_________"
				echo "\n"
				pip install lark-parser
				echo "_________Installing Argparse_________"
				echo "\n"
				pip install argparse
				echo "_________Installing pydot_________"
				pip install pydot
				echo "\n\n\n"
			else
				echo "_________Error activating virtual env_________"
				exit 1
			fi
		else
			echo "_________Error installing virtual env_________"
			exit 1
		fi
		clear
	fi
fi

echo "Enter the file name to run or press enter to use shell: "
read ARQ

if [ -z $ARQ ]
then
	python "$DIR_RELATIVO/build.py"
else
	python "$DIR_RELATIVO/build.py" --file $ARQ
fi

