#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>

// button setup including debouncing
int button_cur_state = LOW;
int button_pressed = LOW;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 10;

const char* phrases[] = {"My dear human, give me food", "I'm hungry", "Please, feed me, human", "It's time for the meal", "Waiting for you in the kitchen"};

// network credentials
const char* ssid = "";        // should be wifi network name here
const char* password = "";    // should be wifi password here

// Telegram BOT and a chat info
#define BOTTOKEN "6662534510:AAGocIvjIHkuhHuCgEVM6eqRJPutFQDhnK0"
#define CHAT_ID ""            // should be chat / user ID here, can be taken from @myidbot

WiFiClientSecure client;
UniversalTelegramBot bot(BOTTOKEN, client);

void setup()
{ 
  Serial.begin(115200);

  pinMode(D7, INPUT_PULLUP);
  
  // Connect to Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  // Add root certificate for api.telegram.org
  client.setCACert(TELEGRAM_CERTIFICATE_ROOT);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  // Print local IP Address
  Serial.println(WiFi.localIP());
  Serial.println("Setup done");

  // bot.sendMessage(CHAT_ID, "Feed system is ON", "");
}

void loop()
{
  int button_val = digitalRead(D7);

  if (button_val != button_cur_state) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (button_val != button_pressed) {
      Serial.printf("Status changed from %d to %d\n", button_pressed, button_val);
      button_pressed = button_val;
      if (button_val == HIGH) {
        // send message only when button is pressed for some time to avoud noise
        bot.sendMessage(CHAT_ID, phrases[random(5)], "");
      }
    }
  }

  button_cur_state = button_val;
}