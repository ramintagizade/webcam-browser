from flask import Flask,Response
from flask import render_template
from webcam import RedisClient, WebCam

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

def get_image():
    redis = RedisClient()
    while(True):
        image = redis.getImg()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

@app.route("/camera")
def start():
    webCam = WebCam()
    webCam.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_stream")
def video_stream():
    return Response(get_image(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()



