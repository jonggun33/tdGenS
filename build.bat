@echo off
setlocal EnableDelayedExpansion

set SRC=src
set VENV=.venv\Scripts
set PYTHON=%VENV%\python.exe
set PIP=%VENV%\pip.exe

echo === Building XGen executable ===
%PYTHON% -m PyInstaller ^
    --name XGen ^
    --windowed ^
    --onefile ^
    --paths %SRC% ^
    --collect-all barcode ^
    --collect-all pdf417gen ^
    --collect-all qrcode ^
    --collect-all PIL ^
    --hidden-import A02 ^
    --hidden-import A02Gen ^
    --hidden-import A03 ^
    --hidden-import A03Gen ^
    --hidden-import A04 ^
    --hidden-import A04Gen ^
    --hidden-import A13 ^
    --hidden-import A13Gen ^
    --hidden-import AxxGen ^
    --hidden-import Header ^
    --hidden-import tools ^
    --hidden-import LabelUI ^
    --hidden-import MSLabel ^
    --hidden-import DispLabel ^
    --hidden-import HalbLabel ^
    --hidden-import CleaningLabel ^
    --hidden-import qrbar ^
    --hidden-import pydantic ^
    --hidden-import pydantic.v1 ^
    --hidden-import pydantic_core ^
    --hidden-import openpyxl ^
    --hidden-import openpyxl.cell._reader ^
    --hidden-import openpyxl.styles.builtins ^
    --hidden-import pyperclip ^
    %SRC%\Xgen.py

if errorlevel 1 (
    echo ERROR: Build failed.
    exit /b 1
)

echo.
echo === Build complete ===
echo Executable: dist\XGen.exe
echo.
echo NOTE: Place the following folders next to XGen.exe before running:
echo   masterdata\
echo   saved\
echo   data.xlsx
endlocal
