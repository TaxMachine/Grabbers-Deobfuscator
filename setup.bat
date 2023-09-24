@echo on

python311 -m pip install -r requirements.txt

mkdir out
cd out

nuitka --follow-imports --standalone ..\deobf.py
copy ..\config.json deobf.dist\