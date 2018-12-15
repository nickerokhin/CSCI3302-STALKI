import sys
sys.path.append('./flight')
sys.path.append('./web')

from multiprocessing import Process, Queue
from flight import start_flight



if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()
