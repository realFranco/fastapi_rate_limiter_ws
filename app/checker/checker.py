"""
This module will check if the "id" from /car websocket endpoints
is already inserted or not.

Will act as a wrapper
"""
import time
import functools
from globalData.data import connList


def is_allowed_to_connect(weboscket_data: dict, decorator_data: dict) -> bool:
    """
    :param weboscket_data {id, weboscket} or any other parameter on the endpoint

    :param decorator_data: dict {limit, rate}
        - key limit: is the limit of connections allowed by the configuration in a window time.
        - key rate: is the expiracy time. Example, 5s means that the rule will expire in 5 seconds
            so, in 5 seconds you could accept "limit" more connections.
    """
    try:
        # weboscket_data: {'id': 'franco', 'websocket': <starlette.websockets.WebSocket object at 0x7f30e6c454c0>}
        # decorator_data: {'limit': 7}

        by, gap = 1, 60
        if 'rate' in decorator_data:
            # minutes
            if 'm' in decorator_data['rate']:
                by = 60
            # hours
            if 'h' in decorator_data['rate']:
                by = 3600
            gap = int(decorator_data['rate'][:-1]) * by
        print(f'gap: {gap}')

        dict_index = weboscket_data['id']
        if weboscket_data['id'] not in connList.conn or \
            connList.conn[dict_index]['resetAt'] < int(time.time()):
            # The second condition is the Expiration scenario
            # If the resetAt is expired, the limit it's gone
            connList.conn[dict_index] = { 'try': 1, 'resetAt': int(time.time()) + gap }
            return True

        if connList.conn[dict_index]['try'] < decorator_data['limit']:
            connList.conn[dict_index] += 1
            return True

        print(f'User id: "{dict_index}" has a lot of conns detected!')
        return False

    except Exception as err:
        print(f'[ERROR] {str(err)}')
        return False


def limit_conn(*args_or_func, **decorator_kwargs):

    def _decorator(func):
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            out = is_allowed_to_connect(kwargs, decorator_kwargs)
            

            # Post logic to close the connection
            if not out:
                kwargs['id'] = ''

            return func(*args, **kwargs) if not out else func(*args, **kwargs)

        return wrapper

    return _decorator(args_or_func[0]) \
        if args_or_func and callable(args_or_func[0]) else _decorator
