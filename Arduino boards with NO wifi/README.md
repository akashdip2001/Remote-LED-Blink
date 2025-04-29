Control the onboard LED of your **Arduino Nano** on **local Wi-Fi network (LAN)** , using my **laptop as a bridge** . This allows to send commands from **mobile phone browser** to toggle the LED.

---

## 🧰 What You Need:

* Arduino Nano (no Wi-Fi)
* USB cable to connect Nano to your laptop
* Laptop (connected to Wi-Fi or LAN)
* Mobile device (connected to the same Wi-Fi)
* Arduino IDE
* Python 3 installed on your laptop
* Python packages: `pyserial`, `flask`

---

## 📦 Step 1: Install Required Software

### 🟢 1.1 Install Arduino IDE

If you haven’t already, download from [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software)

### 🟢 1.2 Install Python 3

Get it from [https://www.python.org/downloads/](https://www.python.org/downloads/)

During install, check  **“Add Python to PATH”** .

### 🟢 1.3 Install Python packages

Open a terminal (CMD or PowerShell on Windows, or Terminal on macOS/Linux) and run:

```bash
pip install pyserial flask
```

---

## 💡 Step 2: Arduino Sketch

Open Arduino IDE, paste the code below, and upload it to your Nano:

```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == '1') {
      digitalWrite(LED_BUILTIN, HIGH);
    } else if (cmd == '0') {
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}
```

1. Select the correct board: **Tools > Board > Arduino Nano**
2. Select the correct port: **Tools > Port**
3. Click **Upload**

---

## 🔌 Step 3: Python Bridge Server

Create a file called `arduino_server.py` with the following code:

```python
from flask import Flask, request
import serial
import time

# Adjust the serial port below (e.g., COM3 for Windows or /dev/ttyUSB0 for Linux)
SERIAL_PORT = 'COM3'  # <-- CHANGE THIS!
BAUD_RATE = 9600

# Initialize serial connection
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  # wait for Arduino to reset

app = Flask(__name__)

@app.route('/led/<state>', methods=['GET'])
def control_led(state):
    if state == 'on':
        arduino.write(b'1')
        return 'LED turned ON'
    elif state == 'off':
        arduino.write(b'0')
        return 'LED turned OFF'
    else:
        return 'Invalid command', 400

if __name__ == '__main__':
    # Get IP address of your laptop and run the server
    app.run(host='0.0.0.0', port=5000)
```

### ⚠️ How to find COM port (Windows):

1. Open **Device Manager**
2. Look under **Ports (COM & LPT)** when the Arduino is plugged in.
3. Use that COM port in the script, e.g., `COM4`.

---

## 🌐 Step 4: Run the Server

In your terminal (same folder as your script), run:

```bash
python arduino_server.py
```

You should see:

```
Running on http://0.0.0.0:5000/
```

Now it’s serving requests over your local network!

---

## 📱 Step 5: Control From Your Mobile Phone

### 🔎 Find Your Laptop’s Local IP Address:

On Windows:

```bash
ipconfig
```

Look for something like `IPv4 Address: 192.168.x.x`

On macOS/Linux:

```bash
ifconfig
```

### 📲 On your mobile browser, open:

```
http://<YOUR_LAPTOP_IP>:5000/led/on   --> turns LED on
http://<YOUR_LAPTOP_IP>:5000/led/off  --> turns LED off
```

Example:

```
http://192.168.1.12:5000/led/on
```

---

## ✅ Done! Your Arduino LED is now controllable via your mobile device on the same Wi-Fi.

Would you like me to help you add a simple mobile-friendly web interface (buttons) instead of typing URLs manually?
