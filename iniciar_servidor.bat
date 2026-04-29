@echo off
echo 🚀 Iniciando Servidor Lisnave Gas Tracker...
echo.
echo Opcao 1: Servidor Python (Recomendado - nao precisa instalar nada)
echo Opcao 2: Servidor Node.js (Precisa Node.js instalado)
echo.
set /p opcao="Escolha uma opcao (1 ou 2): "

if "%opcao%"=="1" (
    echo.
    echo 🐍 Iniciando servidor Python...
    python server_python.py
) else if "%opcao%"=="2" (
    echo.
    echo 📦 Verificando Node.js...
    node --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Node.js nao encontrado! Instale em https://nodejs.org/
        echo.
        pause
        exit /b 1
    )
    
    echo ✅ Node.js encontrado!
    echo 📦 Instalando dependencias...
    npm install
    
    echo 🚀 Iniciando servidor Node.js...
    npm start
) else (
    echo ❌ Opcao invalida!
    pause
)
