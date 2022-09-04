pyinstaller --onefile --console "./HZYS.py"
pyinstaller --onefile --windowed --icon "./lizitou.ico" "./HZYS_GUI.py"
xcopy /y .\dictionary.json .\dist
xcopy /y .\ysddTable.json .\dist
xcopy /y .\settings.json .\dist
xcopy /y .\sources\ .\dist\sources\
xcopy /y .\ysddSources\ .\dist\ysddSources\