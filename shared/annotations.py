from flask import request
from json import dumps
from functools import wraps

from utils.utils_date import datetime_handler

# if nbr_results_default is specified, we try to get nbr_results

def pagination(nbr_results_default=None):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                page_nbr = int(request.args.get('page_nbr'))

                if page_nbr == None or page_nbr == '':
                    page_nbr = 0
            except Exception as e:
                print(e)
                page_nbr = 0

            if nbr_results_default != None:
                try:
                    nbr_results = int(request.args.get('nbr_results'))

                    if nbr_results == None or nbr_results == '':
                        nbr_results = nbr_results_default
                except Exception as e:
                    print(e)
                    nbr_results = nbr_results_default

                kwargs["nbr_results"] = nbr_results

            kwargs["page_nbr"] = page_nbr

            return function(*args, **kwargs)

        wrapper.__name__ = function.__name__
        return wrapper

    return decorator

def to_json():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            res = function(*args, **kwargs)

            return dumps(res, default=datetime_handler)

        wrapper.__name__ = function.__name__
        return wrapper
    return decorator
