from api import MotorController
import time

mc = MotorController()

mc.update_motor_speeds(
    [
        50,
        50,
        50,
        50,
    ]
)
time.sleep(5)
mc.update_motor_speeds(
    [
        0,
        0,
        0,
        0,
    ]
)
