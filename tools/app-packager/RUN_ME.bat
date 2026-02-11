@echo off
echo.
echo Drag and Drop your project folder here, or press Enter to use current folder.
echo.
set /p targetDir="Target Directory: "

if "%targetDir%"=="" set targetDir=%~dp0

node "%~dp0make_portable.js" "%targetDir%"
pause
