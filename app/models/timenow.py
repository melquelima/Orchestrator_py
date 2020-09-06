from app import adjustTime
from datetime import datetime,timedelta

def now():
    return datetime.now() - timedelta(hours=adjustTime[1] if adjustTime[0] else 0)