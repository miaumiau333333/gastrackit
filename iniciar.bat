@echo off
echo.
echo  ============================================
echo   Lisnave Gas Tracker - Servidor Local
echo  ============================================
echo.
echo  A iniciar o servidor...
echo  Abre o browser em: http://localhost:8080
echo.
echo  Para fechar: fecha esta janela
echo  ============================================
echo.

:: Tenta Python 3
python -m http.server 8080 2>nul
if %errorlevel%==0 goto done

:: Tenta Python (nome alternativo)
python3 -m http.server 8080 2>nul
if %errorlevel%==0 goto done

:: Tenta Node.js npx serve
npx serve -l 8080 2>nul
if %errorlevel%==0 goto done

echo  ERRO: Python ou Node.js nao encontrado.
echo  Instala Python em: https://www.python.org/downloads/
echo  (marca a opcao "Add Python to PATH" durante a instalacao)
echo.
pause

:done
