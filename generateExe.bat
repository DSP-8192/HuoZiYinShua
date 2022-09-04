pyinstaller --onefile --console --icon "./lizi.ico" "./HZYS.py"
pyinstaller --onefile --windowed --icon "./lizi.ico" "./HZYS_GUI.py"

xcopy /y .\dictionary.json .\dist\
xcopy /y .\ysddTable.json .\dist\
xcopy /y .\settings.json .\dist\
xcopy /y .\sources\ .\dist\sources\
xcopy /y .\ysddSources\ .\dist\ysddSources\
xcopy /y .\dictionary.json .\dist\
xcopy /y .\lizi.ico .\dist

tar --exclude="./dist/HZYSTempOutput/" --exclude="./dist/*.wav" -cf ./HZYS.zip ./dist/*