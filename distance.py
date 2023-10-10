#from Adafruit_CharLCD import Adafruit_CharLCD # Importing Adafruit library for LCD
import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BOARD)
PIN_TRIGGER = 7
PIN_ECHO = 11
button_pin = 19

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# initiate lcd and specify pins
#lcd = Adafruit_CharLCD (rs=26, en=19, d4=13, d5=6, d6=5, d7=21, cols=16, lines=2)
#lcd.clear()
#lcd.message('WELCOME TO \nIoT WATER BOT')

DIAMETER = 5.0  # Diameter of the cup in centimeters

GPIO.output(PIN_TRIGGER, GPIO.LOW)
print("Waiting for sensor to settle")
time.sleep(2)
print("-------------------------------")

def caculate_distance():
    print("\tCalculating distance")
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time

    distance = round(pulse_duration * 17150, 2)

    
    return distance



def get_amount(d_before, d_after, d):
    '''
    d_before: distance before drinking water in cm
    d_after: distance after drinking water in cm
    d: diameter of the cup in cm
    amount : amount of water in ml
    '''
    # Calculate the radius of the cup
    r = d / 2.0
    
    # Calculate the change in water height
    height_change = d_after - d_before
    
    # Calculate the volume of water (in milliliters)
    # Using the formula for the volume of a cylinder V = π * r^2 * h, where h is the height change
    volume = math.pi * (r ** 2) * height_change
    
    # Convert the volume from cubic centimeters to milliliters (1 cm^3 = 1 ml)
    amount = volume
    
    return amount

# Example usage



try:
    while True:
        
        print("-----------------------------------------------------")
        # before
        print("-----before drink water, press the button to start-----")
        GPIO.wait_for_edge(button_pin, GPIO.FALLING)
        print("\tButton is pressed, now collect the data before drink water")
        time.sleep(2)
        d_before = caculate_distance()
        print(f"\tBefore drinking, the distance is {d_before} cm ")
        
        #GPIO.wait_for_edge(button_pin, GPIO.RISING)
        print("\tButton is released")

        #after
        print("-----after drink water, press the button to start-----")
        GPIO.wait_for_edge(button_pin, GPIO.FALLING)
        print("\tButton is pressed, now collect the data after drink water")
        time.sleep(2)
        d_after = caculate_distance()
        print(f"\tAfter drinking, the distance is {d_after} cm ")
        
        #GPIO.wait_for_edge(button_pin, GPIO.RISING)
        print("\tButton is released")
        
        # get the amount of water and time
        amount = get_amount(d_before, d_after,DIAMETER)
        now = time.ctime()
        # print the result
        print("")
        print(f"\t{now} drink  {amount} ml water")
        #lcd.message('f{now} \n drink {amount} ml wate')

except KeyboardInterrupt:
    pass

# 清理GPIO引脚设置
GPIO.cleanup()
