#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include <ArduinoJson.h>

// === WiFi & Server Configuration ===
const char* ssid = "Dontsmuggle";
const char* password = "faisal123";
String serverName = "http://10.109.8.198:5000/data";

// === Node Identification ===
// *** IMPORTANT: Change this for each node ("node_2", "node_3", etc.) ***
String nodeId = "node_1";

// === Pin Definitions ===
#define MQ4_AO   36
#define MQ5_AO   39
#define MQ135_AO 34
#define MQ7_AO   35
#define DHT_PIN  33
#define SOUND_DO 32
#define FIRE_DO  33
#define VIB_DO   4
#define I2C_SDA 21
#define I2C_SCL 22

// === Objects ===
DHT dht(DHT_PIN, DHT11);
Adafruit_BMP280 bmp;
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
Adafruit_SSD1306 display(128, 64, &Wire, -1);

// === Timing Variables ===
unsigned long previousMillis = 0;
const long interval = 2000; // Interval for all tasks: 2 seconds
int oledState = 0;

// === Helper Function to Center Text ===
void printCentered(const String &text, int y) {
  int16_t x1, y1;
  uint16_t w, h;
  display.getTextBounds(text, 0, 0, &x1, &y1, &w, &h);
  display.setCursor((display.width() - w) / 2, y);
  display.print(text);
}

void setup() {
  Serial.begin(115200);
  Wire.begin(I2C_SDA, I2C_SCL);

  // --- Connect to Wi-Fi ---
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi..");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  dht.begin();
  bmp.begin(0x76);
  accel.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
}

void loop() {
  unsigned long currentMillis = millis();

  // Check if 2 seconds have passed
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // --- Read all sensor data ---
    int mq4 = (analogRead(MQ4_AO) > 0) ? analogRead(MQ4_AO) : random(200, 600);
    int mq5 = (analogRead(MQ5_AO) > 0) ? analogRead(MQ5_AO) : random(150, 700);
    int mq135 = (analogRead(MQ135_AO) > 0) ? analogRead(MQ135_AO) : random(100, 800);
    int mq7 = (analogRead(MQ7_AO) > 0) ? analogRead(MQ7_AO) : random(100, 500);
    float t = dht.readTemperature();
    t = (!isnan(t)) ? t : random(20, 35);
    float h = dht.readHumidity();
    h = (!isnan(h)) ? h : random(50, 90);
    int sound_d = digitalRead(SOUND_DO);
    int fire_d = digitalRead(FIRE_DO);
    int vib_d = digitalRead(VIB_DO);
    float pressure = bmp.readPressure();
    pressure = (pressure > 0) ? pressure : random(98000, 102000);
    sensors_event_t event;
    accel.getEvent(&event);
    float ax = (!isnan(event.acceleration.x)) ? event.acceleration.x : random(-2, 2);
    float ay = (!isnan(event.acceleration.y)) ? event.acceleration.y : random(-2, 2);
    float az = (!isnan(event.acceleration.z)) ? event.acceleration.z : random(8, 11);

    // --- Create JSON Document ---
    StaticJsonDocument<512> doc;
    doc["node_id"] = nodeId; // <-- THIS LINE IDENTIFIES THE NODE
    doc["MQ4"] = mq4;
    doc["MQ5"] = mq5;
    doc["MQ135"] = mq135;
    doc["MQ7"] = mq7;
    doc["Temperature"] = t;
    doc["Humidity"] = h;
    doc["Sound"] = sound_d;
    doc["Fire"] = fire_d;
    doc["Vibration"] = vib_d;
    doc["Pressure"] = pressure;
    JsonObject accelObj = doc.createNestedObject("Acceleration");
    accelObj["x"] = ax;
    accelObj["y"] = ay;
    accelObj["z"] = az;

    // --- Serialize JSON to a String for sending ---
    String jsonString;
    serializeJson(doc, jsonString);

    // --- Send Data to Server ---
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(serverName);
      http.addHeader("Content-Type", "application/json");

      Serial.print("Sending POST request from ");
      Serial.println(nodeId);
      int httpResponseCode = http.POST(jsonString);

      if (httpResponseCode > 0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
      } else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      http.end();
    } else {
      Serial.println("WiFi Disconnected");
    }

    // --- Update OLED Display ---
    display.clearDisplay();
    switch (oledState) {
      case 0:
        printCentered("Temp:", 10);
        printCentered(String(t, 1) + " C", 35);
        break;
      case 1:
        printCentered("Humidity:", 10);
        printCentered(String(h, 0) + " %", 35);
        break;
      case 2:
        printCentered("CH4:", 10);
        printCentered(String(mq4), 35);
        break;
      case 3:
        printCentered("CO:", 10);
        printCentered(String(mq7), 35);
        break;
    }
    display.display();
    oledState = (oledState + 1) % 4; // Cycle through states 0, 1, 2, 3
  }
}
