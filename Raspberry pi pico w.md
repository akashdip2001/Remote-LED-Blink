# Remote LED Blink

# Raspberry pi pico w

https://github.com/user-attachments/assets/ffb6bfb2-7357-4734-9d73-9ed910a507b2

```cpp
#include <WiFi.h>

const char* ssid = "PicoW_AP";
const char* password = "Mahapatra";

// Create a web server on port 80
WiFiServer server(80);
const int LED_PIN = LED_BUILTIN;  // Use the built-in LED macro

// Embedded HTML page stored in program memory
const char html_page[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
    <title>Pico W Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        h1 { color: #3498db; }
        .button { padding: 15px 30px; font-size: 20px; margin: 10px; cursor: pointer; }
        .on { background-color: #2ecc71; color: white; }
        .off { background-color: #e74c3c; color: white; }
    </style>
</head>
<body>
    <h1>Raspberry Pi Pico W - LED Control</h1>
    <p><button class="button on" onclick="toggleLED('ON')">Turn LED ON</button></p>
    <p><button class="button off" onclick="toggleLED('OFF')">Turn LED OFF</button></p>
    <script>
        function toggleLED(state) {
            fetch("/led?state=" + state);
        }
    </script>
</body>
</html>
)rawliteral";

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Set fixed IP configuration for the access point
  IPAddress local_ip(192, 168, 4, 1);
  IPAddress gateway(192, 168, 4, 1);
  IPAddress subnet(255, 255, 255, 0);
  
  if(WiFi.softAPConfig(local_ip, gateway, subnet)){
      Serial.println("AP Fixed IP configuration set successfully.");
  } else {
      Serial.println("Failed to configure AP with fixed IP.");
  }

  Serial.println("Starting WiFi Access Point...");
  WiFi.softAP(ssid, password);
  Serial.println("Access Point Started!");
  Serial.print("AP IP Address: ");
  Serial.println(WiFi.softAPIP());
  
  server.begin();
}

void loop() {
  // Use accept() instead of available() to remove deprecation warnings
  WiFiClient client = server.accept();
  if (!client) return;

  Serial.print("Client connected: ");
  Serial.println(client.remoteIP());

  String request = client.readStringUntil('\r');
  Serial.print("Request: ");
  Serial.println(request);
  client.flush();

  // Toggle LED based on the request URL
  if (request.indexOf("/led?state=ON") != -1) {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("LED turned ON");
  } else if (request.indexOf("/led?state=OFF") != -1) {
    digitalWrite(LED_PIN, LOW);
    Serial.println("LED turned OFF");
  }

  // Send the HTML page to the client
  client.print("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n");
  client.print(html_page);
  client.stop();
  
  Serial.println("Client disconnected.");
}
```

<img align="right" alt="Raspberry pi" width="400" src="https://github.com/user-attachments/assets/355b4301-c3f6-4ab1-b2c5-81b381cf2bac"> 

</br>

### If the Built-in LED Doesn’t Work:
- **External LED Setup:**  
  Connect an LED (with a ~220Ω resistor in series) to a GPIO pin (e.g., GP15). Change the definition at the top:
  ```cpp
  const int LED_PIN = 15;  // Use GP15 for external LED
  ```
- Then wire your external LED’s anode to GP15 and its cathode (through the resistor) to GND.

</br>

- The log shows the LED commands are being received.
- The Pico W’s onboard LED may not be directly controllable.  
- also Use `LED_BUILTIN` (or an external LED) for visual indication.
