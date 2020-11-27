# app.py
from flask import Flask, request, jsonify, url_for, redirect, session
from flask_socketio import SocketIO, send
import json
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = '9ce92082e8'
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("message")
def handle_message(msg):
    print("message: " + msg)
    send(msg, broadcast=True)


@socketio.on('connect')
def u_connect(user):
    if user is dict:
        print(user['username'])
        print(user['id'])
        print(user['location'])
    else:
        send(400)


def push_json():
    j_data = request.json
    f_data = {}
    f_size = os.path.getsize("static/games.json")
    if f_size is 0:
        with open("static/games.json", "w") as f:
            json.dump(j_data, f, indent=2)
            f.close()
    else:
        with open("static/games.json") as f:
            f_data = json.load(f)
            f.close()
        with open("static/games.json", "w") as f:
            for i in f_data:
                print(i)
                for n in j_data:
                    print(n)
                    if n is i:
                        for x in f_data.values():
                            for y in j_data.values():
                                print(x["blue"])
                                print(x["white"])
                                if x["blue"] is not y["blue"]:
                                    x["blue"] = y["blue"]
                                if x["white"] is not y["white"]:
                                    x["white"] = y["white"]
            else:
                f_data.update(j_data)
                json.dump(f_data, f, indent=2)
                f.close()


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    print(request.json)
    data = request.json
    # You can add the test cases you made in the previous function, but in our case here you are just testing the
    # POST functionality
    if data:
        push_json()
        return redirect(url_for('static', filename="index.html"))
    else:
        return jsonify({
            "ERROR": "Invalid post Data"
        })

# A welcome message to test our server
@app.route('/')
def index():
    return redirect(url_for('static', filename="index.html"))


if __name__ == '__main__':
    socketio.run(app)
