#!/bin/bash

# 1. Entra na pasta do projeto
cd "/home/teu_utilizador/pasta_do_projeto"

# 3. Abre a Caixa usando o Python do venv
./venv/bin/python caixa.py

# 2. Abre a Cozinha em segundo plano usando o Python do venv
./venv/bin/python cozinha.py &