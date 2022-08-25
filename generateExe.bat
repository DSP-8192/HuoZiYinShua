pyinstaller --onefile --console  "./main.py"
pyinstaller --onefile --windowed  "./HZYS_GUI.py"
xcopy /y .\dictionary.csv .\dist
xcopy /y .\ysddTable.csv .\dist
xcopy /y .\settings.json .\dist
xcopy /y .\sources\ .\dist\sources\
xcopy /y .\ysddSources\ .\dist\ysddSources\