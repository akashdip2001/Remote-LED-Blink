<div style="display: flex; justify-content: center; gap: 2%; flex-wrap: wrap; margin-top: 20px;">
  <img src="https://github.com/user-attachments/assets/287fccdb-0a3b-4b70-951a-fc575f3a96ac" alt="Image 3" width="46%" />
  <img src="https://github.com/akashdip2001/ESP32-host-HTML-website/raw/main/img/ESP32-38%20PIN-DEVBOARD.png" alt="Image 4" width="46%" />
</div>

<details>
  <summary style="opacity: 0.85;"><b>more imges</b></summary><br>

<p float="center">
   <img src="https://github.com/user-attachments/assets/287fccdb-0a3b-4b70-951a-fc575f3a96ac" alt="Image 3" width="64%" />
   <img src="https://github.com/user-attachments/assets/3f316090-6ef6-4700-ba48-05222f9d6f6a" alt="Image 4" width="34%" />
</p>

<div style="display: flex; justify-content: center; gap: 2%; flex-wrap: wrap; margin-top: 20px;">
  <img src="https://github.com/user-attachments/assets/46d2b340-a9f3-40ac-bdf5-e576b9873ef2" alt="Image 3" width="50.5%" />
  <img src="https://github.com/user-attachments/assets/ddddd859-546c-4857-b9fa-d30870a2127d" alt="Image 4" width="48.5%" />
</div>

</details>
   
---

## 💡 NodeMCU LED Control as AP

- Update Board manager URLs for 8266 [Learn More - How to DO ?](https://github.com/akashdip2001/Arduino-IDE-setup)
- install all required Library

![img](https://github.com/user-attachments/assets/25cd8eaa-a72e-40df-87e2-e974afb050c4)
![Screenshot (337)](https://github.com/user-attachments/assets/f7555fd4-a409-4cbf-898a-4750eff02c7e)

![Screenshot (431)](https://github.com/user-attachments/assets/f112b1c1-e8cd-460d-8f14-a4251f1b52c5)

```cpp
#include <ESP8266WiFi.h> // for ESP 8266
// #include <WiFi.h> // for ESP 32

const char* ssid = "ESP8266_LED";
const char* password = "12345678";

WiFiServer server(80);
const int ledPin = 2;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH); // LED OFF

  WiFi.softAP(ssid, password);
  Serial.println("Access Point Started");
  Serial.print("IP address: ");
  Serial.println(WiFi.softAPIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (!client) return;

  Serial.println("New Client Connected");
  while (!client.available()) delay(1);

  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  // Handle ON/OFF buttons
  if (request.indexOf("/LED=ON") != -1) {
    digitalWrite(ledPin, LOW);
  } else if (request.indexOf("/LED=OFF") != -1) {
    digitalWrite(ledPin, HIGH);
  }

  // Handle blinking with params
  if (request.indexOf("/blink") != -1) {
    int speed = 500; // default
    int count = 5;   // default

    int spIndex = request.indexOf("speed=");
    int ctIndex = request.indexOf("count=");

    if (spIndex != -1) speed = request.substring(spIndex + 6, request.indexOf('&')).toInt();
    if (ctIndex != -1) count = request.substring(ctIndex + 6).toInt();

    Serial.print("Blinking "); Serial.print(count);
    Serial.print(" times at speed "); Serial.println(speed);

    for (int i = 0; i < count; i++) {
      digitalWrite(ledPin, LOW);
      delay(speed);
      digitalWrite(ledPin, HIGH);
      delay(speed);
    }
  }

  // HTML page with slider and input
  String html = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
  html += "<!DOCTYPE html><html><head><title>ESP8266 LED Control</title>";
  html += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">";
  html += "<style>";
  html += "body { background-color: #121212; color: #fff; font-family: Arial; text-align: center; padding: 20px; }";
  html += "h1 { font-size: 2em; margin-bottom: 20px; }";
  html += ".btn { background:#1f1f1f; border:2px solid #03dac5; color:white; padding:15px 30px;";
  html += "font-size:1.1em; border-radius:10px; margin:10px; display:inline-block; transition:0.3s; }";
  html += ".btn:hover { background:#03dac5; color:#121212; transform:scale(1.05); box-shadow:0 0 15px #03dac5; }";
  html += "form { margin-top: 30px; }";
  html += "input[type=number], input[type=range] { width: 80%; max-width: 300px; padding: 10px; margin: 10px auto; display: block; border-radius: 8px; border: none; font-size: 1em; }";
  html += "label { font-size: 1em; margin-top: 15px; display: block; }";
  html += "input[type=submit] { margin-top:20px; }";
  html += "</style></head><body>";
  html += "<h1>ESP8266 LED Control</h1>";
  html += "<a href=\"/LED=ON\"><div class=\"btn\">Turn ON</div></a>";
  html += "<a href=\"/LED=OFF\"><div class=\"btn\">Turn OFF</div></a>";

  // Form for blinking
  html += "<form action=\"/blink\" method=\"GET\">";
  html += "<label for=\"speed\">Blink Speed (ms)</label>";
  html += "<input type=\"range\" id=\"speed\" name=\"speed\" min=\"100\" max=\"1000\" value=\"500\" oninput=\"document.getElementById('sval').innerText = this.value\">";
  html += "<div>Speed: <span id=\"sval\">500</span> ms</div>";

  html += "<label for=\"count\">Blink Count</label>";
  html += "<input type=\"number\" id=\"count\" name=\"count\" min=\"1\" max=\"20\" value=\"5\">";

  html += "<input class=\"btn\" type=\"submit\" value=\"Blink LED\">";
  html += "</form>";

  html += "</body></html>";

  client.print(html);
  delay(1);
  Serial.println("Client Disconnected");
}
```

### 🟢 connect the `WIFI` and open the `mobile Browser` and type `192.168.4.1`

</br>

https://github.com/user-attachments/assets/385bdbcf-755d-4292-91d1-2c45f7a3d63a
