import sys
from bs4 import BeautifulSoup
import requests
from question import *
import json
from dependency_parser import DependencyParser
import numpy as np

def process_recipe(url):
    title, ingredients, steps, prep_time, cook_time, total_time = get_recipe(url)

    # process steps
    str_steps = ". ".join(steps)
    str_steps = str_steps.replace(".", ";")
    steps = re.split(r';', str_steps)
    steps = [i.strip() for i in steps if i]

    # process step data using dependency parser
    dp = DependencyParser()
    steps_data = []
    for s in steps:
        steps_data.append(dp.parse_step(s))

    # get all tools
    total_tools = []
    for sd in steps_data:
        total_tools += sd.tools

    return title, ingredients, steps, prep_time, cook_time, total_time, steps_data, total_tools

# returns title, list of ingredients, list of steps, servings, prep_time, cook_time, and total_time
# prep_time + cook_time = total_time
def get_recipe(url):
    # dp = DependencyParser()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find("h1")
    title = title.get_text()

    # Ingredients
    js = json.loads(soup.find('script', type='application/ld+json').text)
    ingredients = js[0]["recipeIngredient"]
    # ingredients_data = dp.parse_ingredients(ingredients)


    # Steps
    steps = [step["text"] for step in js[0]["recipeInstructions"]]
    # steps_data = [dp.parse_step(step) for step in steps]

    servings = js[0]["recipeYield"]

    # all time in minutes
    prep_time = convert_time(js[0]["prepTime"])
    cook_time = convert_time(js[0]["cookTime"])
    total_time = convert_time(js[0]["totalTime"])

    return title, ingredients, steps, prep_time, cook_time, total_time

# converts time to string containing just numerical value (in minutes)
# e.g. "PT15M" changes into "15"
def convert_time(input):
    output = input[2:-1]
    type = input[-1]
    if type == "M":
        return output

if __name__ == "__main__":
    question = "yes"
    input = {
        "cook_time": "60",
        "ingredients": [
            "1.5 pounds ground beef",
            "1 egg",
            "1 onion, chopped",
            "1 cup milk",
            "1 cup dried bread crumbs",
            "salt and pepper to taste",
            "0.333 cup ketchup",
            "2 tablespoons brown sugar",
            "2 tablespoons prepared mustard"
        ],
        "last_bot": "What do you want to do? [1] Go over ingredients list or [2] Go over recipe steps.",
        "last_user": "",
        "prep_time": "15",
        "steps": [
            "Preheat the oven to 350 degrees F (175 degrees C)",
            "Lightly grease a 9x5-inch loaf pan",
            "Combine ground beef, onion, milk, bread crumbs and egg in a large bowl",
            "season with salt and pepper",
            "Transfer into prepared loaf pan",
            "Mix ketchup, brown sugar, and mustard together in a small bowl until well combined",
            "pour over meatloaf and spread it evenly over the top",
            "Bake in the preheated oven until no longer pink in the center, about 1 hour"
        ],
        "title": "\nEasy Meatloaf",
        "tools": [
            "No tools"
        ],
        "total_time": "75",
        "url": "https://www.allrecipes.com/recipe/16354/easy-meatloaf/"
    }
    response = get_response(question, input)