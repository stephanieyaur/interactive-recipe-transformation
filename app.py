import json

import flask
from flask_cors import CORS

import main
from question import get_response

app = flask.Flask(__name__)
CORS(app)

@app.route("/")
def home():
    response = flask.jsonify({"from": "BOT", "message": "The API works, congrats Stephie :D"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/api/recipe", methods=['POST'])
def process_recipe():
    request_data = flask.request.get_json()
    recipe_url = request_data["recipe_url"]
    # call recipe processor function
    title, ingredients, steps, prep_time, cook_time, total_time = main.process_recipe(recipe_url)
    tools = ["No tools"]
    last_user = ""
    last_bot = message = "What do you want to do? [1] Go over ingredients list or [2] Go over recipe steps."
    recipe_data = {"url": recipe_url, "title": title, "ingredients": ingredients, "steps": steps, "prep_time": prep_time, "cook_time": cook_time, "total_time": total_time, "tools": tools, "last_bot": last_bot, "last_user": last_user, "curr_step": -1}
    recipe_data = json.dumps(recipe_data)
    response = flask.jsonify({"message": message, "recipe_data": recipe_data})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/api/chat", methods=["POST"])
def process_message():
    request_data = flask.request.get_json()
    question, recipe_data = request_data["question"], json.loads(request_data["recipe_data"])
    answer = get_response(question, recipe_data)
    recipe_data = json.dumps(recipe_data)
    response = flask.jsonify({"message": answer, "recipe_data": recipe_data})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run()