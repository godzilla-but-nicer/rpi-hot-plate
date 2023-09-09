import re
import RPi.GPIO as GPIO
from time import sleep
import sys
import random

def update_temp():
    with open("/sys/bus/w1/devices/28-3c01f0963ed3/w1_slave", 'r') as fin:
        raw_text = fin.readlines()
        mat = re.findall(r"t=([0-9]+)", raw_text[1].strip())[0]
        return float(mat) / 1000

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

low = float(sys.argv[1])
high = float(sys.argv[2])

# time parameters
end_time = 10000
save_time = 2
target_move = 600

pwm = GPIO.PWM(11, 50)
pwm.start(0)

# lists for writing data
temps = []
dcs = []
times = []
targets = []
interval = 100
duty_cycle = 0

target = random.randrange(low, high)
timer = 0
while timer < end_time: # 0.33
    # check if its time to move the target
    if timer % target_move == 0:
        target = random.randrange(low, high)

    #print an update
    temp = update_temp()
    print(f"{temp:.2f} C -> {target:.2f} C")
    
    # update lists
    temps.append(temp)
    dcs.append(duty_cycle)
    times.append(timer)
    targets.append(target)

    # if hot plate is off and temp is wrong turn it on
    if target > temp:
        duty_cycle = 100
    elif temp > target:
        duty_cycle = 0

    pwm.ChangeDutyCycle(duty_cycle)
    sleep(save_time)
    timer += save_time

# write data
with open('temps.txt', 'w') as fout:
    for i in range(len(dcs)):
        fout.write(f"{times[i]},{targets[i]},{dcs[i]},{temps[i]}\n")

pwm.stop()
GPIO.cleanup()

