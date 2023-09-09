import re
import RPi.GPIO as GPIO
from time import sleep

def update_temp():
    with open("/sys/bus/w1/devices/28-3c01f0963ed3/w1_slave", 'r') as fin:
        raw_text = fin.readlines()
        return float(re.match(r"t=([0-9]+)", raw_text[1])) / 1000    

def temp_to_dc(temp):
    return (temp / 40) * 10.5 + 2.5

GPIO.setmode(GPIO.BOARD)
GPIO.SETUP(11, GPIO.OUT)

pwm = GPIO.PWM(11, 50)
pwm.start(0)


timer = 0
while timer < 1000: # 0.33
    temp = update_temp()
    duty_cycle = temp_to_dc(temp)
    pwm.ChangeDutyCycle(duty_cycle)
    sleep(0.33)
    timer += 1
