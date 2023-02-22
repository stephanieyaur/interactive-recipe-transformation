import sys
from bs4 import BeautifulSoup
import requests
import json


# returns list of ingredients, list of steps, servings, prep_time, cook_time, and total_time
# prep_time + cook_time = total_time
def main(url):
    # for now, have default url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find("h1")
    title = title.get_text()
    print(title)

    
    js = json.loads(soup.find('script', type='application/ld+json').text)
    ingredients = js[0]["recipeIngredient"]
    print(ingredients)
    steps = [step["text"] for step in js[0]["recipeInstructions"]]
    print(steps)

    # print(js)
    servings = js[0]["recipeYield"]

    # all time in minutes
    prep_time = convert_time(js[0]["prepTime"])
    cook_time = convert_time(js[0]["cookTime"])
    total_time = convert_time(js[0]["totalTime"])

    return ingredients, steps, prep_time, cook_time, total_time

# converts time to string containing just numerical value (in minutes)
# e.g. "PT15M" changes into "15"
def convert_time(input):
    output = input[2:-1]
    type = input[-1]
    if type == "M":
        print(output)
        return output



if __name__ == '__main__':
    # not sure if input is a url on command line
    if len(sys.argv) > 1:
        main(str(sys.argv[1]))
    else:
        # main("https://www.foodnetwork.com/recipes/ina-garten/meat-loaf-recipe-1921718")
        main("https://www.allrecipes.com/recipe/16354/easy-meatloaf/")