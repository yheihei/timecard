import datetime
from datetime import datetime as dt

JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")

def today() -> datetime.date:
    return dt.now(JST).today().date()

def now() -> datetime.datetime:
    return dt.now(JST)
