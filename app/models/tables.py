from app import db,ma
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Time,Boolean
from marshmallow import Schema, fields, pprint
from datetime import datetime,date,timedelta
from flask_login import UserMixin
from app.models.timenow import now

class Enviorment(db.Model):
    __tablename__ = "Enviorment"

    id = Column(Integer,primary_key=True)
    envName = Column(String)

    def __init__(self,envName):
        self.envName = envName

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name != "_sa_instance_state":
            db.session.commit()
    def __repr__(self):
        return "<Env %r>" % self.envName
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.rollback()
        db.session.delete(self)
        db.session.commit()


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    userName = Column(String(50),unique=True)
    password = Column(String(500))
    admin = Column(Boolean)

    def __init__(self,userName,password):
        self.userName = userName
        self.password = password

    @property
    def is_admin(self):
        return self.admin

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name != "_sa_instance_state":
            db.session.commit()

    def __repr__(self):
        return "<User %r>" % self.userName
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.rollback()
        db.session.delete(self)
        db.session.commit()    

class Bot(db.Model):
    __tablename__ = "bot"

    id = Column(Integer,primary_key=True)
    botName =   Column(String(50),unique=True)
    id_Env =    Column(Integer,ForeignKey('Enviorment.id'))
    envName =   db.relationship("Enviorment",foreign_keys=id_Env)
    ping =      Column(DateTime)
    working =   Column(DateTime)
    pingTimeout =   Column(Time,nullable=False)
    workingTimeout =   Column(Time)
    idChat =    Column(String)
    flagOff=    Column(Boolean,default=False)
    descricao = Column(String)
    token = Column(String)
    #roles = db.relationship("Status", backref="bot", lazy="dynamic",secondary = "status")
    
    def __init__(self,botName,id_Env,ping,working,pingTimeout,workingTimeout,idChat,token=None,flagOff=False):
        self.botName = botName
        self.id_Env = id_Env
        self.ping = ping
        self.working = working
        self.pingTimeout = pingTimeout
        self.workingTimeout = workingTimeout
        self.flagOff = flagOff
        self.idChat = idChat

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.rollback()
        db.session.delete(self)
        db.session.commit()

    def pingMinutesTimeout(self):
        return (self.pingTimeout.hour * 60) + self.pingTimeout.minute

    @property
    def is_online(self):
        return self.check(0)
    
    def is_online_time(self,time):
        return self.check(time)

    def check(self,time = 0):
        if self.ping is None: return False
        ping = (self.ping,self.pingTimeout)
        wkng = (self.working,self.workingTimeout)

        if self.working is None:
            png,timeout = ping
        else:
            if self.ping > self.working:
                print("----")
                png,timeout = ping
                self.working = None
                #db.session.commit()
            else:
                png,timeout = wkng

        tempo=    (now()-png).days*86400 + (now()-png).seconds #tempo desde o ultimo ping
        tmout=  datetime.combine(date.min,timeout) - datetime.min #convert to timedelta
        pingsts = tempo < tmout.seconds + time

        return pingsts

    #executa quando o status muda de offline para online
    def onceWhenOnline(self,time,func,args={}):
        sts = self.is_online_time(time)
        if self.flagOff and sts:
            func(**args)
            self.flagOff = False
            self.save()

    #executa quando o status muda de online para offline
    def onceWhenOffline(self,time,func,args={}):
        sts = self.is_online_time(time)
        if not self.flagOff and not sts:
            func(**args)
            self.flagOff = True
            self.save()


    def __repr__(self):
        return "<Bot %r>" % self.envName

class Type(db.Model):
    __tablename__ = "type"

    id = Column(Integer,primary_key=True)
    description = Column(String(5000),unique=True)

    def __init__(self,description):
        self.description = description
    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name != "_sa_instance_state":
            db.session.commit()

    def __repr__(self):
        return "<Type %r>" % self.userName

class Log(db.Model):
    __tablename__ = "log"

    id = Column(Integer,primary_key=True)
    id_bot = Column(Integer,ForeignKey('bot.id'))
    type_id = Column(Integer,ForeignKey('type.id'))
    exception = Column(String)
    lastPing = Column(DateTime)
    datetime = Column(DateTime)
    recurrence = Column(Integer)
    description = db.relationship("Type",foreign_keys=type_id)
    botName = db.relationship("Bot",foreign_keys=id_bot)
    backAt = Column(DateTime)

    def __init__(self,id_bot,type_id,exception,datetime,lastPing,recurrence,backAt):
        self.id_bot = id_bot
        self.type_id = type_id
        self.exception = exception
        self.datetime = datetime
        self.lastPing = lastPing
        self.recurrence = recurrence
        self.backAt = backAt
    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name != "_sa_instance_state":
            db.session.commit()

    def __repr__(self):
        return "<Log %r>" % self.id_bot

class Proc(db.Model):
    __tablename__ = "process"

    id = Column(Integer,primary_key=True)
    id_bot = Column(Integer,ForeignKey('bot.id'))
    type = Column(Integer,ForeignKey('type.id'))
    datetime = Column(DateTime)
    obs1 = Column(String)
    obs2 = Column(String)
    botName = db.relationship("Bot",foreign_keys=id_bot)
    description = db.relationship("Type",foreign_keys=type, lazy='subquery')

    def __init__(self,id_bot,type,datetime,obs1,obs2):
        self.type = type
        self.datetime = datetime
        self.id_bot = id_bot
        self.obs1 = obs1
        self.obs2 = obs2
    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name != "_sa_instance_state":
            db.session.commit()

    def __repr__(self):
        return "<Proc %r>" % self.id

class Notepad(db.Model):
    __tablename__ = "notepad"

    id = Column(Integer,primary_key=True)
    id_bot = Column(Integer,ForeignKey('bot.id'))
    name =   Column(String(50),unique=True,nullable=False)
    text =  Column(String)
    bot = db.relationship("Bot",foreign_keys=id_bot)
    
    def __init__(self,id_bot,name,text):
        self.id_bot = id_bot
        self.name = name
        self.text = text

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.rollback()
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<NotePad %r>" % self.envName




class UserSchema(ma.ModelSchema):
    class Meta:
        model = Users

class EnvSchema(ma.ModelSchema):
    id = fields.Integer()
    envName = fields.String(data_key="Name")

class BotSchema(ma.Schema):
    id = fields.Integer()
    idChat = fields.Integer()
    botName = fields.String()
    #id_Env = fields.Integer()
    #envName = fields.Nested(EnvSchema)
    envName = fields.Nested(EnvSchema,data_key="Env") #fields.Nested(EnvSchema,only=["envName","id"])
    ping =    fields.DateTime(format='%d/%m/%y %H:%M')
    pingTimeout = fields.Time()
    pingMinutesTimeout = fields.Function(lambda obj:obj.pingMinutesTimeout())
    working = fields.String()
    descricao = fields.String()
    flagOff = fields.Boolean()
    #token = fields.String()

    

class EnvSchema2(ma.ModelSchema):
    envName = fields.String(data_key="Name")
    bot = fields.Nested(BotSchema)

class NotepadSchema(ma.ModelSchema):
    id = fields.Integer()
    bot = fields.Nested(BotSchema)
    name = fields.String()
    text = fields.String()