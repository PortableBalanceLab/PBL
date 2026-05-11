#include "HX711.h"

#include <Arduino.h>

constexpr int LOADCELL_DOUT_PIN = 16;
constexpr int LOADCELL_SCK_PIN = 15;
constexpr int SERIAL_BAUD = 9600;

int main(void) {
  init();
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(SERIAL_BAUD);

  HX711 loadcell;
  loadcell.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

  // Core loop: check connection, make measurement if connection is ok
  while (true) {
    if (loadcell.wait_ready_retry(100, 10)) {
      Serial.print("Weight: ");
      Serial.println(loadcell.read());
    }
    else {
      Serial.println("Not ready");
    }
  }
}

