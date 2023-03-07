import flask

import main
from question import get_response

app = flask.Flask(__name__)

@app.route("/")
def home():
    return {"from": "BOT", "message": "The API works, congrats Stephie :D"}

@app.route("/api/recipe", methods=['POST'])
def process_recipe():
    request_data = flask.request.get_json()
    recipe_url = request_data["recipe_url"]
    # call recipe processor function
    title, ingredients, steps, prep_time, cook_time, total_time = main.process_recipe(recipe_url)
    return {"url": recipe_url, "title": title, "ingredients": ingredients, "steps": steps, "prep_time": prep_time, "cook_time": cook_time, "total_time": total_time}

@app.route("api/chat", methods=["POST"])
def process_message():
    request_data = flask.request.get_json()
    question, recipe_data = request_data["question"], request_data["recipe_data"]
    response = get_response(question, recipe_data)
    return {"message": response, "recipe_data": recipe_data}


if __name__ == '__main__':
    app.run()