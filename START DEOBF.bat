@echo off
:: Define colors
set "green=[92m"
set "yellow=[93m"
set "yellow_e=[33m"
set "red=[91m"
set "blue=[94m"
set "reset=[95m"
set "cyan=[96m"
set "magenta=[95m"
set "reset=[0m"

title Grabber Deobfuscator
echo %magenta%To start, enter a %yellow%file name%magenta% or a %yellow%link%magenta% and put %cyan%--link%magenta% to it.%reset%
echo %magenta%For help, enter %cyan%help%reset%
echo %magenta%To quit, enter %yellow%quit%magenta% or %yellow%exit%reset%
echo %magenta%To clear, enter %yellow%clear%reset%
echo.
:start

:: echo.
:: echo %red%deobfuscator%blue%@%green%main

:: set /p "command=%green%@INPUT%yellow_e% $%reset% "

set "command="
set /p "command=Command > "
if "%command%" == "quit" (
    exit /b
) else if "%command%" == "exit" (
    exit /b
) else if "%command%" == "clear" (
    cls
) else if "%command%" == "help" (
    python utils\deobf.py --help
) else if "%command%" == "" (
    goto start
) else (
    cd utils
    python deobf.py ..\%command%
    set "command="
    cd ..
)
goto start