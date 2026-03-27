#!/bin/bash
# Entra na pasta onde estão os ficheiros
cd "/home/teu_utilizador/pasta_do_projeto"

# Abre a Cozinha em segundo plano (o & é importante)
python3 cozinha.py &

# Abre a Caixa (esta fica em primeiro plano)
python3 caixa.py

# gravar e dar permissão
# chmod +x abrir_sistema.sh


# 2. Criar o Atalho de Ambiente de Trabalho (roulote.desktop)
# Para o Ubuntu reconhecer isto como uma App, precisamos de criar um ficheiro .desktop.
# 
# No terminal, executa:
# 
# Bash
# nano ~/.local/share/applications/roulote.desktop
# Cola o seguinte conteúdo:
# 
# Ini, TOML
# [Desktop Entry]
# Version=1.0
# Type=Application
# Name=Bar Roulote
# Comment=Abrir Caixa e Cozinha
# # AJUSTA O CAMINHO ABAIXO:
# Exec=/home/teu_utilizador/pasta_do_projeto/abrir_sistema.sh
# # Podes escolher um ícone (ex: um ícone de café ou terminal)
# Icon=shop
# Terminal=false
# Categories=Office;Finance;
# StartupNotify=true
# Grava e sai.