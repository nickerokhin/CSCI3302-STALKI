import sys
sys.path.append('./flight/')
sys.path.append('./www/')

from multiprocessing import Process, Queue
from flight.fly_drone import *
from www.server import *
import time

dir_list = ["left", "right", "up", "down", "left", "right", "forward", "backward"]


def demo_flight(q):
	for i in dir_list:
		q.put(i)
		time.sleep(1)


if __name__ == '__main__':
	q = Queue()
	web = Process(target=run_server, args=(q,))
	drone = Process(target=demo_flight, args=(q,))
	web.start()
	drone.start()
	drone.join()
