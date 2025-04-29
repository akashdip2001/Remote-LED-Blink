![STM32](https://github.com/user-attachments/assets/95708b30-d4b3-4955-b88f-8f2e27a48233)

Using an **STM32 without built-in Wi-Fi**, and want to control an LED via **PC’s LAN**, like with [`Arduino + Flask setup`](https://github.com/akashdip2001/Remote-LED-Blink/tree/main/Arduino%20boards%20with%20NO%20wifi), I acn do the exact same thing — just using STM32's serial (UART) to communicate with the Python Flask server.

---

<details>
  <summary style="opacity: 0.85;"><b>🟢 using STM32CubeIDE</b></summary><br>

---

### 🧰 What You Need:
- STM32 board (e.g., STM32F103C8T6 or similar)
- USB to Serial (ST-Link or UART to USB)
- USB cable (to connect to PC)
- LED connected to a GPIO pin (or use onboard LED if available)
- Python + Flask running on the PC to act as a bridge over USB (same as with Arduino)

## 🔌 1. STM32 Firmware (Baremetal or HAL)

### ✅ STM32 Code (for STM32CubeIDE or PlatformIO)

This version expects `'1'` or `'0'` from the PC via USB (UART). LED turns ON or OFF accordingly.

#### For STM32CubeIDE (HAL library):
```c
#include "main.h"
#include <string.h>

UART_HandleTypeDef huart1;
#define LED_PIN GPIO_PIN_13
#define LED_PORT GPIOC

void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART1_UART_Init(void);

uint8_t rx_data;

int main(void)
{
  HAL_Init();
  SystemClock_Config();
  MX_GPIO_Init();
  MX_USART1_UART_Init();

  while (1)
  {
    if (HAL_UART_Receive(&huart1, &rx_data, 1, HAL_MAX_DELAY) == HAL_OK)
    {
      if (rx_data == '1')
        HAL_GPIO_WritePin(LED_PORT, LED_PIN, GPIO_PIN_RESET); // ON (PC13 is active-low)
      else if (rx_data == '0')
        HAL_GPIO_WritePin(LED_PORT, LED_PIN, GPIO_PIN_SET);   // OFF
    }
  }
}
```

> ⚠️ STM32F103 “Blue Pill” has onboard LED on **PC13**. It’s active LOW!

#### Initialize UART in `MX_USART1_UART_Init()`:
```c
huart1.Instance = USART1;
huart1.Init.BaudRate = 9600;
huart1.Init.WordLength = UART_WORDLENGTH_8B;
huart1.Init.StopBits = UART_STOPBITS_1;
huart1.Init.Parity = UART_PARITY_NONE;
huart1.Init.Mode = UART_MODE_TX_RX;
huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
huart1.Init.OverSampling = UART_OVERSAMPLING_16;
HAL_UART_Init(&huart1);
```

#### GPIO PC13 Initialization (already in CubeMX):
- Set PC13 as Output Push-Pull
- Set to High (LED off)

---

## 💻 2. Python + Flask App (on PC) - Same as Arduino Version

Use the **same Flask app** you used for Arduino — just change the serial port to the STM32's COM port (e.g., `COM5`, `COM9`, etc.)

```python
# Replace SERIAL_PORT with your STM32's COM port
SERIAL_PORT = 'COM9'  # Change as needed
BAUD_RATE = 9600
```

> ✅ The PC sends `'1'` or `'0'` to STM32 over USB, and STM32 turns the LED on/off.

---

</details>

---

# 🟢 using ARDUINO IDE

---

## ✅ PART 1: Set Up STM32 in Arduino IDE (for USB Serial)

### 🔧 What You Need:
- STM32 board (e.g., **Blue Pill – STM32F103C8T6**)
- USB to Serial (FTDI or ST-Link V2 programmer)
- Arduino IDE with STM32 board support

---

### 🔌 Step 1: Install STM32 Board Support in Arduino IDE

![Screenshot (432)](https://github.com/user-attachments/assets/121e5f61-1a6f-45b9-a1e7-e767d8d7d5d0)
![Screenshot (433)](https://github.com/user-attachments/assets/ccd28543-351a-4304-b712-ad052261f79c)

1. Go to **File > Preferences**
2. In “Additional Board URLs”, add:
   ```
   https://github.com/stm32duino/BoardManagerFiles/raw/main/package_stmicroelectronics_index.json
   ```
3. Go to **Tools > Board > Board Manager**
4. Search for **STM32** and install **STM32 MCU based boards**

---

### ⚙️ Step 2: Select Board and Port

![Screenshot (436)](https://github.com/user-attachments/assets/13c4190f-2c93-41f4-8968-abacdc818d85)

- **Board**: `Generic STM32F103C series`
- **Variant**: `STM32F103C8 (20k RAM, 64k Flash)`
- **Upload method**: `STM32CubeProgrammer (Serial)` or `STLink`
- **Port**: Select the correct COM port
- **Tools > USB Support**: Optional: set to `CDC (Generic Serial)` if using USB directly

---

### 🧠 Step 3: Upload This Code (LED via Serial)

```cpp
// For STM32 Blue Pill (onboard LED is PC13)
#define LED_PIN PC13

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH); // Turn off (LED is active-low)
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '1') {
      digitalWrite(LED_PIN, LOW);  // Turn LED on
    } else if (c == '0') {
      digitalWrite(LED_PIN, HIGH); // Turn LED off
    }
  }
}
```

![Screenshot (437)](https://github.com/user-attachments/assets/31cdaae5-6144-4ca9-90f5-163da973c982)

Great news: you've already selected the correct board in Arduino IDE.

**You chose:**  
✅ `Generic STM32F1 series`  
➡️ Then inside that, you selected `BluePill F103C8 (32K)` — this **matches** your board (GD32F103C8T6 is a clone of STM32F103C8T6).

---

### ❗ Issue: “USB device not recognized”

This error usually means **your board doesn’t have a USB bootloader** installed, or the **USB-to-Serial chip driver is missing or unsupported**. The GD32 clone boards are especially known for this.

<details>
  <summary style="opacity: 0.85;"><b>Solutions 🔵</b></summary><br>

---

### 🔵 Solution 1: Use USB to Serial (UART) for uploading  
Use an **external USB-to-Serial adapter** (like an FTDI module) and connect:

| FTDI Adapter | STM32 (Blue Pill) |
|--------------|-------------------|
| TX           | A10 (RX)          |
| RX           | A9  (TX)          |
| GND          | GND               |
| 3.3V         | 3.3V              |

#### Also, set BOOT0 to 1, BOOT1 to 0:
- BOOT0 jumper to `1` (HIGH)
- BOOT1 jumper to `0` (LOW)
This puts the board in **Serial Bootloader mode**.

Then, in Arduino IDE:
- **Upload method**: choose `"Serial"` (not SWD)
- **Port**: select the COM port for the FTDI adapter
- Click **Upload**

---

### 🔵 Solution 2: Use ST-Link (recommended)
If you have an **ST-Link V2** programmer (cheap and easy), you can upload via SWD:

**Connect:**

| ST-Link | STM32 |
|---------|-------|
| SWDIO   | SWDIO |
| SWCLK   | SWCLK |
| GND     | GND   |
| 3.3V    | 3.3V  |

Then:
- In Arduino IDE, set:
  - **Upload method:** `"STLink"`
  - **Board part number:** `"BluePill F103C8 (32k)"`
- Upload your sketch

🔴🔴🔴🔴🔴

</details>

---

## ✅ PART 2: Python Flask Code in VS Code

Your Python Flask code in VS Code stays the same [complete `code link`](https://github.com/akashdip2001/Remote-LED-Blink/blob/main/Arduino%20boards%20with%20NO%20wifi/arduino_server.py) — just update the **COM port**:

```python
SERIAL_PORT = 'COM9'  # Change this to match your STM32 serial port
BAUD_RATE = 9600
```

Then run it:

```bash
python arduino_server.py
```

Access it from your phone or browser:
```
http://<your-laptop-ip>:5000
```

---

## ✅ OPTIONAL: Test Serial Before Flask

You can test serial with a quick Python script:

```python
import serial
arduino = serial.Serial('COM9', 9600)
arduino.write(b'1')  # Turn LED on
```

---
