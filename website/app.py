from flask import Flask, render_template, jsonify, request
from gpiozero import LED

app = Flask(__name__)

# LED numberings
yellow = LED(5)
green = LED(19)
red = LED(6)
blue = LED(13)

mood_leds = {
    "hello": yellow,
    "love": red,
    "miss": blue,
    "proud": green
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/led/on", methods=["POST"])
def turn_led_on():
    mood = request.get_json().get("mood")
    led = mood_leds.get(mood)
    if led is None:
        return jsonify({"error": "unknown mood"}), 400

    led.on()
    return jsonify({"status": "on", "mood": mood})

if __name__ == "__main__":
    # use_reloader=False: stops Flask from starting the file twice,
    # which would try to grab the same GPIO pins twice
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)