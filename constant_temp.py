import re
import RPi.GPIO as GPIO
from time import sleep
import sys

def update_temp():
    with open("/sys/bus/w1/devices/28-3c01f0963ed3/w1_slave", 'r') as fin:
        raw_text = fin.readlines()
        mat = re.findall(r"t=([0-9]+)", raw_text[1].strip())[0]
        return float(mat) / 1000

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

target = float(sys.argv[1])

pwm = GPIO.PWM(11, 50)
pwm.start(0)

temp_time_series = []
dcs = []
interval = 100
time_since = 0
duty_cycle = 0

timer = 0
while timer < 1000: # 0.33
    temp = update_temp()
    print(f"{temp:.2f} C")
    temp_time_series.append(temp)

    # if hot plate is off and temp is wrong turn it on
    if target > temp:
        duty_cycle = 100
    elif temp > target:
        duty_cycle = 0

    dcs.append(duty_cycle)
    pwm.ChangeDutyCycle(duty_cycle)
    sleep(1.0)
    timer += 1.0
    time_since += 1.0

# write data
with open('temps.txt', 'w') as fout:
    for i in range(len(dcs)):
        fout.write(f"{dcs[i]},{temp_time_series[i]}\n")

pwm.stop()
GPIO.cleanup()

