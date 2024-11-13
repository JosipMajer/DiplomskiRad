#include <WiFi.h>  // Spajanje na WiFi
#include <WiFiUdp.h>  // Za primanje i slanje paketa pomocu UDPa
#include <string.h> // Za manipulaciju stringovima
#include <Adafruit_ILI9341.h>   // Za komunikaciju sa ekranom
#include <Adafruit_GFX.h>   // Za iscrtavanja grafičkih objekata

// Konstante za spajanje na WiFi
const char* ssid = "TIOSLAN";   // Ime Wifi mreze
const char* password = "suzasuza";    // Lozinka za mrezu
const int CONNECTION_TIMEOUT = 10;  // Koliko dugo trazi mrezu

// Varijable za UDP komunikaciju
WiFiUDP Udp;  // Definicija Udp
char packet_buffer[255]; // Niz od 255 bytova za nadolazecu poruku
uint8_t  reply_buffer[] = "HelloTIOSS";  // Odgovor za indentifikaciju kontrolera
const char tioss_message[] = "ThisIsTIOSS";  // Poruka koja se ocekuje od robota
IPAddress tioss_ip;  // Variabla za zapis ip adrese servera
unsigned int tioss_port = 5005;  // Dogovoreni port za socket

// ILI9341 TFT LCD deklaracija pinova
#define TFT_CS 5
#define TFT_DC 21

// Tipke
#define BTN_UP_DOWN  35
#define BTN_LEFT_RIGHT 34
#define BTN_A  32
#define BTN_B  33
#define BTN_MENU 13
#define BTN_SELECT 27
#define BTN_START  39 
#define BTN_VOL  0

// stvaranje objekta ekrana koji će se zvati tft
Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC);

void connectToWiFi()
{
  WiFi.mode(WIFI_STA); // Postavi WiFi mod u klijenta
  WiFi.begin(ssid, password); // Zapocni spajanje sa gore definiranim podatcima
  // Iscrtavanje na ejran
  tft.fillScreen(ILI9341_BLACK); // Boja zaslona
  tft.setTextSize(4); // Velicina teksta
  tft.setRotation(3); // Orijentacija teksta
  tft.setTextColor(ILI9341_RED);
  tft.setCursor(40,80);
  tft.print("Connecting");
  tft.setCursor(10,120);
  // Potrebne varijable
  int dot_counter = 0;
  int timeout_counter = 0;
  
  // Pricekaj dok se ne spoji na wifi
  while(WiFi.status() != WL_CONNECTED)
  {
    tft.print(".");
    delay(100);
    dot_counter++;
    timeout_counter++;
    if (dot_counter > 11)
    {
      tft.fillRect(10,120,300,40,ILI9341_BLACK);
      tft.setCursor(10,120);
      dot_counter = 0;
    }
    // ako pre dugo traje da se eps32 resetira
    if(timeout_counter >= CONNECTION_TIMEOUT * 5)
      ESP.restart();
  }
}

void connectedWIFI()
{
 tft.fillScreen(ILI9341_BLACK); // boja zaslona
 tft.setTextSize(1);
 tft.setRotation(3);
 tft.setCursor(0,0);
 tft.setTextColor(ILI9341_WHITE);
 tft.print("Connected: ");
 tft.setTextColor(ILI9341_GREEN);
 tft.print("TIOSLAN");
}

void findTIOSS()  // Funkcija za pronalazak IP adrese servera 
{
  tft.setTextSize(4);
  tft.setTextColor(ILI9341_RED);
  tft.setCursor(40,80);
  tft.print("Connecting");
  tft.setCursor(60,120);
  tft.print("to TIOSS");
  while (1) // Dok ga ne nades
  {
    int packet_size = Udp.parsePacket(); // Procitaj paket
    if (packet_size) // ako paket nije prazan
    {
      int len = Udp.read(packet_buffer, 255);  
      if (len > 0) 
      {
        packet_buffer[len] = 0;
      }
      if (!strcmp(packet_buffer, tioss_message)) // Provjera jeli se javio server 
      {
        tioss_ip = Udp.remoteIP(); // Zabiljezi ip adresu kako adresu servera
        // Vratiti odgovor kako bi se uspostavila komunikacija
        sendMessage(reply_buffer);
        return; // Izlaz i funkcije
      }
    }
  }
}

