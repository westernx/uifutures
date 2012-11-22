import time
import random

from uifutures import Executor
from uifutures.worker import set_progress, notify


icons = [
    'add',
    'delete',
    'edit',
    'error',
    'go',
    'link',
]
icons = ['/home/mboers/Documents/icons/fatcow/32x32/brick_%s.png' % x for x in icons]


def worker():
    for i in xrange(5):
        for j in xrange(10):
            time.sleep(0.01 + 0.1 * random.random())
            set_progress(i * 10 + j + 1, maximum=50, status='Working...')
    notify(message='Sleeping is complete.')


if __name__ == '__main__':
    
    import uifutures.examples.sleep
    
    executor = Executor()
    for i in range(5):
        future = executor.submit_ext(uifutures.examples.sleep.worker, name='Sleeper', icon=random.choice(icons))
    res = future.result()
    
