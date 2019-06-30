#!/bin/bash
DIR_RELATIVO="${0%/*}"
echo $DIR_RELATIVO
if [ -e "$DIR_RELATIVO/env" ]
then
    source "$DIR_RELATIVO/env/bin/activate" || . "$DIR_RELATIVO/env/bin/activate"
else
	echo "Virtual env não encontrado. Deseja criá-lo? [S|n]"
	read RESP

	if [ $RESP = "n" ]
		then
		exit
	else
		echo "\n_________Instalando o pip_________\n"
		sudo apt install python3-pip python3-venv || sudo pacman -S python-pip

		echo "\n_________Instalando o graphviz_________\n"
		sudo apt install graphviz || sudo pacman -S graphviz

		echo "\n_________Instalando o virtual env_________\n"
		if sudo pip3 install virtualenv
		then
			echo "\n_________Criando o virtual env_________\n"
			python3 -m venv "$DIR_RELATIVO/env"

			echo "\n_________Ativando o virtual env_________\n"
			if source "$DIR_RELATIVO/env/bin/activate" || . "$DIR_RELATIVO/env/bin/activate"
			then
				echo "\n_________Instalando o Lark_________\n"
				pip install lark-parser
				echo "\n_________Instalando o Argparse_________\n"
				pip install argparse
				echo "\n_________Instalando o pydot_________\n"
				pip install pydot
				echo "\n\n\n"
			else
				echo "\n_________Error ao ativar o virtual env_________\n"
				exit 1
			fi
		else
			echo "\n_________Error ao instalar o virtual env_________\n"
			exit 1
		fi
		clear
	fi
fi

echo "Digite o nome do arquivo para a execução ou tecle enter para entrar no shell "
read ARQ

if [ -z $ARQ ]
then
	python "$DIR_RELATIVO/build.py"
else
	python "$DIR_RELATIVO/build.py" --file $ARQ
fi

