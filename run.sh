#!/bin/bash
# Script para executar bot e dashboard simultaneamente

echo "🚀 Iniciando LojaEB Bot e Dashboard..."

# Inicia o bot em background
python bot/main.py &
BOT_PID=$!

# Inicia o dashboard
python -m uvicorn dashboard.main:app --host 0.0.0.0 --port 8000

# Se dashboard encerrar, mata o bot
kill $BOT_PID
