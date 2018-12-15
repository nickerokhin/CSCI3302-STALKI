import sys
sys.path.append('./flight/')
sys.path.append('./web/')

from multiprocessing import Process, Queue
from flight.fly_drone import *



if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()
