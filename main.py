import sys
sys.path.append('./flight/')
sys.path.append('./web/')

from multiprocessing import Process, Queue
from flight.fly_drone import *
from www.server import *

if __name__ == '__main__':
    q = Queue()
	web = Process(target=run_server, args=(q,))
	drone = Process(target=start_flight, args=(q,))
    web.start()
	drone.start()
