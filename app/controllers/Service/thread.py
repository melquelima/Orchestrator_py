from threading import Thread
from app import db,Telbot
from app.models.uteis import addLog
from app.models.tables import Type,Log,Bot
from datetime import datetime,date,timedelta
from app.models.timenow import now
from app.controllers.Service.socket import skt_refreshDash
import time
from sqlalchemy import desc
from apscheduler.scheduler import Scheduler
import atexit

#t = AppContextThread(target=logStatus)
#t.start()

#Thread(target=logStatus).start()
cron = Scheduler(daemon=True,max_instances=10)
# Explicitly kick off the background thread
cron.start()

#flagOff
 #    1 estava offline
 #    0 estava online

def onceWhenOnline(**args):
    bot = args["bot"]
    lg = Log.query.filter_by(id_bot=bot.id,type_id=4).order_by(desc(Log.datetime)).first()
    if lg:lg.backAt = now()
    if bot.idChat: 
        header = f"<b>===={bot.botName}====</b>\n"
        Telbot.sendMessage(bot.idChat,header + "Is online!",parse_mode='HTML')
    skt_refreshDash()

def onceWhenOffline(**args):
    bot = args["bot"]
    addLog(bot,"offline",f'Bot "{bot.botName}" offline')


    if bot.idChat: 
        header = f"<b>===={bot.botName}====</b>\n"
        Telbot.sendMessage(bot.idChat,header + "Is offline!",parse_mode='HTML')
    skt_refreshDash()


#@cron.interval_schedule(seconds=5)
def logStatus():
    sts = Bot.query.filter(Bot.ping.isnot(None)).all()

    for en in sts: # for each bot
        # if not en.ping: continue #en.ping must not be Null

        en.onceWhenOnline(60,onceWhenOnline,{"bot":en})
        en.onceWhenOffline(60,onceWhenOffline,{"bot":en})
        # continue

        # sts = en.is_online_time(60) #se esta online com margem de erro de 60 segundos

        # if not sts:   #esta offline
        #     if not en.flagOff: #estava online
        #         addLog(en,"offline",f'Bot "{en.botName}" offline')
        #         en.flagOff = True
        #         en.save()
        # else:
        #     if en.flagOff: # verifica se estava offline
        #         en.flagOff = False
        #         lg = Log.query.filter_by(id_bot=en.id,type_id=4).order_by(desc(Log.datetime)).first()
        #         if lg:lg.backAt = now()
        #         if en.idChat: Telbot.sendMessage(en.idChat,f'Bot "{en.botName}" online!')
            


# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))
