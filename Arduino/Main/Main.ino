// Define Blynk template ID, name, authentication token, and print configuration.
#define BLYNK_TEMPLATE_ID           "TMPL4axNVK7Vu"
#define BLYNK_TEMPLATE_NAME         "Quickstart Device"
#define BLYNK_AUTH_TOKEN            "NmEFh0ohBnnS-Xwmykao8XBWPLOkoHoN"
#define BLYNK_PRINT Serial

// Include necessary libraries.
#include <rpcWiFi.h> // Library for Wi-Fi communication on Wio Terminal.
#include <WiFiClient.h> // Standard Arduino library for Wi-Fi Client
#include <BlynkSimpleWioTerminal.h> // Blynk library for Wio Terminal
#include <Presentation_control_3_inferencing.h> // This is the edge impulse model to compute the inference.
#include "TFT_eSPI.h" // TFT_eSPI library for TFT screen functionalities
#include "LIS3DHTR.h" // LIS3DHTR library for accelerometer functionalities

// Set WiFi credentials.
char ssid[] = "gamificationlab";
char pass[] = "gamlab-11";

// Initialize TFT screen and LIS3DHTR accelerometer.
TFT_eSPI tft;
LIS3DHTR<TwoWire> lis;
#define CONVERT_G_TO_MS2    9.80665f
// Array to store current classification results and label with maximum confidence.
ei_impulse_result_classification_t currentClassification[EI_CLASSIFIER_LABEL_COUNT];
const char* maxConfidenceLabel;

// Function to run the edge impulse classifier.
void runClassifier()
{
  // Acquire accelerometer data and populate the buffer.
  float buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE] = { 0 };
  for (size_t ix = 0; ix < EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE; ix += 3) {
    uint64_t next_tick = micros() + (EI_CLASSIFIER_INTERVAL_MS * 1000);
    lis.getAcceleration(&buffer[ix], &buffer[ix + 1], &buffer[ix + 2]);
    buffer[ix + 0] *= CONVERT_G_TO_MS2;
    buffer[ix + 1] *= CONVERT_G_TO_MS2;
    buffer[ix + 2] *= CONVERT_G_TO_MS2;
    delayMicroseconds(next_tick - micros());
  }
  signal_t signal;
  int err = numpy:: signal_from_buffer(buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
  ei_impulse_result_t result = { 0 };

  err = run_classifier(&signal, &result, false); // Run the edge impulse classifier.
  
  // Find the label with maximum confidence.
  float maxValue = 0;
  for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
    ei_impulse_result_classification_t classification_t = result.classification[ix];
    ei_printf("    %s: %.5f\n", classification_t.label, classification_t.value);
    float value = classification_t.value;
    if (value > maxValue) {
      maxValue = value;
      maxConfidenceLabel = classification_t.label;
    }
    currentClassification[ix] = classification_t;
  }
  // Send the result to Blynk.
  Blynk.virtualWrite(V0, maxConfidenceLabel);
}

void setup()
{
  // Initialize serial communication.
  Serial.begin(115200);

  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass); // Initialize Blynk with authentication token and Wi-Fi credentials.
  
  // Initialize TFT screen and LIS3DHTR accelerometer.
  tft.begin();
  lis.begin(Wire1);
  lis.setOutputDataRate(LIS3DHTR_DATARATE_100HZ);
  lis.setFullScaleRange(LIS3DHTR_RANGE_4G);
  
  // Configure TFT screen.
  tft.setRotation(3);
  tft.setTextSize(5);
  tft.setTextColor(TFT_GREEN);
  tft.fillScreen(TFT_BLACK);
}

void loop()
{
  Blynk.run(); // Run Blynk.
  runClassifier(); // Run the edge impulse classifier and display results on TFT screen.
  tft.setTextSize(5);
  tft.fillScreen(TFT_BLACK);
  tft.drawString((String)maxConfidenceLabel, 100, 110);
}

