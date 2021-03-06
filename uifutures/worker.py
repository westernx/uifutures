import select
import _multiprocessing
import sys
import os
import cPickle as pickle
import traceback


_conn = None
_job = {}


def notify(message, **kwargs):
    if _conn:
        kwargs['type'] = 'notify'
        kwargs['message'] = message
        _conn.send(kwargs)


def set_progress(value=None, maximum=None, status=None):
    if _conn is not None:
        _conn.send(dict(
            type='progress',
            value=value,
            maximum=maximum,
            status=status,
        ))

def set_thumbnail(path):
    if _conn is not None:
        _conn.send(dict(
            type='thumbnail',
            path=path,
        ))

def main():
    
    global _conn
    
    # Connect to the executor, and start the listener.
    fd = int(sys.argv[1])
    _conn = conn = _multiprocessing.Connection(fd)
    conn.send(dict(
        type='handshake',
        pid=os.getpid(),
    ))
    
    try:
        process(conn)
    except Exception as e:
        conn.send(dict(
            type='exception',
            exception_name=type(e).__name__,
            exception_message=str(e),
            exception_traceback=traceback.format_exc(),
            package=pickle.dumps(dict(
                exception=e,
            ), protocol=-1),
        ))

def process(conn):
    
    global _job
    
    # Get the message.
    rlist, _, _ = select.select([conn], [], [])
    _job = msg = conn.recv()
    # debug('Worker: recieved message\n%s', pprint.pformat(msg))
    
    package = pickle.loads(msg['package'])
    res = package['func'](*package['args'], **package['kwargs'])
    conn.send(dict(
        type='result',
        package=pickle.dumps(dict(
            result=res
        ), protocol=-1),
    ))
    

if __name__ == '__main__':
    main()
