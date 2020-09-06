from app import db,ma
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Time,Boolean
from marshmallow import Schema, fields, pprint
from datetime import datetime,date,timedelta
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

class Users(db.Model):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    userName = Column(String,unique=True)
    password = Column(String)

    def __init__(self,userName,password):
        self.userName = userName
        self.password = password
    
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name != "_sa_instance_state":
            db.session.commit()

    def __repr__(self):
        return "<User %r>" % self.userName

    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

class Bot(db.Model):
    __tablename__ = "bot"

    id = Column(Integer,primary_key=True)
    botName =   Column(String)
    id_Env =    Column(Integer,ForeignKey('Enviorment.id'))
    envName =   db.relationship("Enviorment",foreign_keys=id_Env)
    ping =      Column(DateTime)
    working =   Column(DateTime)
    pingTimeout =   Column(Time,nullable=False)
    workingTimeout =   Column(Time)
    idChat =    Column(String)
    flagOff=    Column(Boolean,default=False)
    #roles = db.relationship("Status", backref="bot", lazy="dynamic",secondary = "status")
    
    def __init__(self,botName,id_Env,ping,working,pingTimeout,workingTimeout,flagOff=False):
        self.botName = botName
        self.id_Env = id_Env
        self.ping = ping
        self.working = working
        self.pingTimeout = pingTimeout
        self.workingTimeout = workingTimeout
        self.flagOff = flagOff

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name != "_sa_instance_state":
            db.session.commit()

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
        tempo=    (now()-png).seconds
        tmout=  datetime.combine(date.min,timeout) - datetime.min #convert to timedelta
        pingsts = tempo < tmout.seconds + time
        return pingsts

    def __repr__(self):
        return "<Bot %r>" % self.envName

class Type(db.Model):
    __tablename__ = "type"

    id = Column(Integer,primary_key=True)
    description = Column(String,unique=True)

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


class UserSchema(ma.ModelSchema):
    class Meta:
        model = Users

class EnvSchema(ma.ModelSchema):
    class Meta:
        model = Enviorment
    envName = fields.String(data_key="Name")

class BotSchema(ma.Schema):
    id = fields.Integer()
    botName = fields.String()
    #id_Env = fields.Integer()
    #envName = fields.Nested(EnvSchema)
    envName = fields.Nested(EnvSchema,data_key="Env") #fields.Nested(EnvSchema,only=["envName","id"])
    ping =    fields.Time()
    timeout = fields.Time()
    working = fields.String()
    flagOff = fields.Boolean()
    

class EnvSchema2(ma.ModelSchema):
    envName = fields.String(data_key="Name")
    bot = fields.Nested(BotSchema)
