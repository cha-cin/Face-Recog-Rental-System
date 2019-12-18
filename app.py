#from flask import Flask
#from flask_socketio import SocketIO, send, emit
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from flask import request
from flask import render_template
import json
from datetime import datetime, timedelta
import pytz
tz = pytz.timezone('Asia/Taipei')

app = Flask(__name__)


socket = SocketIO(app)
authority = {}
face_Recog = False

@socket.on('face_recog')
def text(data):
    for i in data:
        face_Recog = i
        

def check_authority(authority):
    #return str(taiwan_now) + str(star_time)
    taiwan_now = datetime.now(tz)
    #clear the timezone
    taiwan_now = taiwan_now.replace(tzinfo=None)
    if len(authority)>=1:
        if taiwan_now - authority['end_time'] >= timedelta(seconds=2):
            return "ok! you can use it"
        else:
            return "someone use it"
    else:
        return "you don't have authority maybe you have to apply"

@app.route('/', methods=['GET', 'POST'])
def submit():
    star_time = ''
    end_time = ''
    global authority
    global face_Recog
    
    if request.method == 'POST':
        star_time = request.form.get('star_time')
        end_time = request.form.get('end_time')
        #convert str to datetime
        star_time = datetime.strptime(star_time, "%Y-%m-%dT%H:%M")
        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
        full_name = request.form.get('full_name')
        if face_Recog is True:
            authority['full_name'] = full_name
            authority['star_time'] = star_time
            authority['end_time'] = end_time
        else:
            authority = {}
        
        return check_authority(authority)
    elif request.method == 'GET':
        return render_template('apply form/index.html')
            
    
#get the static web path
@app.route('/<path:path>', methods=['GET'])
def static_files(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    socket.run(app, debug=True, host='140.115.87.73', port ='3000')