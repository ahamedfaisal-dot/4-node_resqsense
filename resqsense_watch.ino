#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

// --- Wi-Fi & Server Configuration ---
const char* ssid = "Dontsmuggle";
const char* password = "faisal123";
// Example: "http://192.168.1.100:5000/data"
const char* serverUrl = "http://10.109.8.52:5000/watchdata";


#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// === OLED ===
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// === ADXL345 ===
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

// === MAX30102 ===
MAX30105 particleSensor;

// === Pins ===
#define BUZZER_PIN D5
#define BUTTON_PIN D3

// --- Buffer for SPO2 calculation ---
#define SAMPLE_BUFFER 100
uint32_t irBuffer[SAMPLE_BUFFER];
uint32_t redBuffer[SAMPLE_BUFFER];
int32_t bufferLength = SAMPLE_BUFFER;
int32_t spo2;
int8_t validSPO2;
int32_t heartRate;
int8_t validHeartRate;

// --- Buzzer timer ---
bool buzzerActive = false;
unsigned long buzzerStartTime = 0;

// --- OLED page switch ---
int currentPage = 0;
unsigned long lastPageSwitch = 0;
const unsigned long pageInterval = 3000; // 3 sec per slide

void setupWiFi() {
  Serial.print("Connecting to ");
  Serial.println(ssid);
  display.clearDisplay();
  display.setCursor(0,0);
  display.print("Connecting to WiFi...");
  display.display();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  display.clearDisplay();
  display.setCursor(0,0);
  display.print("WiFi Connected!");
  display.setCursor(0,10);
  display.print(WiFi.localIP());
  display.display();
  delay(2000);
}


void setup() {
  Serial.begin(115200);
  Wire.begin(D2, D1); // SDA, SCL

  // --- OLED ---
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 not found"));
    while (1);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("System Boot...");
  display.display();

  // --- Connect to WiFi ---
  setupWiFi();

  // --- ADXL345 ---
  if (!accel.begin()) {
    Serial.println("ADXL345 not found");
    while (1);
  }
  accel.setRange(ADXL345_RANGE_16_G);

  // --- MAX30102 ---
  if (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) {
    Serial.println("MAX30102 not found");
    while (1);
  }
  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);
  particleSensor.setPulseAmplitudeGreen(0);

  // --- Pins ---
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  Serial.println("System Ready...");
}

void loop() {
  unsigned long now = millis();

  // --- Read Accelerometer ---
  sensors_event_t event;
  accel.getEvent(&event);

  // --- Collect MAX30102 Samples (non-blocking) ---
  for (int i = 0; i < bufferLength; i++) {
    while (!particleSensor.available()) {
      particleSensor.check();
    }
    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample();
  }

  // --- Run SPO2 Algorithm ---
  maxim_heart_rate_and_oxygen_saturation(
    irBuffer, bufferLength,
    redBuffer,
    &spo2, &validSPO2,
    &heartRate, &validHeartRate
  );

  // --- Button handling ---
  if (digitalRead(BUTTON_PIN) == LOW && !buzzerActive) {
    buzzerActive = true;
    buzzerStartTime = now;
    digitalWrite(BUZZER_PIN, HIGH);
    Serial.println("Button pressed -> Buzzer sequence started.");
  }

  // --- Handle buzzer sequence ---
  if (buzzerActive) {
    if (now - buzzerStartTime >= 15000) {
      buzzerActive = false;
      digitalWrite(BUZZER_PIN, LOW);
      Serial.println("Buzzer sequence ended.");
    }
  }

  // --- Create JSON ---
  StaticJsonDocument<256> doc;
  doc["accelerometer"]["x"] = event.acceleration.x;
  doc["accelerometer"]["y"] = event.acceleration.y;
  doc["accelerometer"]["z"] = event.acceleration.z;
  doc["heart_rate"] = validHeartRate ? heartRate : -1;
  doc["spo2"] = validSPO2 ? spo2 : -1;
  doc["button"] = digitalRead(BUTTON_PIN) == LOW ? 1 : 0;
  doc["buzzer"] = digitalRead(BUZZER_PIN);

  // --- Send JSON to Server ---
  if (WiFi.status() == WL_CONNECTED) {
    String jsonString;
    serializeJson(doc, jsonString);

    WiFiClient client;
    HTTPClient http;

    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonString);

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected. Cannot send data.");
  }


  // --- OLED Page Switch ---
  if (now - lastPageSwitch > pageInterval) {
    currentPage = (currentPage + 1) % 4; // 4 slides
    lastPageSwitch = now;
  }

  // --- OLED Display ---
  display.clearDisplay();
  display.setTextColor(WHITE);

  switch (currentPage) {
    case 0: { // Heart Rate
      display.setTextSize(3);
      display.setCursor(10, 20);
      display.print("HR:");
      display.setCursor(70, 20);
      display.print(validHeartRate ? heartRate : 0);
      break;
    }
    case 1: { // SpO2
      display.setTextSize(3);
      display.setCursor(10, 20);
      display.print("SpO2");
      display.setCursor(70, 20);
      display.print(validSPO2 ? spo2 : 0);
      display.print("%");
      break;
    }
    case 2: { // Accelerometer
      display.setTextSize(2);
      display.setCursor(0, 10);
      display.print("X:");
      display.println(event.acceleration.x, 1);
      display.setCursor(0, 30);
      display.print("Y:");
      display.println(event.acceleration.y, 1);
      display.setCursor(0, 50);
      display.print("Z:");
      display.println(event.acceleration.z, 1);
      break;
    }
    case 3: { // Button
      display.setTextSize(3);
      display.setCursor(10, 20);
      display.print("Btn:");
      display.setCursor(10, 45);
      display.print(digitalRead(BUTTON_PIN) == LOW ? "ON" : "OFF");
      break;
    }
  }

  display.display();
}
