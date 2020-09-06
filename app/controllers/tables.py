from app import app,db
from app.models.tables import Bot,BotSchema,Enviorment,EnvSchema2
from flask import request
import json


@app.route('/api/tbl_bots')
def bots():
    sc = BotSchema()
    id = request.args.get('id')
    if id is None:
        bt = Bot.query.all()
    else:
        bt = [Bot.query.get(str(id))]
    return {"bots":[json.loads(sc.dumps(x)) for x in bt if sc.dumps(x) != '{}']}

@app.route('/api/tbl_env')
def env():
    sc = EnvSchema2()
    id = request.args.get('id')
    if id is None:
        en = Enviorment.query.all()
    else:
        bt = [Bot.query.get(str(id))]
    return {"enviorments":[json.loads(sc.dumps(x)) for x in en if sc.dumps(x) != '{}']}

@app.route('/api/tbl_status')
def status():
    sc = StatusSchema()
    id = request.args.get('id')
    if id is None:
        en = Status.query.all()
    else:
        en = [Status.query.get(str(id))]
    return {"Status":[json.loads(sc.dumps(x)) for x in en if sc.dumps(x) != '{}']}
