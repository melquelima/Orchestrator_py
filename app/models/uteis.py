from app import db,Telbot
from app.models.timenow import now
from flask import render_template,request
from app.models.tables import Bot,Type,Log
from sqlalchemy import desc,or_
from functools import wraps
from sqlalchemy.inspection import inspect

def post_id_validation(req,cls,field=None,order=None):
    id = req.form.get("id")
    xstr = lambda s: s or ""

    if id is None:return (False,("id must be sent!",500))

    if field is None:
        en = cls.query.get(str(id))
    else:
        field = getattr(cls,field).like("%{}%".format(str(id)))
        en = cls.query.filter(field).order_by(order).all()
    
    if en: return True,en

    return (False,("id not found!",500))

def get_id_validation(req,cls,field=None,order=None):
    id = req.args.get("id")
    xstr = lambda s: s or ""
    content = xstr(req.headers.get("Content-Type"))

    if id is None:return (False,("id must be sent!",500) if "json" in content else render_template("grafana1.html",value="id must be sent!",color=False))

    if field is None:
        en = cls.query.get(str(id))
    else:
        field = getattr(cls,field).like("%{}%".format(str(id)))
        en = cls.query.filter(field).order_by(order).all()
    
    if en: return True,en,content

    return (False,("id not found!",500) if "json" in content else render_template("grafana1.html",value="id not found!",color=False))

def addLog(bt,tp,exception):
    #bt migth be "1" or bot Object
    if type(bt) == str:
        bt = Bot.query.get(bt)
        if not bt: return False, f"bot '{bt}' not found!"

    #find log that corresponds to tp, it migth be type_id "4"(offline) or description "offline"
    idLog = Type.query.filter(or_(Type.description==tp,Type.id==tp)).first()
    if not idLog:
        return False,f"type_id {tp} not found!"

    #get last log uploaded for the same bot
    lastlog = Log.query.filter_by(id_bot=bt.id).order_by(desc(Log.datetime)).first()

    if idLog.description == 'offline' and lastlog and lastlog.type_id == idLog.id and not lastlog.backAt:
        return True,"OK"

    #if log im uploading is the same of the last log updated, just add 1 to recurrence column
    if lastlog and lastlog.type_id == idLog.id and lastlog.exception == exception and lastlog.type_id != 4:
        lastlog.recurrence +=1
        lastlog.datetime = now()
    else:
        bt.flagOff = idLog.description == 'offline'
        lg = Log(bt.id,idLog.id,exception,now(),bt.ping,1,None)
        db.session.add(lg)
        db.session.commit()
        
    header = "<b>===={}====</b>\n".format(bt.botName)
    msg = header + exception
    if bt.idChat: Telbot.sendMessage(bt.idChat,msg,parse_mode='HTML')
    return True,"OK"

def validate_field2(cls,value,like=None,field=None,order=None):
    #xstr = lambda s: s or ""
    #contentJson = "json" in xstr(request.headers.get("Content-Type"))

    if field is None:
        en = cls.query.get(str(value))
        field = inspect(cls).primary_key[0].name
    else:
        value = value if not like else like.format(value)
        _field = getattr(cls,field).like(value)
        en = cls.query.filter(_field).order_by(order).all()

    return en,"OK" if en else "couldn't find '{}' value at '{}' column".format(value,field)

def retContent(value,jsn,error=False):
    xstr = lambda s: s or ""
    contentJson = "json" in xstr(request.headers.get("Content-Type"))
    return jsn if contentJson else render_template("grafana1.html",value=value,color=error)

#decorator
def fields_required(lista):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            xstr = lambda s: s or ""
            contentJson = "json" in xstr(request.headers.get("Content-Type"))

            if request.method == "GET":
                fields = request.args.to_dict()
            elif request.method == "POST":
                fields =  request.json if contentJson else request.form.to_dict()
            
            notfound = [x for x in lista if not x in fields]
            if notfound:
                return "couldn't find these fields:\n\t" + "\n\t".join(notfound)

            result = function(fields=fields,*args, **kwargs)
            return result
        return wrapper
    return decorator



def validate_field(cls,value,like=None,field=None,order=None,fixedjson=None,errorMsg=None):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            _value = kwargs['fields'][value]
            if field is None:
                en = cls.query.get(str(_value))
                fieldName = inspect(cls).primary_key[0].name
            else:
                _value = _value if not like else like.format(_value)
                _field = getattr(cls,field).like(_value)
                en = cls.query.filter(_field).order_by(order).all()
                fieldName = field

            falseValue = errorMsg if errorMsg else "couldn't find '{}' value at '{}' column".format(_value,fieldName)

            if not en: return falseValue if fixedjson else retContent(falseValue,falseValue,False)
            return function(en,*args, **kwargs)
        return wrapper
    return decorator

def ping_validation(*args, **kwargs):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg,Bot):
                    if not arg.ping:
                        return retContent("No ping detected!","No ping detected!",False)
            return function(*args, **kwargs)
        return wrapper
    return decorator