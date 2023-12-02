from battery.ups import UpsLite
import time

battery = UpsLite()

while True:
    battery.print_value("voltage")
    battery.print_value("capacity")
    time.sleep(1)
