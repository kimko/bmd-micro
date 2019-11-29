# project/api/metrics.py


from functools import wraps
from time import time

from flask import current_app as app


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        app.logger.info(
            f"{args[0].__class__.__name__}.{f.__name__}() {round((end - start) * 1000, 2)}ms"
        )
        return result

    return wrapper
