from flask import Flask, Response
import cv2
import mss
import numpy as np

app = Flask(__name__)


def generate_frames():
    with mss.mss() as sct:
        # Define the monitor part to capture (full screen)
        monitor = sct.monitors[1]

        while True:
            try:
                # Capture the screen
                img = sct.grab(monitor)
                img_np = np.array(img)
                frame = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

                # Encode the frame in JPEG format
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    continue

                frame = buffer.tobytes()

                # Yield the output frame in byte format
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                print(f'Error: {e}')


@app.route('/video_feed')
def video_feed():
    try:
        return Response(generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return f'Error: {e}', 500


if __name__ == '__main__':
    print('Starting server...')
    app.run(host='0.0.0.0', port=5000)
