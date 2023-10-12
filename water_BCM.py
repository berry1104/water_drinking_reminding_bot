# from Adafruit_CharLCD import Adafruit_CharLCD # Importing Adafruit library for LCD
import RPi.GPIO as GPIO
import time
import math
import Adafruit_CharLCD as LCD
import sqlite3

# Switch to BCM numbering mode
GPIO.setmode(GPIO.BCM)

# Define BCM GPIO pins
PIN_TRIGGER = 4  # Corresponds to BCM GPIO 4
PIN_ECHO = 13    # Corresponds to BCM GPIO 13
button_pin = 19  # Corresponds to BCM GPIO 19

# Raspberry Pi pin setup
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize the LCD
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

lcd.message('Drink Bot')
# Wait 5 seconds
time.sleep(5.0)
lcd.clear()



DIAMETER = 6.7  # Diameter of the cup in centimeters

GPIO.output(PIN_TRIGGER, GPIO.LOW)
print("Waiting for sensor to settle")
time.sleep(2)
print("-------------------------------")

def caculate_distance():
    #print("\tCalculating distance")
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

def get_median(d1,d2,d3):
    list=[d1,d2,d3]
    return sorted(list)[1]
    

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
    
    
    return round(volume,2)

def create_table():
    try:
        with sqlite3.connect('water_data_test.db') as conn:
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS water_data
               (id INTEGER PRIMARY KEY AUTOINCREMENT, now TEXT, amount REAL)''')
    except sqlite3.Error as e:
        print("SQLITE ERROR", e)

def insert_data(amount, now):
    try:
        with sqlite3.connect('water_data_test.db') as conn:
            cursor = conn.cursor()

            cursor.execute("INSERT INTO water_data (now, amount) VALUES (?, ?)", (now, amount))
            conn.commit()
    except sqlite3.Error as e:
        print("SQLITE ERROR", e)

create_table()

try:
    while True:
        
        print("-----------------------------------------------------")
        # before
        print("-----before drink water, press the button to start-----")
        lcd.clear()
        lcd.message('before drink\npress the button')
        GPIO.wait_for_edge(button_pin, GPIO.FALLING)
        lcd.clear()
        print("\tButton is pressed, now collect the data before drink water")
        lcd.message('Button is pressed')
        time.sleep(2)
        lcd.clear()
        d_1 = caculate_distance()
        time.sleep(0.1)
        d_2 = caculate_distance()
        time.sleep(0.1)
        d_3 =caculate_distance()
        time.sleep(0.1)
        d_before = get_median(d_1,d_2,d_3)
        print(f"\tBefore drinking, the distance is {d_before} cm ")
        
        #GPIO.wait_for_edge(button_pin, GPIO.RISING)
        print("\tButton is released")

        #after
        print("-----after drink water, press the button to start-----")
        lcd.message('after drink\npress the button')
        GPIO.wait_for_edge(button_pin, GPIO.FALLING)
        lcd.clear()
        print("\tButton is pressed, now collect the data after drink water")
        lcd.message('Button is pressed')
        time.sleep(2)
        lcd.clear()
        da_1 = caculate_distance()
        time.sleep(0.1)
        da_2 = caculate_distance()
        time.sleep(0.1)
        da_3 =caculate_distance()
        time.sleep(0.1)
        d_after = get_median(da_1,da_2,da_3)
        print(f"\tAfter drinking, the distance is {d_after} cm ")
        
        #GPIO.wait_for_edge(button_pin, GPIO.RISING)
        print("\tButton is released")
        
        # get the amount of water and time
        amount = get_amount(d_before, d_after,DIAMETER)
        now = time.ctime()
        insert_data(amount, now)
        # print the result
        print("")
        result = f"{now} \n{amount} ml water"
        print(result)
        lcd.message(result)
        time.sleep(5)
        #lcd.clear()
      

except KeyboardInterrupt:
    pass

# Clean up GPIO pin settings
GPIO.cleanup()
