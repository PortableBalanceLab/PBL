#!/usr/bin/env python3

# example run command assuming SCK pin 1, DOut pin 2 and known weights 5,10,50,100: 
#   `python3 calibrate.py 1 2 5 10 50 100`

from hx711_multi import HX711
import sys
from statistics import mean, stdev
import RPi.GPIO as GPIO  # import GPIO

# init GPIO (should be done outside HX711 module in case you are using other GPIO functionality)
GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering

readings_to_average = 1  # datapoints to read per measurement

# set values using python input args
# arg 1: SCK/Clock pin
# arg 2: DOut/Measurement pin
# args 3+: known weights to use for calibration
sck_pin = None
dout_pin = None
known_weights = []
if len(sys.argv) > 1:
    sck_pin = int(sys.argv[1])
    if len(sys.argv) > 2:
        dout_pin = int(sys.argv[2])
    if len(sys.argv) > 3:
        known_weights = [float(x) for x in sys.argv[3:]]

# prompt for pin inputs if not entered as args
if sck_pin is None:
    sck_pin = input('Enter SCK/Clock pin: ')
    if not sck_pin:
        print('No SCK/Clock pin entered. Exiting..')
        quit()
    else:
        sck_pin = int(sck_pin)
if dout_pin is None:
    dout_pin = input('Enter DOut/Measurement pin: ')
    if not dout_pin:
        print('No DOut/Measurement pin entered. Exiting..')
        quit()
    else:
        dout_pin = int(dout_pin)

try:
    # create hx711 instance
    hx711 = HX711(dout_pins=dout_pin,
                  sck_pin=sck_pin,
                  channel_A_gain=128,
                  channel_select='A',
                  all_or_nothing=False,
                  log_level='CRITICAL')

    weight_multiple = hx711.run_calibration(known_weights=known_weights, readings_to_average=readings_to_average)
    print(f'Weight multiple = {weight_multiple}')

except KeyboardInterrupt:
    print('Keyboard interrupt..')
except Exception as e:
    print(e)

# cleanup GPIO
GPIO.cleanup()