void connectedTIOSS()
{
  connectedWIFI();
  tft.setCursor(0,10);
  tft.setTextColor(ILI9341_WHITE);
  tft.print("Connected: ");
  tft.setTextColor(ILI9341_GREEN);
  tft.print("TIOSS");
}

void sendMessage(uint8_t *packet)
{
  int messegeSize = 0;
  while (packet[messegeSize] != '\0')
  {
    messegeSize++;
  }
  Udp.beginPacket(tioss_ip, tioss_port);
  Udp.write(packet, messegeSize);
  Udp.endPacket();
}

void startMainMenu()
{
  tft.setCursor(70,80);
  tft.setTextSize(4);
  tft.setTextColor(ILI9341_BLACK, ILI9341_WHITE);
  tft.print(" Glava ");
  tft.setCursor(70,120);
  tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.print(" Ruke ");
  tft.setCursor(110,230);
  tft.setTextSize(1);
  tft.setTextColor(ILI9341_WHITE);
  tft.print("Odabir: ");
  tft.setTextColor(ILI9341_RED);
  tft.print("SELECT");
}

void updateManinMenu(int a)
{
  tft.setCursor(70,80);
  tft.setTextSize(4);
  if (a == 0)
    tft.setTextColor(ILI9341_BLACK, ILI9341_WHITE);
  else
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.print(" Glava ");
  tft.setCursor(70,120);
  if (a == 1)
    tft.setTextColor(ILI9341_BLACK, ILI9341_WHITE);
  else
    tft.setTextColor(ILI9341_WHITE, ILI9341_BLACK);
  tft.print(" Ruke  ");
}

void initializePins() // Inicijalizacija pinova tipki
{
  pinMode(BTN_UP_DOWN, INPUT_PULLUP);
  pinMode(BTN_LEFT_RIGHT, INPUT_PULLUP);
  pinMode(BTN_A, INPUT_PULLUP);
  pinMode(BTN_B, INPUT_PULLUP);
  pinMode(BTN_MENU, INPUT_PULLUP);
  pinMode(BTN_SELECT, INPUT_PULLUP);
  pinMode(BTN_START, INPUT_PULLUP);
  pinMode(BTN_VOL, INPUT_PULLUP);
}

void glavaScreen()
{
  connectedTIOSS();
  tft.setCursor(70,30);
  tft.setTextSize(4);
  tft.setTextColor(ILI9341_WHITE);
  tft.print(" Glava ");
  tft.setCursor(0,90);
  tft.setTextSize(2);
  tft.setTextColor(ILI9341_WHITE);
  tft.print("Desno:   ");
  tft.setTextColor(ILI9341_RED);
  tft.print("RIGHT");
  tft.setTextColor(ILI9341_WHITE);
  tft.print("\nLijevo:  ");
  tft.setTextColor(ILI9341_RED);
  tft.print("LEFT");
  tft.setTextColor(ILI9341_WHITE);
  tft.print("\n\nNazad:   ");
  tft.setTextColor(ILI9341_RED);
  tft.print("MENU");
}

