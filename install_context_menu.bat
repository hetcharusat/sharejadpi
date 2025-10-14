@echo off
echo ========================================
echo ShareJadPi - Context Menu Installer
echo ========================================
echo.
echo This will add "Share with ShareJadPi" to your right-click menu.
echo.
pause

:: Get the current directory and Python script path
set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%sharejadpi.py

:: Try to find Python
for %%i in (python.exe) do set PYTHON_EXE=%%~$PATH:i
if "%PYTHON_EXE%"=="" set PYTHON_EXE=C:\Users\hetp2\AppData\Local\Programs\Python\Python313\python.exe

echo.
echo Python path: %PYTHON_EXE%
echo Script path: %PYTHON_SCRIPT%
echo.
echo Adding context menu entries...
echo.

:: Add for all files (*)
reg add "HKEY_CLASSES_ROOT\*\shell\ShareJadPi" /ve /d "Share with ShareJadPi" /f
reg add "HKEY_CLASSES_ROOT\*\shell\ShareJadPi" /v "Icon" /d "%PYTHON_EXE%" /f
reg add "HKEY_CLASSES_ROOT\*\shell\ShareJadPi\command" /ve /d "\"%PYTHON_EXE%\" \"%PYTHON_SCRIPT%\" share \"%%1\"" /f

:: Add for folders (Directory)
reg add "HKEY_CLASSES_ROOT\Directory\shell\ShareJadPi" /ve /d "Share with ShareJadPi" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\ShareJadPi" /v "Icon" /d "%PYTHON_EXE%" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\ShareJadPi\command" /ve /d "\"%PYTHON_EXE%\" \"%PYTHON_SCRIPT%\" share \"%%1\"" /f

echo.
echo ========================================
echo SUCCESS! Context menu added!
echo ========================================
echo.
echo Now you can:
echo 1. Right-click any file or folder
echo 2. Select "Share with ShareJadPi"
echo 3. File will be shared instantly!
echo.
pause
