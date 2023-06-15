/*
espMacAdress:A4-E5-7C-1E-5D-16
aspIpAdress: 192.168.0.102   */

#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "Korepich";
const char* password = "37555399";
const size_t CAPACITY = JSON_OBJECT_SIZE(1);

uint8_t tries = 10;  // Попыткок подключения к точке доступа

bool connection = true; //для переключения между режимами
bool lock;  //состояние замка

String breackingEvent = "thief";
String confirmationTrue = "confirmationOpened";
String confirmationFalse = "confirmationClosed";

WebSocketsClient webSocket;

StaticJsonDocument<200> doc; //для разбора json-строки

void setup() 
{

  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (--tries && WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.println(".");  //потом убрать
  }
  if (WiFi.status() != WL_CONNECTED) 
  {
    Serial.println("Non Connecting to WiFi.."); // потом убрать
    connection = false;
    Serial.println("connectionF");
    
  } 
  else 
  {
    // Иначе удалось подключиться отправляем сообщение
    // о подключении и выводим адрес IP
    Serial.println(""); //потом убрать
    Serial.println("WiFi connected"); //потом убрать
    Serial.println("IP address: "); //потом убрать
    Serial.println(WiFi.localIP()); //потом убрать
    connection = true;
    Serial.println("connectionT");
    //веб сокеты:
    webSocket.begin("192.168.0.101", 8000, "/api/v1/notifications/action/");
    webSocket.onEvent(webSocketEvent); 
    webSocket.setReconnectInterval(5000);
  }

}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {

	switch(type) 
    {
		case WStype_DISCONNECTED:
			Serial.printf("[WSc] Disconnected!\n");
			break;
		case WStype_CONNECTED: 
        {
			Serial.printf("[WSc] Connected to url: %s\n", payload);
		}
			break;
		case WStype_TEXT:
			Serial.printf("[WSc] get text: %s\n", payload);
      DeserializationError error = deserializeJson(doc, payload);
      
      const char* command = doc["message"];
      Serial.println(command);

      // Test if parsing succeeds.
      if (error) 
      {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.f_str());
        return;
      }

      while(true)
      {
        Serial.println(Serial.available());
        if (Serial.available())
        {
          String str = Serial.readString();

          DynamicJsonDocument doc(1024);
          String output;

          JsonObject object = doc.to<JsonObject>();
          doc["message"] = "door_action_confirmation";

          if (confirmationTrue == str) doc["status"] = true;
          if (confirmationFalse == str) doc["status"] = false;
          serializeJson(doc, output);

          Serial.println(object);

          webSocket.sendTXT(output);
          Serial.println(output);

          break;       
        }
      }
	    break;
    }
}

void breackingEvent1()
{
  HTTPClient http;
  WiFiClient client;
  StaticJsonDocument<CAPACITY> doc;
  
  String output;

  JsonObject object = doc.to<JsonObject>();
  object["door"] = 1;
  serializeJson(doc, output);

  http.begin(client, "http://192.168.0.101:8000/api/v1/breaking/");      //адрес запроса
  http.addHeader("Content-Type", "application/json");  //заголовок

  int httpCode = http.POST(output);   //Отправьте запрос
  String payload = http.getString();                  //Получите полезную нагрузку ответа

  http.end();
}

void loop() 
{
  if (Serial.available()) //чтение сообщения от меги 
  {
    String str = Serial.readString();
    if (str == breackingEvent)
    {
      breackingEvent1();
    }
  }

  if (connection = false) //попытка переподключения каждые 5 минут
  {
    if (millis() % 300000)
    {
      setup();
    }
  }
  
  webSocket.loop();
}



