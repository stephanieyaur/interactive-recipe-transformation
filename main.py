import sys
from bs4 import BeautifulSoup
import requests

import global_vars
from question import *
import json
from dependency_parser import DependencyParser
import numpy as np
import validators

def main():
    print("Hi, I'm Chef Bot! I'm an interactive chatbot that can walk through recipes from AllRecipes.com.")
    while True:
        print("First, type in a recipe url! ex: https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/")
        url = input()
        if not validators.url(url) or not (url.startswith("https://www.allrecipes.com/recipe") or url.startswith("http://www.allrecipes.com/recipe")):
            print("I'm sorry, that's not a valid allrecipes.com recipe url. Please try again.")
        else:
            break
    print("Let me process that recipe...please wait a moment")
    process_recipe(url)
    print("Great choice! You've decided to make " + global_vars.title + ".")
    print("What do you want to do? [1] Go over ingredients list [2] Go over recipe steps [3] Transform the recipe")
    while True:
        question = input()
        response = get_response(question)
        if response:
            print(response)





def process_recipe(url):
    title, ingredients, steps, prep_time, cook_time, total_time = get_recipe(url)

    global_vars.title = title
    global_vars.ingredients = ingredients
    global_vars.steps = steps
    global_vars.prep_time = prep_time
    global_vars.cook_time = cook_time
    global_vars.total_time = total_time
    global_vars.url = url

    # process steps
    str_steps = ". ".join(steps)
    str_steps = str_steps.replace(".", ";")
    steps = re.split(r';', str_steps)
    steps = [i.strip() for i in steps if i]

    # process step data using dependency parser
    dp = DependencyParser()
    for s in steps:
        sd = dp.parse_step(s)
        global_vars.tools += sd.tools
        global_vars.parsed_steps.append(sd)
    return

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
    main()