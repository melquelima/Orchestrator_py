from threading import Thread
from app import db,Telbot
from app.models.uteis import addLog
from app.models.tables import Type,Log,Bot
from datetime import datetime,date,timedelta
from app.models.timenow import now
import time
from sqlalchemy import desc
from apscheduler.scheduler import Scheduler
import atexit
#t = AppContextThread(target=logStatus)
#t.start()

#Thread(target=logStatus).start()
cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()

@cron.interval_schedule(seconds=5)
def logStatus():
    sts = Bot.query.all()

    for en in sts: # for each bot
        if not en.ping: continue #en.ping must not be Null

        sts = en.is_online_time(60)
        if not sts:
            addLog(en,"offline",f'Bot "{en.botName}" offline')
        else:
            if en.flagOff: # verifica se estava offline
                en.flagOff = False
                lg = Log.query.filter_by(id_bot=en.id,type_id=4).order_by(desc(Log.datetime)).first()
                if lg:lg.backAt = now()
                if en.idChat: Telbot.sendMessage(en.idChat,f'Bot "{en.botName}" online!')
            



# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))
