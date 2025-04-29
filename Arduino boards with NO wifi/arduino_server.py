from flask import Flask, request, render_template_string, redirect, url_for
import serial
import time

# Arduino serial configuration
SERIAL_PORT = 'COM9' # check the port and change it
BAUD_RATE = 9600

# Initialize serial connection
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  # Wait for Arduino to reset

# Flask app setup
app = Flask(__name__)
led_status = "OFF"  # Global status variable

# HTML template with dynamic message support
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Arduino LED Control</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { background-color: #121212; color: #fff; font-family: Arial; text-align: center; padding: 20px; }
    h1 { font-size: 2em; margin-bottom: 20px; }
    .btn { background:#1f1f1f; border:2px solid #03dac5; color:white; padding:15px 30px;
           font-size:1.1em; border-radius:10px; margin:10px; display:inline-block; transition:0.3s; text-decoration: none; }
    .btn:hover { background:#03dac5; color:#121212; transform:scale(1.05); box-shadow:0 0 15px #03dac5; }
    form { margin-top: 30px; }
    input[type=number], input[type=range] { width: 80%; max-width: 300px; padding: 10px; margin: 10px auto;
           display: block; border-radius: 8px; border: none; font-size: 1em; }
    label { font-size: 1em; margin-top: 15px; display: block; }
    input[type=submit] { margin-top:20px; }
    .status { margin-top: 20px; font-size: 1.2em; color: #03dac5; }
  </style>
</head>
<body>
  <h1>Arduino LED Control</h1>
  <a href="/led/on" class="btn">Turn ON</a>
  <a href="/led/off" class="btn">Turn OFF</a>

  <form action="/blink" method="get">
    <label for="speed">Blink Speed (ms)</label>
    <input type="range" id="speed" name="speed" min="100" max="1000" value="500"
           oninput="document.getElementById('sval').innerText = this.value">
    <div>Speed: <span id="sval">500</span> ms</div>

    <label for="count">Blink Count</label>
    <input type="number" id="count" name="count" min="1" max="20" value="5">

    <input class="btn" type="submit" value="Blink LED">
  </form>

  {% if message %}
    <div class="status">{{ message }}</div>
  {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    message = request.args.get("message", "")
    return render_template_string(HTML_PAGE, message=message)

@app.route('/led/<state>')
def control_led(state):
    global led_status
    if state == 'on':
        arduino.write(b'1')
        led_status = "ON"
        return redirect(url_for('home', message="LED turned ON"))
    elif state == 'off':
        arduino.write(b'0')
        led_status = "OFF"
        return redirect(url_for('home', message="LED turned OFF"))
    else:
        return redirect(url_for('home', message="Invalid LED state"))

@app.route('/blink')
def blink_led():
    try:
        count = int(request.args.get('count', 5))
        speed = int(request.args.get('speed', 500))
        for _ in range(count):
            arduino.write(b'1')
            time.sleep(speed / 1000.0)
            arduino.write(b'0')
            time.sleep(speed / 1000.0)
        return redirect(url_for('home', message=f"LED blinked {count} times at {speed}ms"))
    except Exception as e:
        return redirect(url_for('home', message="Invalid parameters"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
