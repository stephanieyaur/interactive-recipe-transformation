import sys
from bs4 import BeautifulSoup
import requests
from question import *
from global_vars import *
import json
from dependency_parser import DependencyParser
import numpy as np

def main():
    # not sure if input is a url on command line
    if len(sys.argv) > 1:
        url = str(sys.argv[1])
    else:
        # main("https://www.foodnetwork.com/recipes/ina-garten/meat-loaf-recipe-1921718")
        url = "https://www.allrecipes.com/recipe/16354/easy-meatloaf/"
    title, ingredients, steps, prep_time, cook_time, total_time = get_recipe(url)

    # process steps
    str_steps = ". ".join(steps)
    str_steps = str_steps.replace(".", ";")
    steps = re.split(r';', str_steps)
    steps = [i.strip() for i in steps if i]
    print("STEPS")
    print(steps)

    # set global vars
    global_vars.url = url
    global_vars.title = title
    global_vars.ingredients = ingredients
    global_vars.steps = steps
    global_vars.prep_time = prep_time
    global_vars.cook_time = cook_time
    global_vars.total_time = total_time
    question_parser("blah blah")

# returns title, list of ingredients, list of steps, servings, prep_time, cook_time, and total_time
# prep_time + cook_time = total_time
def get_recipe(url):
    dp = DependencyParser()
    # for now, have default url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find("h1")
    title = title.get_text()
    print(title)

    # Ingredients
    js = json.loads(soup.find('script', type='application/ld+json').text)
    ingredients = js[0]["recipeIngredient"]
    print(ingredients)
    ingredients_data = dp.parse_ingredients(ingredients)
    print(ingredients_data)


    # Steps
    steps = [step["text"] for step in js[0]["recipeInstructions"]]
    print(steps)
    steps_data = [dp.parse_step(step) for step in steps]
    print(steps_data)

    # print(js)
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
        print(output)
        return output



if __name__ == '__main__':
    main()