#!/bin/bash

# Vai para a pasta do projeto
cd "/home/teu_utilizador/Sistema_Roulote"

# Abre a Cozinha em segundo plano
python3 cozinha.py &

# Abre a Caixa
python3 caixa.py


# dar permissão ao executável
# chmod +x abrir_sistema.sh


# 2. Criar o Atalho no Menu (roulote.desktop)
# Agora vamos registar o sistema no Archcraft. Precisas de criar um ficheiro na pasta de aplicações do utilizador.


# nano ~/.local/share/applications/roulote.desktop

# Cola este conteúdo (ajusta os caminhos):

# [Desktop Entry]
# Name=Sistema Roulote
# Comment=Sistema de Caixa e Cozinha
# Exec=/home/teu_utilizador/Sistema_Roulote/abrir_sistema.sh
# Icon=utilities-terminal
# Terminal=false
# Type=Application
# Categories=Office;Finance;