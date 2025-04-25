#include <Mouse.h>

const int xPin = A1;
const int yPin = A0;
const int buttonPin = 3;

const int center = 512;
const int deadzone = 25;

unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 50;
int lastButtonState = HIGH;
int debouncedButtonState = HIGH;

void setup() {
  Serial.begin(9600);
  pinMode(xPin, INPUT);
  pinMode(yPin, INPUT);
  pinMode(buttonPin, INPUT_PULLUP);
}

int applyDeadzone(int value) {
  if (abs(value) < deadzone) {
    return 0;
  }
  return value;
}

int scale(int value, double in_min, double in_max, double out_min, double out_max) {
  return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void loop() {
  int rawX = analogRead(xPin) - center;
  int rawY = analogRead(yPin) - center;
  int xVal = -scale(applyDeadzone(rawX), -center, 1023 - center, -100, 100);
  int yVal = scale(applyDeadzone(rawY), -center, 1023 - center, -100, 100);

  int reading = digitalRead(buttonPin);

  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != debouncedButtonState) {
      debouncedButtonState = reading;
    }
  }

  lastButtonState = reading;

  if(debouncedButtonState == LOW) {
    Serial.print("X");
  } else {
    Serial.print(xVal);
    Serial.print(",");
    Serial.print(yVal);
  }
  Serial.println();

  delay(20);
}
