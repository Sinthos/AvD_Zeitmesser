#include <Arduino_LED_Matrix.h>

ArduinoLEDMatrix matrix;

// Pre-defined 2D array for the "M" pattern
byte frame[8][12] = {
     { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
     { 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0 },
     { 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0 },
     { 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0 },
     { 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0 },
     { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0 },
     { 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0 },
     { 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0 }
};

void setup() {
  pinMode(A0, OUTPUT);  // Setzt A0 als Ausgangspin
  pinMode(A1, INPUT);   // Setzt A1 als Eingangspin
  pinMode(A2, INPUT);   // Setzt A2 als Eingangspin

  Serial.begin(9600);  // Startet die serielle Kommunikation

  // Initialize LED matrix
  matrix.begin();
}

void loop() {
  analogWrite(A0, 255);  // Sendet ein hohes Signal auf A0

  // Überprüft, ob das Signal auf A1 oder A2 ankommt
  if (analogRead(A1) > 1000) {
    Serial.println("Signal auf A1 erkannt");
    shiftFrameRight();
    while(analogRead(A1) > 1000);  // Wartet, bis das Signal verschwindet
  }

  if (analogRead(A2) > 1000) {
    Serial.println("Signal auf A2 erkannt");
    shiftFrameRight();
    while(analogRead(A2) > 1000);  // Wartet, bis das Signal verschwindet
  }

  analogWrite(A0, 0);  // Schaltet das Signal auf A0 aus

  // Display the updated "M" pattern on the LED matrix
  matrix.renderBitmap(frame, 8, 12);

  delay(100);  // Wartet eine Sekunde vor der nächsten Überprüfung
}

void shiftFrameRight() {
  // Funktion zum Verschieben des Musters nach rechts
  byte temp;
  for (int row = 0; row < 8; row++) {
    temp = frame[row][11]; // Speichert das letzte Element
    for (int col = 11; col > 0; col--) {
      frame[row][col] = frame[row][col - 1];
    }
    frame[row][0] = temp; // Setzt das gespeicherte Element am Anfang
  }
}
