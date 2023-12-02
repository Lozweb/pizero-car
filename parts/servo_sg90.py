import RPi.GPIO as GPIO


class Sg90:

    def __init__(self, default_pos, servo_pin, max_value, min_value):
        self.SERVO_PIN = servo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)
        GPIO.output(self.SERVO_PIN, GPIO.LOW)
        self.PI_PORT = GPIO.PWM(self.SERVO_PIN, 50)
        self.OFFSET_DUTY = 0.5
        self.SERVO_MIN_DUTY = 2.5 + self.OFFSET_DUTY
        self.SERVO_MAX_DUTY = 12.5 + self.OFFSET_DUTY
        self.SERVO_DEFAULT_POS = default_pos
        self.current_pos = self.SERVO_DEFAULT_POS
        self.MAX_VALUE = max_value
        self.MIN_VALUE = min_value

    @staticmethod
    def mapping(value, from_low, from_high, to_low, to_high):
        return (to_high - to_low) * (value - from_low) / (from_high - from_low) + to_low

    def set_angle(self, angle):
        if angle < self.MIN_VALUE:
            angle = self.MIN_VALUE

        elif angle > self.MAX_VALUE:
            angle = self.MAX_VALUE

        self.PI_PORT.ChangeDutyCycle(
            self.mapping(
                angle,
                0,
                180,
                self.SERVO_MIN_DUTY,
                self.SERVO_MAX_DUTY))

        self.current_pos = angle

    def move_to(self, direction):
        if direction == "left":
            self.set_angle(self.MIN_VALUE)
        elif direction == "right":
            self.set_angle(self.MAX_VALUE)
        else:
            self.set_angle(self.SERVO_DEFAULT_POS)

