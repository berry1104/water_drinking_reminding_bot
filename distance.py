import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
PIN_TRIGGER = 7
PIN_ECHO = 11
button_pin = 19

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(PIN_TRIGGER, GPIO.LOW)
print("Waiting for sensor to settle")
time.sleep(2)
print("-------------------------------")

def caculate_distance():
    print("Calculating distance")
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time

    distance = round(pulse_duration * 17150, 2)

    print(f"distance is {distance} cm ")
    return distance

# print("First caculate the height of cup :  ")
# height_cup = caculate_distance()

try:
    while True:
        print("--------------------------------------")
        print("now, wait for the button to be pressed")
        GPIO.wait_for_edge(button_pin, GPIO.FALLING)
        print("Button is pressed, now sleep 2s for water surface stable")
        time.sleep(2)
        d1 = caculate_distance()
        print("Waiting for the button to be released")
        GPIO.wait_for_edge(button_pin, GPIO.RISING)
        print("Button is released")

except KeyboardInterrupt:
    pass

# 清理GPIO引脚设置
GPIO.cleanup()
