import logging
import requests
from contextlib import contextmanager
import urllib
import json

__all__ = ['get', 'post', 'delete', 'put']


@contextmanager
def send(method, url, data, headers, status_code, parsejson):
    response_obj = ()
    if '://' not in url:
        url = 'http://' + url
    try:
        ret = None
        fn = getattr(requests, method)
        if method in ('get', 'delete'):
            if data:
                url += '?' + urllib.parse.urlencode(data)
            ret = fn(url, headers=headers, timeout=3)
        else:
            ret = fn(url, data=data, headers=headers, timeout=3)
        ret.encoding = 'utf-8'
        assert ret.status_code == status_code, 'status_code: {}\ntext: {}\n'.format(ret.status_code, ret.text)
        if parsejson:
            response_obj = ret.json()
        else:
            response_obj = ret.text
        yield response_obj
    except Exception as e:
        logging.fatal('req-url: %s\n' % url)
        logging.fatal('req-data: %s\n' % json.dumps(data))
        logging.fatal('req-headers: %s\n' % json.dumps(headers))
        if ret is not None:
            logging.fatal('text:\n' + ret.text + '\n')
        if response_obj != ():
            logging.fatal(response_obj)
        raise


def get(url, data={}, headers={}, status_code=200, parsejson=True):
    return send('get', url, data, headers, status_code, parsejson)


def post(url, data={}, headers={}, status_code=200, parsejson=True):
    return send('post', url, data, headers, status_code, parsejson)


def delete(url, data={}, headers={}, status_code=200, parsejson=True):
    return send('delete', url, data, headers, status_code, parsejson)


def put(url, data={}, headers={}, status_code=200, parsejson=True):
    return send('put', url, data, headers, status_code, parsejson)

