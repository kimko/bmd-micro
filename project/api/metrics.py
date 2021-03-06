# project/api/metrics.py
"""Helper functions to measure and log metrics.

Returns:
    timing -- Decorator to measure and log execution time
"""

from functools import wraps
from time import time

from flask import current_app as app


def timing(f):
    """I time the execution time of any function when used as a decorator and log to the flask application looker.

    Decorator function that utilizes functools.wraps to copy over all arguments of the passed function (f)
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        if app:
            app.logger.info(
                f"{args[0].__class__.__name__}.{f.__name__}() {round((end - start) * 1000, 2)}ms"
            )
        return result

    return wrapper
