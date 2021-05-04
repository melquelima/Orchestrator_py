from app import app,socketio
from flask import request
from app.models.tables import Bot
from app.models.uteis import fields_required

@app.route('/pings/<id>')
def pings(id):
    socketio.emit("updateDashboard","asdasd")
    return "OK"
    ev = Event()
    result = "Offline"
    def ack(data):
        nonlocal result,ev
        result = "Online"
        ev.set()  # unblock HTTP route

    a = socketio.emit('ping',"", room=id, callback=ack)
    ev.wait(2)
    return result



@socketio.on('refreshDashboard')
def skt_refreshDash():
    bots = Bot.query.all()
    cadastrados = len(bots)
    online = len([ x for x in bots if x.is_online_time(60)])
    offline = len([ x for x in bots if not x.is_online_time(60)])

    data = {"cadastrados":cadastrados,"online":online,"offline":offline}
    print(data)
    socketio.emit("refreshDashboard",data)

@socketio.on('forceRefreshDashBoard')
def skt_forceRefreshDash():
    skt_refreshDash()


@socketio.on('message')
def handleMessage(msg):
    print("asdasdasd")
    open("reqId.txt","w",True).write(request.sid)
    send(msg,broadcast=True)

@socketio.on('online')
def cnt(data):
    a = request.sid
    #users.append(a)
    print("asdasdas")