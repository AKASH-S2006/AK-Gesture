import os
from flask import Flask, render_template, Response, request, jsonify
from camera import VideoCamera

app = Flask(__name__)

camera = VideoCamera()


@app.route("/")
def index():
    return render_template("index.html")


def generate_frames():
    while True:
        frame = camera.get_frame()

        if frame is None:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )
@app.route("/set_mode", methods=["POST"])
def set_mode():

    data = request.get_json()

    mode = data.get("mode")

    camera.engine.mode = mode

    print(f"\nCurrent Mode : {mode}\n")

    return jsonify({

        "success": True,
        "mode": mode

    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)