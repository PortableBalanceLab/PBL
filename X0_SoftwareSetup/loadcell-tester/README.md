# Load Cell Tester

> Hardware hacking project related to the Portable Balance Lab
>
> - Adam Kewley

This code is standalone from the rest of PBL, but it's for a small device
I hacked together to test load cells and [SparkFun Load Cell Amplifiers](https://www.sparkfun.com/sparkfun-load-cell-amplifier-hx711.html)
separately from the full 4-way integration that students use in S3 (force plate).

The idea behind the device is that it enables testing:

- If the amplifier works, by checking whether it responds to the controller
- If a load cell works, by displaying its raw 24-bit reading (you have to manually
  apply a force to it).

By writing the response/readings to the serial output, which can be displayed on
a connected computer.

In the future (if I get time), I also want:

- Calculating the sampling frequency (load cells can sample too slowly, which requires
  diagnosis).
- Displaying the information on an LCD screen, so that organizers don't
  have to plug it into a laptop, open a serial terminal, etc.

# Software

- Software was written in the Arduino IDE
- Requires [bogde/HX711](https://github.com/bogde/HX711), which is a HX711 library.

# Electronics

This is a rough explanation because I threw this README.md together.

- An Arduino nano was used for the device, rather than a Pi Zero, so that
  it turns on instantly and behaves very deterministically when taking readings.
- The CLK and DAT lines were connected as normal (see source code for pinout), but
  an additional 10 kOhm pullup was added between the 5V rail and DAT so that it
  deterministically returns to HIGH when the load cell isn't connected.
- Two 1 kOhm resistors were used to create a half bridge. One resistor was used to
  bridge RED to GRN. The other was used to bridge BLK to GRN. This matches the electronics
  of the S3 board.

# TODO

- Get alligator clips with male jumper terminals so that the load cells don't
  require adding pins in order to talk to this board
- Figure out how to plug pins into DE-15 (VGA) female cables so that this board can talk
  to an integrated load cell (in S3, they're all joined into one female VGA, so
  you must plug stuff into that to figure out which load cell is busted.
- Add LCD screen readout
- Add battery/easier power port (my nanos use a mini USB connector but all of the
  cables for the course are USB-C/Micro-USB/USB-A).
