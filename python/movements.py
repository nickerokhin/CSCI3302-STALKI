from pyparrot.Bebop import Bebop

MAX_TIME = 3
MAX_TILT = 40
MAX_VERT = 40

def move_up(bebop, velocity, time):
  velocity = velocity if velocity < MAX_VERT else MAX_VERT
  time = time if time < MAX_TIME else MAX_TIME
  bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=velocity, duration=time)

def move_down(bebop, velocity, time):
  velocity = velocity if velocity < MAX_VERT else MAX_VERT
  time = time if time < MAX_TIME else MAX_TIME
  bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-velocity, duration=time)

def move_forward(bebop, tilt, time):
  tilt = tilt if tilt < MAX_TILT else MAX_TILT
  time = time if time < MAX_TIME else MAX_TIME
  bebop.fly_direct(roll=0, pitch=tilt, yaw=0, vertical_movement=0, duration=time)

def move_backward(bebop, time):
  tilt = tilt if tilt < MAX_TILT else MAX_TILT
  time = time if time < MAX_TIME else MAX_TIME
  bebop.fly_direct(roll=0, pitch=-tilt, yaw=0, vertical_movement=0, duration=time)

def move_left(bebop, time):
  tilt = tilt if tilt < MAX_TILT else MAX_TILT
  time = time if time < MAX_TIME else MAX_TIME
  bebop.fly_direct(roll=tilt, pitch=0, yaw=0, vertical_movement=0, duration=time)

def move_right(bebop, time):
  tilt = tilt if tilt < MAX_TILT else MAX_TILT
  time = time if time < MAX_TIME else MAX_TIME
  bebop.fly_direct(roll=-tilt, pitch=0, yaw=0, vertical_movement=0, duration=time)
