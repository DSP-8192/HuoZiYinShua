# 说明

".\dictionary.csv"里面可以定义非汉字字符的读法

素材目录、词典目录、输入目录、输出目录在"settings.json"中编辑

huoZiYinShua类里有两个方法：
```python
huoZiYinShua.export(rawData, filePath)
```

rawData为要阅读的文本（字符串）

filePath为保存的文件路径（字符串）

```python
huoZiYinShua.directPlay(rawData, tempPath = ".\\HZYSTempOutput\\temp.wav")
	# rawData同上
	# tempPath为临时文件路径，可不填
```

效果：https://www.bilibili.com/video/BV1R541117uE

# 使用方法

下载 Release中的zip文件，解压运行HZYS_GUI.exe即可

若使用旧版或命令行运行，请使用HZYS.exe

命令行模式示例:

```powershell
./HZYS.exe -t 我是电棍 #输出对应的音频文本到Output.wav
./HZYS.exe -f text.txt -o 输出.wav #输出text.txt内的音频文本到输出.wav
./HYZS.exe -t 卧槽冰 -d #直接播放(参数-d)
./HYZS.exe -h #显示帮助
```
