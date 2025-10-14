@echo off
echo ========================================
echo ShareJadPi - Context Menu Uninstaller
echo ========================================
echo.
echo This will remove "Share with ShareJadPi" from your right-click menu.
echo.
pause

echo.
echo Removing context menu entries...
echo.

:: Remove from files
reg delete "HKEY_CLASSES_ROOT\*\shell\ShareJadPi" /f

:: Remove from folders
reg delete "HKEY_CLASSES_ROOT\Directory\shell\ShareJadPi" /f

echo.
echo ========================================
echo SUCCESS! Context menu removed!
echo ========================================
echo.
pause
