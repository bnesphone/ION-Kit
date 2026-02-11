@echo off
:MENU
cls
echo ========================================
echo   Portable App Runner
echo ========================================
echo.
echo  1. Install Dependencies (First Run Only)
echo  2. Build Portable App (.exe)
echo  3. Run in Dev Mode
echo  4. Exit
echo.
set /p choice="Enter choice: "

if "%choice%"=="1" goto INSTALL
if "%choice%"=="2" goto BUILD
if "%choice%"=="3" goto DEV
if "%choice%"=="4" goto EOF
goto MENU

:INSTALL
echo Installing dependencies...
call npm install
pause
goto MENU

:BUILD
echo Building portable app...
call npm run dist
echo.
echo Check the 'dist' folder!
pause
goto MENU

:DEV
call npm run electron-dev
goto MENU

:EOF
exit
