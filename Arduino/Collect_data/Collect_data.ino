#include"TFT_eSPI.h" // Include TFT_eSPI library for TFT display.
#include"LIS3DHTR.h" // Include LIS3DHTR library for accelerometer.

TFT_eSPI tft; // Create TFT display object.
LIS3DHTR<TwoWire> lis; // Create LIS3DHTR accelerometer object using TwoWire communication.
#define CONVERT_G_TO_MS2    9.80665f // Conversion factor for acceleration from g to m/s^2.

void setup(){
  pinMode(WIO_KEY_A, INPUT_PULLUP); // Set pin mode for WIO_KEY_A button.
  tft.begin(); // Initialize TFT display.
  tft.setRotation(3); // Set display rotation.
  Serial.begin(9600); // Initialize Serial communication.
  lis.begin(Wire1); // Initialize LIS3DHTR accelerometer using Wire1 communication.
  lis.setOutputDataRate(LIS3DHTR_DATARATE_100HZ); // Set accelerometer data rate.
  lis.setFullScaleRange(LIS3DHTR_RANGE_4G); // Set accelerometer full-scale range.
  
  // Set pin modes for buttons and joystick
  pinMode(WIO_KEY_B, INPUT_PULLUP);
  pinMode(WIO_KEY_C, INPUT_PULLUP);
  pinMode(WIO_5S_RIGHT, INPUT_PULLUP);
  pinMode(WIO_5S_LEFT, INPUT_PULLUP);

}



