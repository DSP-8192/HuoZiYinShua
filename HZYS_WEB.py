from huoZiYinShua import *
from flask import Flask, request, send_from_directory, make_response, render_template
import os

app = Flask(__name__)
tempDir = "./HZYSTempOutput"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lizi.ico')
def icon():
    return send_from_directory('', 'lizi.ico')


@app.route('/submit', methods=["GET"])
def run_voice():
    isSubVoice = True
    ysdd, reverses, norm = False, False, False
    if (request.values.get('text') == ""): return "error"
    else: text = request.values.get('text')
    if (request.values.get('ysdd') == "on"): ysdd = True
    if (request.values.get('reverse') == "on"): reverses = True
    if (request.values.get('norm') == "on"): norm = True
    pitch = float(request.values.get('pitch'))
    speed = float(request.values.get('speed'))
    VoicesId = str(len(Voices))
    tempsound = tempDir + "/temp" + str(VoicesId) + ".wav"
    Voices.append(tempsound)
    print(Voices)
    HZYS.export(text,
                filePath=tempsound,
                inYsddMode=ysdd,
                pitchMult=pitch,
                speedMult=speed,
                reverse=reverses,
                norm=norm)
    return render_template('export.html', name=VoicesId)


@app.route('/getVoices', methods=["GET"])
def getVoice():
    if (request.values.get('id') == ""): return "error"
    else: VoiceId = int(request.values.get('id'))
    file_path, file_name = os.path.split(Voices[VoiceId])
    response = make_response(
        send_from_directory(file_path, file_name, as_attachment=True))
    for root, dirs, files in os.walk(tempDir):
        for f in files:
            if not ((tempDir + '/' + f) in Voices):
                os.remove(tempDir + '/' + f)
    Voices.pop(VoiceId)
    return response


if __name__ == '__main__':
    HZYS = huoZiYinShua("./settings.json")
    Voices = []
    if not (os.path.exists(tempDir)):
        os.makedirs(tempDir)
    app.run(host="127.0.0.1", port=1234)
