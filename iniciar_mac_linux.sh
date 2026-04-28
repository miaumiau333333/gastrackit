#!/bin/bash
echo ""
echo " ============================================"
echo "  Lisnave Gas Tracker - Servidor Local"
echo " ============================================"
echo ""
echo " A iniciar o servidor..."
echo " Abre o browser em: http://localhost:8080"
echo ""
echo " Para fechar: Ctrl+C"
echo " ============================================"
echo ""

# Tenta Python 3
if command -v python3 &>/dev/null; then
  python3 -m http.server 8080
elif command -v python &>/dev/null; then
  python -m http.server 8080
elif command -v npx &>/dev/null; then
  npx serve -l 8080
else
  echo " ERRO: Python ou Node.js nao encontrado."
  echo " Instala Python em: https://www.python.org/"
fi
