import select
import _multiprocessing
import pprint
import sys
import os
import cPickle as pickle

from .utils import debug
        # 
        # try:
        #     res = func(*args, **kwargs)
        # except Exception as e:
        #     debug('Host: exception: %r', e)
        #     conn.send(dict(
        #         type='exception',
        #         uuid=uuid,
        #         exception=e,
        #     ))
        # else:
        #     debug('Host: result: %r', res)
        #     conn.send(dict(
        #         type='result',
        #         uuid=uuid,
        #         result=res
        #     ))
        # 



def main():
    
    # Connect to the executor, and start the listener.
    fd = int(sys.argv[1])
    conn = _multiprocessing.Connection(fd)
    conn.send(dict(
        type='handshake',
        pid=os.getpid(),
    ))
    
    try:
        process(conn)
    except Exception as e:
        conn.send(dict(
            type='exception',
            package=pickle.dumps(dict(
                exception=e,
            ), protocol=-1),
        ))

def process(conn):
    
    # Get the message.
    rlist, _, _ = select.select([conn], [], [])
    msg = conn.recv()
    debug('Worker: recieved message\n%s', pprint.pformat(msg))
    
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