void loop(){
  // Check if WIO_KEY_A button is pressed.
  if (digitalRead(WIO_KEY_A) == LOW) {
    Serial.println("c:(start,1,flip)");
    // Display flip data sampling animation on TFT.
    tft.fillScreen(0x0000);
    tft.setTextSize(2);
    tft.setTextColor(0xF800);
    for (int i = 0; i < 1875; i++) {
      delay(16);
      // Print accelerometer data to Serial.
      Serial.println("c:("+String(lis.getAccelerationX()*CONVERT_G_TO_MS2)+","+String(lis.getAccelerationY()*CONVERT_G_TO_MS2)+","+String(lis.getAccelerationZ()*CONVERT_G_TO_MS2)+")");
      if (i%62 == 0) {
        // Update TFT display during animation.
        tft.fillScreen(0x0000);
        tft.drawString("flip data sampling...", 0, 0);
        tft.drawCircle(160, 120, 30, 0xF800);
        tft.fillCircle(160, 120, 30, 0xF800);
      }
    }
    Serial.println("c:(end,1,flip)");
    // Display "OK" on TFT after data sampling.
    tft.fillScreen(0x0000);
    tft.setTextColor(0x7E8);
    tft.setTextSize(4);
    tft.drawString("OK", 120, 100);
  }
  // Check if WIO_KEY_B button is pressed.
  if (digitalRead(WIO_KEY_B) == LOW) {
    Serial.println("c:(start,1,idle)");
    // Display idle data sampling animation on TFT.
    tft.fillScreen(0x0000);
    tft.setTextSize(2);
    tft.setTextColor(0xF800);
    for (int i = 0; i < 1875; i++) {
      delay(16);
      // Print accelerometer data to Serial.
      Serial.println("c:("+String(lis.getAccelerationX()*CONVERT_G_TO_MS2)+","+String(lis.getAccelerationY()*CONVERT_G_TO_MS2)+","+String(lis.getAccelerationZ()*CONVERT_G_TO_MS2)+")");
      if (i%62 == 0) {
      // Update TFT display during animation.
        tft.fillScreen(0x0000);
        tft.drawString("idle data sampling...", 0, 0);
        tft.drawCircle(160, 120, 30, 0xF800);
        tft.fillCircle(160, 120, 30, 0xF800);
      }
    }
    Serial.println("c:(end,1,idle)");
    tft.fillScreen(0x0000);
    tft.setTextColor(0x7E8);
    tft.setTextSize(4);
    tft.drawString("OK", 120, 100);
  }
  // Check if WIO_KEY_C button is pressed.
  if (digitalRead(WIO_KEY_C) == LOW) {
    Serial.println("c:(start,1,down)");
    // Display down data sampling animation on TFT.
    tft.fillScreen(0x0000);
    tft.setTextSize(2);
    tft.setTextColor(0xF800);
    for (int i = 0; i < 1875; i++) {
      delay(16);
      // Print accelerometer data to Serial.
      Serial.println("c:("+String(lis.getAccelerationX()*CONVERT_G_TO_MS2)+","+String(lis.getAccelerationY()*CONVERT_G_TO_MS2)+","+String(lis.getAccelerationZ()*CONVERT_G_TO_MS2)+")");
      if (i%62 == 0) {
        // Update TFT display during animation.
        tft.fillScreen(0x0000);
        tft.drawString("down data sampling...", 0, 0);
        tft.drawCircle(160, 120, 30, 0xF800);
        tft.fillCircle(160, 120, 30, 0xF800);
      }
    }
    Serial.println("c:(end,1,down)");
    // Display "OK" on TFT after data sampling.
    tft.fillScreen(0x0000);
    tft.setTextColor(0x7E8);
    tft.setTextSize(4);
    tft.drawString("OK", 120, 100);
  }
  // Check if WIO_5S_RIGHT button is pressed.
  if (digitalRead(WIO_5S_RIGHT) == LOW) {
    Serial.println("c:(start,1,right)");
    // Display right data sampling animation on TFT.
    tft.fillScreen(0x0000);
    tft.setTextSize(2);
    tft.setTextColor(0xF800);
    for (int i = 0; i < 1875; i++) {
      delay(16);
      // Print accelerometer data to Serial.
      Serial.println("c:("+String(lis.getAccelerationX()*CONVERT_G_TO_MS2)+","+String(lis.getAccelerationY()*CONVERT_G_TO_MS2)+","+String(lis.getAccelerationZ()*CONVERT_G_TO_MS2)+")");
      if (i%62 == 0) {
        // Update TFT display during animation.
        tft.fillScreen(0x0000);
        tft.drawString("right data sampling...", 0, 0);
        tft.drawCircle(160, 120, 30, 0xF800);
        tft.fillCircle(160, 120, 30, 0xF800);
      }
    }
    Serial.println("c:(end,1,right)");
    // Display "OK" on TFT after data sampling.
    tft.fillScreen(0x0000);
    tft.setTextColor(0x7E8);
    tft.setTextSize(4);
    tft.drawString("OK", 120, 100);
  }
  // Check if WIO_5S_LEFT button is pressed.
  if (digitalRead(WIO_5S_LEFT) == LOW) {
    Serial.println("c:(start,1,left)");
    // Display left data sampling animation on TFT.
    tft.fillScreen(0x0000);
    tft.setTextSize(2);
    tft.setTextColor(0xF800);
    for (int i = 0; i < 1875; i++) {
      delay(16);
      // Print accelerometer data to Serial.
      Serial.println("c:("+String(lis.getAccelerationX()*CONVERT_G_TO_MS2)+","+String(lis.getAccelerationY()*CONVERT_G_TO_MS2)+","+String(lis.getAccelerationZ()*CONVERT_G_TO_MS2)+")");
      if (i%62 == 0) {
        // Update TFT display during animation.
        tft.fillScreen(0x0000);
        tft.drawString("left data sampling...", 0, 0);
        tft.drawCircle(160, 120, 30, 0xF800);
        tft.fillCircle(160, 120, 30, 0xF800);
      }
    }
    Serial.println("c:(end,1,left)");
    // Display "OK" on TFT after data sampling.
    tft.fillScreen(0x0000);
    tft.setTextColor(0x7E8);
    tft.setTextSize(4);
    tft.drawString("OK", 120, 100);
  }

}

}
