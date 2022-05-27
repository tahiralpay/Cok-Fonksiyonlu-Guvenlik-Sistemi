/*                      MART 2021 TALPAY
                 ÇOK FONKSİYONLU GÜVENLİK SİSTEMİ
**************************************************************************************
  BAĞLANTI PİNLERİ:
  RASPBERRY ÇIKISI A0 NOLU DİGİTAL PİNE
  DHT11 A1 NOLU ANALOG PİNE
  MQ-9 A2 NOLU DİGİTAL PİNE

  SİM800L TX PİNİ 2 NOLU DİGİTAL PİNE
  SİM800L RX PİNİ 3 NOLU DİGİTAL PİNE
  SW-420 4 NOLU DİGİTAL PİNE
  FLAME SENSÖR 5 NOLU DİGİTAL PİNE
**************************************************************************************
  GEREKLİ KÜTÜPHANELER:
  https://github.com/adafruit/DHT-sensor-library
*/

#include "SoftwareSerial.h"
#include <DHT.h>
#include <Wire.h>

#define SIM800L_Tx 3
#define SIM800L_Rx 2

#define DHTTYPE DHT11
#define voltaj A0
#define DHTpin A1
#define deprem 4
#define ates 5

SoftwareSerial SIM800L(SIM800L_Tx, SIM800L_Rx);
DHT dht(DHTpin, DHTTYPE);

/************************** DEĞİŞKENLER ***********************************/
int deger;
int durum;
float t, h;
float vout = 0.0;
float vin = 0.0;
float R1 = 10000.0; // 10K ohm direnç
float R2 = 1000.0; // 1K ohm direnç
int value = 0;

String smsMetni = "";
void SMSgonder();

int x = 0;
int i = 0;
int j = 0;
int k = 0;
int l = 0;

/********************** SİM800L KONTROL FONKSİYONU *********************/
void SMSgonder(String mesaj) {
  SIM800L.print("AT+CMGF=1\r");
  delay(100);
  SIM800L.println("AT+CMGS=\"+905377324141\"");// 1.sahıs telefon numarasi
  delay(100);
  SIM800L.println(mesaj);
  delay(100);
  SIM800L.println((char)26);
  delay(100);
  SIM800L.println();
  delay(100);
  SIM800L.println("AT+CMGD=1,4");
  delay(100);
  SIM800L.println("AT+CMGF=1");
  delay(100);
  SIM800L.println("AT+CNMI=1,2,0,0,0");
  delay(200);
  smsMetni = "";
}

void setup() {
  dht.begin();
  Serial.begin(9600);
  SIM800L.begin(9600);

  pinMode(voltaj, INPUT);
  pinMode(deprem, INPUT);
  pinMode(ates, INPUT);

}

void loop() {
  /**************** HESAPLAMALARIN YAPILMASI *****************************/
  value = analogRead(voltaj);
  vout = (value * 5.0) / 1024.0;
  vin = vout / (R2 / (R1 + R2));
  if (vin < 0.09) {
    vin = 0.0;
  }
  h = dht.readHumidity();
  t = dht.readTemperature();
  int val = digitalRead(deprem);//sw420 titreşim sensörü
  durum = digitalRead(ates);// flame sensör
  deger = analogRead(A2); // mq9 gaz sensörü

  /**************** DEĞERLERİN SERİ POPTA YAZILMASI *****************************/
  Serial.print("voltaj: ");
  Serial.println(vin);
  Serial.print("sicaklik: ");
  Serial.println(t);
  Serial.print("titreşim durum: ");
  Serial.println(val);
  Serial.print("ateş durum: ");
  Serial.println(durum);
  Serial.print("gaz durum: ");
  Serial.println(deger);
  Serial.println(" ");

  /********************** ACİL DURUMLARDA ALICININ UYARILMASI *********************/
  /*******************************************************************************/
  if (vin >= 2.00 && x == 0) {
    smsMetni = "HAREKET ALGILANDI";
    SMSgonder(smsMetni);
    Serial.println("HAREKET ALGILANDI");
    Serial.println(" ");
    x = 1;
  }

  if (vin < 2.00) {
    x = 0;
  }

  /*******************************************************************************/
  if (deger >= 400 && i == 0) {
    smsMetni = "KIMYASAL GAZ TEHLIKESI";
    SMSgonder(smsMetni);
    Serial.println("KIMYASAL GAZ TEHLIKESI");
    Serial.println(" ");
    i = 1;
  }

  if (deger < 400) {
    i = 0;
  }

  /*******************************************************************************/
  if ((durum == 0 || (deger >= 400 && t >= 45)) && j == 0) {
    smsMetni = "YANGIN TEHLIKESI";
    SMSgonder(smsMetni);
    Serial.println("YANGIN TEHLIKESI");
    Serial.println(" ");
    j = 1;
  }

  if (durum == 1) {
    j = 0;
  }

  /*******************************************************************************/
  if (val == 1 && k == 0) {
    smsMetni = "DEPREM TEHLIKESI";
    SMSgonder(smsMetni);
    Serial.println("DEPREM TEHLIKESI");
    Serial.println(" ");
    k = 1;
  }

  if (val == 0) {
    k = 0;
  }

  /*******************************************************************************/
  if (t >= 45 && l == 0) {
    smsMetni = "SICAKLIK ARTISI";
    SMSgonder(smsMetni);
    Serial.println("SICAKLIK ARTISI");
    Serial.println(" ");
    l = 1;
  }

  if (t < 45) {
    l = 0;
  }

  delay(500);
}
