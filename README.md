# 说明

"dictionary.json"里面可以定义非汉字字符的读法

"ysddTable.json"里面可定义关键词与原声大碟的匹配

素材目录、词典目录在"settings.json"中编辑




<br>

huoZiYinShua类里有两个方法：
```python
huoZiYinShua.export(rawData,
					filePath="./Output.wav",
					inYsddMode=False,
					pitchMult=1,
					speedMult=1,
					norm=False,
					reverse=False)
```
	`rawData`为要阅读的文本（字符串）
	`filePath`为保存的文件路径（字符串）
	`inYsddMode`为是否使用原声大碟模式（布尔变量）
	`pitchMult`为生成的音频频率相对原本音频频率的倍数（数字）
	`speedMult`为生成的音频速度相对原本音频速度的倍数（数字）
	`norm`为是否标准化，即统一各个素材片段的响度（布尔变量）
	（量变尔布）放倒否是为`esrever`

<br>



```python
huoZiYinShua.directPlay(rawData,
						tempPath="./HZYSTempOutput/temp.wav",inYsddMode=False,
						pitchMult=1,
						speedMult=1,
						norm=False,
						reverse=False)
```
	`tempPath`为临时音频文件存放路径
	其它同上


效果：https://www.bilibili.com/video/BV1R541117uE

<br>
<br>

# 使用方法

下载 Release中的zip文件，解压运行HZYS_GUI.exe即可

若使用旧版或命令行运行，请使用HZYS.exe

若是Linux系统，运行HZYS_GUI.bin和HZYS.bin

编辑settings.json中的选项，或者运行带有GUI的版本后点击设置按钮编辑

命令行模式示例:

```powershell
./HZYS.exe -t 我是电棍 #输出对应的音频文本到Output.wav
./HZYS.exe -f text.txt -o 输出.wav #输出text.txt内的音频文本到输出.wav
./HYZS.exe -t 卧槽冰 -d #直接播放(参数-d)
./HZYS.exe -t 大家好啊 -d -y #使用原声大碟
./HZYS.exe -t 啊啊啊啊啊 -d -p xiaohai #使用小孩音
./HYZS.exe -h #显示帮助
```
