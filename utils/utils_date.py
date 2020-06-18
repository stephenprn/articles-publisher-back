import datetime

def get_current_date():
    return datetime.datetime.now()


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    
    raise TypeError("Unknown type")