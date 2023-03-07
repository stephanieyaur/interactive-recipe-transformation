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

    return title, ingredients, steps, prep_time, cook_time, total_time

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