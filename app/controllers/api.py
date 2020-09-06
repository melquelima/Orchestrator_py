from app import app,db
import json
from flask import jsonify,request,redirect,url_for,render_template
from datetime import datetime,timedelta
from app.models.uteis import get_id_validation,post_id_validation,addLog,fields_required,validate_field,retContent,ping_validation
from app.models.timenow import now
from app.models.tables import Bot,Log,Type,Proc
from sqlalchemy import desc

from threading import Thread
import time

@app.route('/api/response')
@fields_required(['id'])
@validate_field(Bot,'id')
@ping_validation()
def response(item,fields):
    status = item.is_online
    text=   "Online" if status else "Offline"
    dt =    item.ping.strftime("%Y-%m-%d %H:%M:%S")
    time =  item.pingTimeout.strftime("%H:%M:%S")
    json=   {"Online":status,"LastPing":dt,"Timeout":time}

    return retContent(text,json,status)
   
@app.route('/api/lastPing') #Grafana
@fields_required(['id'])
@validate_field(Bot,'id')
@ping_validation()
def lastPing(item,fields):
    dt =    item.ping.strftime("%d-%m %H:%M:%S")#f"{item.ping:%Y-%m-%d %H:%M:%S}"
    time =  item.pingTimeout.strftime("%H:%M:%S")
    json=   {"Online":item.is_online,"LastPing":dt,"Timeout":time}
    return retContent(dt,json,item.is_online)
    
@app.route('/api/ping', methods=['POST'])
@fields_required(['id'])
@validate_field(Bot,'id')
def ping(item,fields):    
    item.ping = now()
    return {"Response":"OK"}

@app.route('/api/logs')
@fields_required(['id'])
@validate_field(Log,'id',field='id_bot',order=desc(Log.datetime),errorMsg="No logs found!")
def logs(item,fields):
    return render_template("table.html",lista=item)


@app.route('/api/responseLog', methods=['POST'])
@fields_required(['id','type_id','exception'])
@validate_field(Bot,'id',fixedjson=True)
@ping_validation()
def responseLog(item,fields):
    lg = addLog(fields["id"],fields["type_id"],fields["exception"])
    if not lg[0]: return lg[1]
    return "OK"

@app.route('/api/process', methods=['POST'])
@fields_required(['id','type','obs1','obs2'])
@validate_field(Bot,'id',fixedjson=True)
@validate_field(Type,'type',fixedjson=True)
@ping_validation()
def process(t_item,b_item,fields):
    db.session.add(Proc(b_item.id,t_item.id,now(),fields["obs1"],fields["obs2"]))
    db.session.commit()
    return "OK"

@app.route('/api/countProcess') #Grafana
@fields_required(['type'])
@validate_field(Bot,'id',fixedjson=True)
def countProcess(item,fields):
    lst = Proc.query.filter_by(id_bot = item.id,type=fields["type"]).all()
    html=   render_template("grafana1.html",value=len(lst),color=True)
    json=   {"Qtd":len(lst)}
    return retContent(len(lst),json,True)