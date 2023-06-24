from flask import Flask, render_template, request, jsonify, Response
import cv2 as cv


app = Flask(__name__)

def one():
    print("one")


def two():
    print("two")

def three():
    print("three")


def generate_frames():
    camera = cv.VideoCapture(0)

    # width = 1280
    # height = 720
    # camera.set(cv.CAP_PROP_FRAME_WIDTH, width)
    # camera.set(cv.CAP_PROP_FRAME_HEIGHT, height)



    while True:
            
        ## read the camera frame
        success,frame=camera.read()

        # frame = cv.Canny(frame, 200, 50)
        
        if not success:
            break
        else:
            ret,buffer=cv.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/button', methods=['POST'])
def test():
    data = request.get_json()

    print(data)

    if data:
        button = data.get('button')
        print(button)

        if (button == '1'):
            one()
        elif (button == '2'):
            two()
        else:
            three()

        response = {"message": "JSON recieved"}
    else:
        response = {"message": "JSON not recieved"}

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
