from app import db,Telbot
from app.models.timenow import now
from flask import render_template,request
from app.models.tables import Bot,Type,Log
from sqlalchemy import desc,or_
from functools import wraps
from datetime import datetime as dt
from sqlalchemy.inspection import inspect
import json

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
    if type(bt) == str or type(bt) == int :
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
        en = cls.query.filter(_field).order_by(order).first()

    return en,"OK" if en else "couldn't find '{}' value at '{}' column".format(value,field)

def retContent(value,jsn,error=False):
    xstr = lambda s: s or ""
    contentJson = "json" in xstr(request.headers.get("Content-Type"))
    return jsn if contentJson else render_template("grafana1.html",value=value,color=error)

def fields_required(lista,methods="*",out="fields"):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            xstr = lambda s: s or ""
            contentJson = "json" in xstr(request.headers.get("Content-Type"))

            if methods == "*" or request.method in methods:
                if request.method == "GET":
                    fields = request.args.to_dict()
                elif request.method in ["POST","PUT","DELETE","DEL","CREDIT"]:
                    data = request.get_json(force=True) or request.get_json() or request.form.to_dict()
                    fields =  request.json if contentJson else data
                
                lista2 = lista if isinstance(lista,list) else list(lista.keys())

                notfound = [x for x in lista2 if not x in fields]
                if notfound:
                    return "campos nao encontrados!:\n\t" + "\n\t".join(notfound),400
                
                if isinstance(lista,dict):
                    for k,v in lista.items():
                        
                        if v == float and isinstance(fields[k],int):
                            fields[k] = float(fields[k])

                        if not isinstance(fields[k],v):
                            tipo = str(v).split("'")[1]
                            return f"o campo '{k}' nao corresponde ao tipo ({tipo})",400


                kwargs[out] = fields
                result = function(*args, **kwargs)
                return result
            else:
                kwargs[out] = []
                return function(*args, **kwargs)

        return wrapper
    return decorator

def mallowList(schema,lista):#coverte dados da api para formtado jdson
    sc = schema()
    return [json.loads(sc.dumps(x)) for x in lista if sc.dumps(x) != '{}']

def Datevalidate(date_text,formt): #valida formato de data
    try:
        dt.strptime(date_text, formt)
        return True,dt.strptime(date_text,formt)
    except ValueError:
        return  False,""

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