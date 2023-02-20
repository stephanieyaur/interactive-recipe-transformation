import sys
from bs4 import BeautifulSoup
import requests
import json
import re


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

    # will return array of ingredients and steps

if __name__ == '__main__':
    # not sure if input is a url on command line
    if len(sys.argv) > 1:
        main(str(sys.argv[1]))
    else:
        # main("https://www.foodnetwork.com/recipes/ina-garten/meat-loaf-recipe-1921718")
        main("https://www.allrecipes.com/recipe/16354/easy-meatloaf/")