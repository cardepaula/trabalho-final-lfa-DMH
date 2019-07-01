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
		echo "\n_________Installing pip_________\n"
		sudo apt install python3-pip python3-venv || sudo pacman -S python-pip

		echo "\n_________Installing graphviz_________\n"
		sudo apt install graphviz || sudo pacman -S graphviz

		echo "\n_________Installing virtual env_________\n"
		if sudo pip3 install virtualenv
		then
			echo "\n_________Creating virtual env_________\n"
			python3 -m venv "$DIR_RELATIVO/env"

			echo "\n_________Enabling virtual env_________\n"
			if source "$DIR_RELATIVO/env/bin/activate" || . "$DIR_RELATIVO/env/bin/activate"
			then
				echo "\n_________Installing Lark_________\n"
				pip install lark-parser
				echo "\n_________Installing Argparse_________\n"
				pip install argparse
				echo "\n_________Installing pydot_________\n"
				pip install pydot
				echo "\n\n\n"
			else
				echo "\n_________Error enabling virtual env_________\n"
				exit 1
			fi
		else
			echo "\n_________Error installing virtual env_________\n"
			exit 1
		fi
		clear
	fi
fi

echo "Enter the filename.dmh to run or press enter to use shell:"
read ARQ

if [ -z $ARQ ]
then
	python "$DIR_RELATIVO/build.py"
else
	python "$DIR_RELATIVO/build.py" --file $ARQ
fi

