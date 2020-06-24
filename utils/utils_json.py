import datetime

def default_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    
    raise TypeError("Unknown type")