void rukeScreen()
{
  connectedTIOSS();
  tft.setCursor(75,30);
  tft.setTextSize(4);
  tft.setTextColor(ILI9341_WHITE);
  tft.print(" Ruke  ");
  tft.setCursor(0,90);
  tft.setTextSize(2);
  tft.setTextColor(ILI9341_WHITE);
  tft.print("LGore:   ");
  tft.setTextColor(ILI9341_RED);
  tft.print("RIGHT");
  tft.setTextColor(ILI9341_WHITE);
  tft.print("\nLDolje:  ");
  tft.setTextColor(ILI9341_RED);
  tft.print("LEFT");
  tft.setTextColor(ILI9341_WHITE);
  tft.print("\nLStisni: ");
  tft.setTextColor(ILI9341_RED);
  tft.print("BTN_B");
  tft.setTextColor(ILI9341_WHITE);
  tft.print("\n\nRGore:   ");
  tft.setTextColor(ILI9341_RED);
  tft.print("UP");
  tft.setTextColor(ILI9341_WHITE);
  tft.print("\nRDolje:  ");
  tft.setTextColor(ILI9341_RED);
  tft.print("DOWN");
  tft.setTextColor(ILI9341_WHITE);
  tft.print("\nRStisni: ");
  tft.setTextColor(ILI9341_RED);
  tft.print("BTN_A");
  tft.setTextColor(ILI9341_WHITE);
  tft.print("\n\nNazad:   ");
  tft.setTextColor(ILI9341_RED);
  tft.print("MENU");
}

void glavaLogic()
{
  glavaScreen();
  while(1)
  {
    delay(50);
    if (analogRead(BTN_LEFT_RIGHT) > 4000) // Lijeva tipka
    {
      uint8_t buff[20] = "GlavaLeft";
      sendMessage(buff);
      continue;
    }
    if (analogRead(BTN_LEFT_RIGHT) > 1800 and analogRead(BTN_LEFT_RIGHT) < 2000) // Desna tipka
    {
      uint8_t buff[20] = "GlavaRight";
      sendMessage(buff);
      continue;
    }
    if (digitalRead(BTN_MENU) == LOW)
    {
      connectedTIOSS();
      startMainMenu();
      return;
    }
  }
}

void rukeLogic()
{
  rukeScreen();
  while(1)
  {
    delay(50);
    if (analogRead(BTN_LEFT_RIGHT) > 4000) // Lijeva tipka
    {
      uint8_t buff[20] = "LArmDown";
      sendMessage(buff);
      continue;
    }
    if (analogRead(BTN_LEFT_RIGHT) > 1800 and analogRead(BTN_LEFT_RIGHT) < 2000) // Desna tipka
    {
      uint8_t buff[20] = "LArmUp";
      sendMessage(buff);
      continue;
    }
    if (analogRead(BTN_UP_DOWN) > 4000) // Gore tipka
    {
      uint8_t buff[20] = "RArmUp";
      sendMessage(buff);
      continue;
    }
    if (analogRead(BTN_UP_DOWN) > 1800 and analogRead(BTN_UP_DOWN) < 2000) // dolje tipka
    {
      uint8_t buff[20] = "RArmDown";
      sendMessage(buff);
      continue;
    }
    if (digitalRead(BTN_A) == LOW)
    {
      uint8_t buff[20] = "RArmHold";
      sendMessage(buff);
      continue;
    }
    if (digitalRead(BTN_B) == LOW)
    {
      uint8_t buff[20] = "LArmHold";
      sendMessage(buff);
      continue;
    }
    if (digitalRead(BTN_MENU) == LOW)
    {
      connectedTIOSS();
      startMainMenu();
      return;
    }
  }
}


void setup() 
{
  Serial.begin(115200); // pokreni serijsku vezu
  tft.begin(); // inicijalizacija zaslona
  connectToWiFi();
  connectedWIFI();
  Udp.begin(tioss_port); // Pokreni UDP
  findTIOSS();
  connectedTIOSS();
  initializePins();
  startMainMenu();
}

int menu_item = 0;

void loop() 
{
  delay(120);
  if (analogRead(BTN_UP_DOWN) > 4000) // Gore tipka
  {
    menu_item = abs((menu_item - 1) % 2);
    updateManinMenu(menu_item);
  }
  if (analogRead(BTN_UP_DOWN) > 1800 and analogRead(BTN_UP_DOWN) < 2000) // Dolje tipka
  {
    menu_item = abs((menu_item + 1) % 2);
    updateManinMenu(menu_item);
  }
  if (digitalRead(BTN_SELECT) == LOW)
  {
    if (menu_item == 0)
      glavaLogic();
    if (menu_item == 1)
      rukeLogic();
    menu_item = 0;
  }
}
