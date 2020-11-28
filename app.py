# app.py
import json

from flask import Flask, request, jsonify, url_for, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@app.route('/post/', methods=['POST'])
def post_something():
    if request.is_json:
        data = request.get_json()
        print(data)
        with open("./static/games.json", "w") as f:
            json.dump(data, indent=2, fp=f)
            f.close()
        return "JSON received", 200
    else:
        return jsonify({
            "ERROR": "Invalid post Data"
        }), 400

# A welcome message to test our server
@app.route('/')
def index():
    return redirect(url_for('static', filename="index.html"))


if __name__ == '__main__':
    app.run(debug=True)
