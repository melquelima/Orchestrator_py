from app import app,db
from app.models.tables import Bot,BotSchema,Enviorment,EnvSchema2,EnvSchema,Notepad,NotepadSchema
from app.models.uteis import mallowList,fields_required,Datevalidate
from flask import request,jsonify
from datetime import datetime as dt,timedelta
import json


@app.route('/api/tbl_bots')
@app.route('/api/tbl_bots/<int:id>')
def bots(id=None):
    if not id:
        bt = Bot.query.all()
    else:
        bt = [Bot.query.get(id)]

    return jsonify(mallowList(BotSchema,bt))

@app.route('/api/tbl_bots',methods=['PUT'])
@fields_required({"id":int,"botName":str,"id_Env":int,"descricao":str,"idChat":int,"pingMinutesTimeout":int})
def botUpdate(fields):
    if fields["botName"] == "": return "O campo 'nome' não pode estar em branco",400

    #timeout = Datevalidate(fields["pingTimeout"],"%H:%m:%S")
    #if (not timeout[0]) and fields["pingTimeout"] != "": return "o campo 'timeout' contem um formato inválido",400
    pingMinutesTimeout = (dt.min + timedelta(minutes=fields["pingMinutesTimeout"])).time()
    fields["idChat"] = None if not fields["idChat"] else fields["idChat"]

    bot = Bot.query.get(fields["id"])
    if bot:
        env = Enviorment.query.get(fields["id_Env"])
        if env:
            bot.botName = fields["botName"]
            bot.id_Env = env.id
            bot.idChat = fields["idChat"]
            bot.descricao = fields["descricao"]
            bot.pingTimeout = pingMinutesTimeout
            bot.save()
            return "OK"
        else:
            return "Ambiente não encontrado!",400
    else:
        return "Bot não existente!",400

@app.route('/api/tbl_bots',methods=['POST'])
@fields_required({"botName":str,"id_Env":int,"descricao":str,"idChat":int,"pingMinutesTimeout":int})
def botAdd(fields):
    if fields["botName"] == "": return "O campo 'nome' não pode estar em branco",400

    #timeout = Datevalidate(fields["pingTimeout"],"%H:%m:%S")
    #if (not timeout[0]) and fields["pingTimeout"] != "": return "o campo 'timeout' contem um formato inválido",400
    pingMinutesTimeout = (dt.min + timedelta(minutes=fields["pingMinutesTimeout"])).time()


    bot = Bot.query.filter_by(botName=fields["botName"]).first()
    if not bot:
        env = Enviorment.query.get(fields["id_Env"])
        if env:
            bot = Bot(fields["botName"],fields["id_Env"],None,None,pingMinutesTimeout,None,fields["idChat"])
            bot.save()
            return "OK"
        else:
            return "Ambiente não encontrado!",400
    else:
        return "Bot ja existente!",400


@app.route('/api/tbl_notepads')
@app.route('/api/tbl_notepads/<int:id>')
def notepadsApi(id=None):
    if not id:
        bt = Notepad.query.all()
    else:
        bt = [Notepad.query.get(id)]

    return jsonify(mallowList(NotepadSchema,bt))


@app.route('/api/tbl_env')
@app.route('/api/tbl_env/<int:id>')
def env(id=None):
    if not id:
        bt = Enviorment.query.all()
    else:
        bt = [Enviorment.query.get(id)]

    return jsonify(mallowList(EnvSchema,bt))

