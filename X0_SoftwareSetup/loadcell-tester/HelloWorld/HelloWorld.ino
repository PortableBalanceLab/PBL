//www.elegoo.com
//2016.12.9

/*
  LiquidCrystal Library - Hello World

 Demonstrates the use a 16x2 LCD display.  The LiquidCrystal
 library works with all LCD displays that are compatible with the
 Hitachi HD44780 driver. There are many of them out there, and you
 can usually tell them by the 16-pin interface.

 This sketch prints "Hello World!" to the LCD
 and shows the time.

  The circuit:
 * LCD RS pin to digital pin 7
 * LCD Enable pin to digital pin 8
 * LCD D4 pin to digital pin 9
 * LCD D5 pin to digital pin 10
 * LCD D6 pin to digital pin 11
 * LCD D7 pin to digital pin 12
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

 Library originally added 18 Apr 2008
 by David A. Mellis
 library modified 5 Jul 2009
 by Limor Fried (http://www.ladyada.net)
 example added 9 Jul 2009
 by Tom Igoe
 modified 22 Nov 2010
 by Tom Igoe

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/LiquidCrystal
 */

#include <Arduino.h>
#include <HX711.h>
#include <LiquidCrystal.h>

constexpr int LOADCELL_DOUT_PIN = 16;
constexpr int LOADCELL_SCK_PIN = 15;
constexpr int SERIAL_BAUD = 9600;

namespace
{
  template<class T>
  T exchange(T& obj, T new_value) { T old_value = obj; obj = new_value; return old_value; }
}

int main(void) {
  init();
  // pinMode(LED_BUILTIN, OUTPUT);

  // initialize the library with the numbers of the interface pins
  LiquidCrystal lcd(2, 3, 7, 8, 9, 10);
  lcd.begin(16, 2);

  HX711 loadcell;
  loadcell.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

  unsigned long last_update = 0;
  unsigned long measurements_since_last_update = 0;
  unsigned long measurement_times_accumulator = 0;
  long last_reading = 0;
  bool waiting = true;
  while (true) {
    const unsigned long before = millis();

    // Perform measurement
    if (loadcell.wait_ready_retry(100, 10)) {
      const long reading = loadcell.read();
      const unsigned long after = millis();

      measurements_since_last_update++;
      measurement_times_accumulator += after - before;
      last_reading = reading;
      if (exchange(waiting, false)) {
        lcd.clear();
      }
    }
    else {
      if (not exchange(waiting, true)) {
        lcd.clear();
      }
    }

    // Calculate+perform screen update
    if (before > last_update + 100) {
      if (waiting) {
        lcd.setCursor(0, 0);
        lcd.print("    Waiting");
        lcd.setCursor(0, 1);
        lcd.print("Insert load cell");
      }
      else {
        lcd.setCursor(0, 0);
        lcd.print("Value: ");
        lcd.print(last_reading);
        lcd.setCursor(0, 1);
        lcd.print("Rate : ");
        lcd.print(static_cast<double>(measurement_times_accumulator)/measurements_since_last_update);
        lcd.print(" Hz");
      }
      last_update = before;
      measurements_since_last_update = 0;
      measurement_times_accumulator = 0;
    }
  }
}
