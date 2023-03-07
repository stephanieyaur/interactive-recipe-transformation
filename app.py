import flask

app = flask.Flask(__name__)

@app.route("/")
def home():
    return {"from": "BOT", "message": "The API works, congrats Stephie :D"}

if __name__ == '__main__':
    app.run()