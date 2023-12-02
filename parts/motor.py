import RPi.GPIO as GPIO


class Motor:

    def __init__(self, a1, b1, e1,):
        self.Motor1A = a1
        self.Motor1B = b1
        self.Motor1E = e1
        self.current_direction = ""
        self.isRunning = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Motor1A, GPIO.OUT)  # set pins to OUTPUT mode
        GPIO.setup(self.Motor1B, GPIO.OUT)
        GPIO.setup(self.Motor1E, GPIO.OUT)

    def set_motor(self, direction, trig_pos):
        tpos = 0

        if 0.3 > trig_pos > 0:
            tpos = 0
        elif -0.3 < trig_pos < 0:
            tpos = 0
        else:
            tpos = trig_pos

        value = (round(tpos * 100))

        print(value)

        if direction == "forward" and value > 0:
            GPIO.output(self.Motor1A, GPIO.HIGH)
            GPIO.output(self.Motor1B, GPIO.LOW)
            GPIO.output(self.Motor1E, GPIO.HIGH)
            self.isRunning = True
            print('Turn Forward...')

        elif direction == "backward" and value > 0:
            GPIO.output(self.Motor1A, GPIO.LOW)
            GPIO.output(self.Motor1B, GPIO.HIGH)
            GPIO.output(self.Motor1E, GPIO.HIGH)
            self.isRunning = True
            print('Turn Backward...')

        elif value == 0:
            GPIO.output(self.Motor1E, GPIO.LOW)
            self.isRunning = False
            print('Motor Stop...')

        else:
            GPIO.output(self.Motor1E, GPIO.LOW)
            self.isRunning = False
            print('Motor Stop...')

    def change_direction(self):
        if self.current_direction == "forward":
            self.current_direction = "backward"
        else:
            self.current_direction = "forward"
