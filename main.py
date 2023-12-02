import time
from threading import Thread
import RPi.GPIO as GPIO
from battery.ups import UpsLite
from parts.servo_sg90 import Sg90
from parts.manette import Manette
from parts.motor import Motor
from parts.led import Led

servo = Sg90(90, 7, 105, 78)
motor = Motor(24, 23, 25)
manette = Manette(0)
stopLight = Led(20)
phare = Led(21)
turn_l = Led(16)
turn_r = Led(12)
battery = UpsLite()


def setup():
    servo.PI_PORT.start(0)
    servo.set_angle(servo.SERVO_DEFAULT_POS)


def destroy():
    servo.PI_PORT.stop()
    GPIO.cleanup()


def battery_handle():
    while True:
        battery.print_value("voltage")
        battery.print_value("capacity")
        time.sleep(10)


def manette_handler():
    while True:
        manette.controler.axis_l.when_moved = manette.on_axis_l_moved
        manette.controler.button_x.when_released = manette.on_button_x_release
        manette.controler.trigger_r.when_moved = manette.on_trigger_rt_moved
        manette.controler.button_a.when_released = manette.on_button_a_release
        manette.controler.button_trigger_r.when_released = manette.on_button_r1_release
        manette.controler.button_trigger_l.when_released = manette.on_button_l1_release

        time.sleep(0.1)


def motor_setter():
    while True:

        direction = manette.direction
        acceleration = manette.trig_rt_pos
        motor.set_motor(direction, acceleration)

        time.sleep(0.1)


def direction_setter():
    while True:

        if manette.lx_pos < 0:
            print("turn left")
            servo.move_to("left")

        elif manette.lx_pos > 0:
            print("turn right")
            servo.move_to("right")

        else:
            servo.move_to("straight")

        time.sleep(0.1)


def light_setter():
    while True:

        if not motor.isRunning:
            stopLight.on()
        else:
            stopLight.off()

        if manette.phare_is_active:
            phare.on()
        else:
            phare.off()

        time.sleep(0.1)


def flashing_setter():
    while True:

        if manette.turn_r_is_active:
            turn_r.flashing_on()
        else:
            turn_r.off()

        if manette.turn_l_is_active:
            turn_l.flashing_on()
        else:
            turn_l.off()


if __name__ == '__main__':
    print('Program is starting ... ')
    setup()

    try:

        thread_battery_handler = Thread(target=battery_handle)
        thread_manette_handler = Thread(target=manette_handler)
        thread_motor_setter = Thread(target=motor_setter)
        thread_direction_setter = Thread(target=direction_setter)
        thread_light_setter = Thread(target=light_setter)
        thread_flashing_light = Thread(target=flashing_setter)
        thread_battery_handler.start()
        thread_manette_handler.start()
        thread_motor_setter.start()
        thread_direction_setter.start()
        thread_light_setter.start()
        thread_flashing_light.start()

    except (KeyboardInterrupt, SystemExit):
        destroy()
