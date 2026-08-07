#include <DHT.h> 
#include <WiFi.h> 
#include <PubSubClient.h> 

// ── Pin definitions ────────────────────────────────── 
#define DHTPIN 15 // DHT22 data pin 
#define DHTTYPE DHT22 
#define TRIG_PIN 5 // HC-SR04 trigger 
#define ECHO_PIN 18 // HC-SR04 echo 
#define POT_PIN 34 // Potentiometer (ADC) 

// ── Network & broker settings ───────────────────────── 
const char* ssid = "Wokwi-GUEST"; 
const char* password = ""; 
const char* mqttServer = "broker.hivemq.com"; 
const int mqttPort = 1883; 

// ── MQTT topics — replace GROUP_NAME with your team name ─ 
const char* topicEnv = "iot-lab/TRIAL_and_ERROR/environment"; 
const char* topicDist = "iot-lab/TRIAL_and_ERROR/distance"; 
const char* topicADC = "iot-lab/TRIAL_and_ERROR/analog"; 
const char* topicStatus = "iot-lab/TRIAL_and_ERROR/status";

DHT dht(DHTPIN, DHTTYPE); 
WiFiClient espClient; 
PubSubClient mqttClient(espClient); 

unsigned long lastPublish = 0; // Tracks timing for 5-second interval 
const long interval = 5000; // Milliseconds between publishes

void connectWiFi() { 
  Serial.print("Connecting to Wi-Fi"); 
  WiFi.begin(ssid, password); 
  int tries = 0; 
  while (WiFi.status() != WL_CONNECTED && tries < 20) { 
    delay(500); 
    Serial.print("."); 
    tries++; 
    } 
    if (WiFi.status() == WL_CONNECTED) { 
      Serial.println(" connected! IP: " + WiFi.localIP().toString()); 
      } else { 
        Serial.println(" FAILED. Check SSID."); 
      } 
}

void reconnectMQTT() { 
  int attempts = 0; 
  while (!mqttClient.connected() && attempts < 5) {
    Serial.print("Connecting to MQTT broker..."); 
    String clientId = "ESP32-" + String(random(0xFFFF), HEX); 
    if (mqttClient.connect(clientId.c_str())) { 
      Serial.println(" connected! Client: " + clientId); 
      // Publish a status message when we first connect 
      mqttClient.publish(topicStatus, "{\"event\": \"device_online\"}"); 
    } else { 
      Serial.print(" failed. rc="); 
      Serial.println(mqttClient.state()); 
      Serial.println("Retrying in 3 seconds..."); 
      delay(3000); 
      attempts++; 
    } 
  }
}

float readDistance() { 
  // Send a 10-microsecond trigger pulse 
  digitalWrite(TRIG_PIN, LOW); 
  delayMicroseconds(2); 
  digitalWrite(TRIG_PIN, HIGH); 
  delayMicroseconds(10); 
  digitalWrite(TRIG_PIN, LOW); 
  
  // Measure the echo pulse duration 
  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // timeout: 30ms 
  
  if (duration == 0) return -1.0; // No echo = out of range or error 
  
  // Convert duration to distance: speed of sound = 343 m/s = 0.0343 cm/us 
  // Divide by 2 because pulse travels to object AND back 
  float distanceCm = (duration * 0.0343) / 2.0; 
  return distanceCm; 
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(500); 
  
  dht.begin(); 
  pinMode(TRIG_PIN, OUTPUT); 
  pinMode(ECHO_PIN, INPUT); 
  // GPIO 34 is input-only by default — no pinMode needed 
  connectWiFi(); 
  mqttClient.setServer(mqttServer, mqttPort); 
  mqttClient.setKeepAlive(60); 
  reconnectMQTT(); 
}

void loop() {
  // put your main code here, to run repeatedly:
  // Maintain Wi-Fi 
  if (WiFi.status() != WL_CONNECTED) { 
    Serial.println("Wi-Fi lost. Reconnecting..."); 
    connectWiFi(); 
  } 

  // Maintain MQTT connection 
  if (!mqttClient.connected()) {
    reconnectMQTT(); 
  } mqttClient.loop(); // Process incoming messages and keepalives 
  
  // Publish every 5 seconds using non-blocking timing 
  unsigned long now = millis(); 
  if (now - lastPublish >= interval) { 
    lastPublish = now; 
    
    // ── Read DHT22 ────────────────────────────────── 
    float temp = dht.readTemperature(); 
    float hum = dht.readHumidity(); 
    
    if (!isnan(temp) && !isnan(hum)) { 
      char envMsg[80]; 
      snprintf(envMsg, sizeof(envMsg), 
          "{\"temperature\": %.1f, \"humidity\": %.1f}", 
          temp, hum); 
      mqttClient.publish(topicEnv, envMsg); 
      Serial.println("ENV: " + String(envMsg)); 
    } else { 
      Serial.println("DHT22 read error — skipping publish"); 
      mqttClient.publish(topicStatus, "{\"event\": \"dht_error\"}"); 
    } 
    
    // ── Read HC-SR04 ──────────────────────────────── 
    float dist = readDistance(); 
    char distMsg[60]; 
    if (dist > 0) { 
      snprintf(distMsg, sizeof(distMsg), 
          "{\"distance_cm\": %.1f}", 
          dist); 
    } else { 
      snprintf(distMsg, sizeof(distMsg), 
          "{\"distance_cm\": null, \"error\": \"out_of_range\"}"); 
    } 
    mqttClient.publish(topicDist, distMsg); 
    Serial.println("DIST: " + String(distMsg)); 
    
    // ── Read potentiometer (ADC) ───────────────────── 
    int rawADC = analogRead(POT_PIN); // 0 – 4095 
    float voltage = rawADC * (3.3 / 4095.0); 
    float pct = (rawADC / 4095.0) * 100.0; 
    char adcMsg[80]; 
    snprintf(adcMsg, sizeof(adcMsg), 
        "{\"raw\": %d, \"voltage\": %.2f, \"percent\": %.1f}", 
        rawADC, voltage, pct); 
    mqttClient.publish(topicADC, adcMsg); 
    Serial.println("ADC: " + String(adcMsg)); 
    Serial.println("─────────────────────────────────────"); 
  }
}
