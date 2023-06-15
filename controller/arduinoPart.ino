#include <Servo.h> 
#include <SPI.h>
#include <MFRC522.h>

#define motionPin 4 //датчик движения
#define confirmPin A0 //подтверждение закрытия, серва на 3 пин
#define buttonPin 2 //кнопка для открытия изнутри
#define SS_PIN 10 //для rc522
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

Servo servo; // объявляем переменную servo типа "servo"

bool connection = false; //для изменения режима работы, для rc522
bool confirm = false; //для подтверждения закрытия

String openEvent = "open"; // команда на открывание
String closeEvent = "close"; //команда на закрывание
String connEventT = "connectionT";
String connEventF = "connectionF";

void setup() 
{ 
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();

  pinMode(confirmPin, INPUT); //проверка закрытости
  pinMode(motionPin, INPUT); //датчик вибрации
  pinMode(buttonPin, INPUT); //кнопка

  servo.attach(3); // привязываем сервопривод к аналоговому выходу 10
  servo.write(180); //ставим в закрыто
}

void open()
{
  if (servo.read() == 180)
  {
    servo.write(0); //открываем
    delay (1000); 
  }

  if (analogRead(confirmPin) < 512) //подтверждение
  {
    Serial.println("confirmationOpened");
    delay(1000);
    confirm = false;
  }
}

void close()
{
  if (servo.read() == 0)
  {
    servo.write(180); //закрываем
    delay (1000); 
  }

  if (analogRead(confirmPin) > 512) //подтверждение
  {
    Serial.println("confirmationClosed");
    delay(1000);
    confirm = true;
  }
}

void loop() 
{
  //кнопка
  if (digitalRead(buttonPin) == HIGH)
  {
    if (servo.read() == 0)
    {
      servo.write(180); //закрываем
      delay (1000); // задержка в 1 секунду
    }
    else
    {
      servo.write(0); //открываем
      delay (1000); // задержка в 1 секунду
    }

  }

  if (Serial.available()) 
  {
    String str = Serial.readString();

    if (str == closeEvent)
    {
      Serial.println("закрываю"); //потом убрать
      close();
      //delay(500);
    }

    if (str == openEvent)
    {
      Serial.println("открываю"); //потом убрать
      open();
      //delay(500);
    }

    if (str == connEventT) //смена состояния подключения
    {
      connection = true;
    }

    if (str == connEventF) //смена состояния подключения
    {
      connection = false;
    }
  }

  //датчик вибрации
  if ((!digitalRead(motionPin)) & (confirm==true))
  {
    Serial.println("thief");
    delay(4000);
  }

  //rc522
  if (connection == false)
  {
     if ( ! mfrc522.PICC_IsNewCardPresent()) // если новая карта
    {
      return;
    }

    // выберем одну из карт
    if ( ! mfrc522.PICC_ReadCardSerial()) 
    {
      return;
    }

    String content= "";
    uint8_t letter;
    for (byte i = 0; i < mfrc522.uid.size; i++) 
    {    
      content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
      content.concat(String(mfrc522.uid.uidByte[i], HEX));
    }

    content.toUpperCase();
    if (content.substring(1) == "C3 E5 B9 52" ) 
    {  
      Serial.println("щаща");
      if (servo.read() == 0)
      {
        servo.write(180); //закрываем
        delay (1000); // задержка в 1 секунду
      }
      else
      {
        servo.write(0); //открываем
        delay (1000); // задержка в 1 секунду
      }
     
    }

  }

}




