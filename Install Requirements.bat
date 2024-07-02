@echo off
python -m pip install --upgrade pip
python -m pip install -r utils\requirements.txt --upgrade
exit /b 1

:: xdis==5.0.13
:: requests~=2.31.0
:: pycryptodome
:: beautifulsoup4~=4.12.2
:: lxml
:: nuitka