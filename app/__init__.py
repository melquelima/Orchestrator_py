from flask import Flask
from flask_cors import CORS, cross_origin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO,send,emit
import telepot as tp
import os

app = Flask(__name__)
cors = CORS(app)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.needs_refresh_message = (u"Session timedout, please re-login")
socketio = SocketIO(app,ping_timeout=5, ping_interval=2)

ma = Marshmallow(app)
adjustTime = False,3
Telbot = tp.Bot("1238447435:AAGufd338Uwk7Muub6r7-NeF_jjAULwi3Fs")
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    print("-----------------------------")
    #Telbot.message_loop(lambda msg:Telbot.sendMessage(msg["chat"]["id"],"<b>your chat id is:</b> %r" %msg['chat']['id'],parse_mode='HTML'))
#Telbot.message_loop(lambda msg:msg)
#self.bot.message_loop(self.ChatBotConfig)

from app.models.filters.filters import *
from app.models.filters.contexts import *
from app.models.filters.inject import *
from app.controllers.Api import api,tables
from app.controllers.Routes import login,default,robos,notepads
from app.controllers.Service import thread,socket
#from app.controllers.Service.socket import *



