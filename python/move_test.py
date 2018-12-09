from pyparrot.Bebop import Bebop

bebop = Bebop()

print("connecting")
success = bebop.connect(10)
print(success)

try:
  if (success):

    bebop.smart_sleep(2)

    bebop.ask_for_state_update()

    print('taking off')
    bebop.safe_takeoff(10)

    bebop.set_max_tilt(5)
    bebop.set_max_vertical_speed(1)

    bebop.set_hull_protection(1)

    print("Flying direct: Slow move for indoors")
    bebop.fly_direct(roll=0, pitch=0, yaw=180, vertical_movement=0, duration=5)

    print('taking off')
    bebop.safe_land(20)

    bebop.smart_sleep(5)
    bebop.disconnect()
except Exception:
  bebop.emergency_land()

