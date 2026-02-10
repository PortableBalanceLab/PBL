#!/usr/bin/env python3

from hx711_multi import HX711
from RPi import GPIO
import argparse
import time

# top-level variables
_readings_to_average = 1
_readings_to_average_for_zeroing = 128 * _readings_to_average

def _run_unguarded(
    clock_pin,
    data_pins,
    rate,
    ignore_errors):

    GPIO.setmode(GPIO.BCM)

    hx711 = HX711(
        dout_pins=[int(pin) for pin in data_pins],
        sck_pin=int(clock_pin),
        channel_A_gain=128,
        channel_select='A',
        all_or_nothing=False,
        log_level='CRITICAL'  # change this if you're having hardware problems
    )
    hx711.reset()

    try:
        hx711.zero(_readings_to_average_for_zeroing)  # can raise `Exception` if connection is broken
    except Exception as e:
        if ignore_errors:
            print(e)
        else:
            raise e

    try:
        prev_line_len = 0
        while True:
            cur_vals = hx711.read_raw(readings_to_average=_readings_to_average)

            # round vals to the nearest integer
            displayed_vals = [round(val) if val else val for val in cur_vals]

            # print, overwriting previous output
            line = ", ".join([f"Pin({pin}) = {val}" for pin, val in zip(data_pins, displayed_vals)])
            print(f'{prev_line_len * " "}\r', end='')
            print(line, end='')

            time.sleep(1.0/rate)

            prev_line_len = len(line)
    except KeyboardInterrupt:
        pass  # just exit if user presses Ctrl+C or similar
    finally:
        print('')  # ensure a newline is output

def run(
    clock_pin,
    data_pins,
    rate,
    ignore_errors):

    GPIO.setmode(GPIO.BCM)
    try:
        _run_unguarded(
            clock_pin,
            data_pins,
            rate,
            ignore_errors
        )
    finally:
        GPIO.cleanup()

def main():
    parser = argparse.ArgumentParser("identify", description="identify which pins are connected to which plate")
    parser.add_argument("clock_pin", type=int)
    parser.add_argument("data_pins", nargs='+', type=int)
    parser.add_argument("--rate", default=1.0, type=float)
    parser.add_argument("--ignore-errors", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    run(
        clock_pin=int(args.clock_pin),
        data_pins=[int(data_pin) for data_pin in args.data_pins],
        rate=float(args.rate),
        ignore_errors=bool(args.ignore_errors)
    )

if __name__ == '__main__':
    main()
