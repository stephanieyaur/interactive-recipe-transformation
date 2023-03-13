import json
import global_vars
from dependency_parser import DependencyParser

# Given a transformation, transform the recipe
def transformDriver(question):
    with open('database.json') as json_file:
        tdict = json.load(json_file)
    if "non-vegetarian" in question or ("not" in question and "vegetarian" in question):
    # convert to non-vegetarian
        return
    elif "vegetarian" in question:
    # convert to vegetarian
        return
    elif "non-healthy" in question or ("not" in question and "healthy" in question):
    # convert to non-healthy
        return
    elif "healthy" in question:
    # convert to healthy
        return
    elif "cuisine" in question or "chinese" in question or "kosher" in question:
        if "chinese" in question:
        # convert to chinese
            return
        elif "kosher" in question:
        # convert to kosher
            return
        else:
            print("Sorry, the only cuisines we are currently able to transform a recipe into are chinese and kosher. Please try one of those.")
    elif "double" in question:
        print("original ingredients")
        print(global_vars.ingredients)
        ingredient_steps = []
        for ingredient in global_vars.parsed_ingredients:
            # get ingredient_step
            original_amount = global_vars.parsed_ingredients[ingredient].amount
            print(type(original_amount))
            new_amount = int(original_amount) * 2
            ingredient_split = ingredient.split()
            original_step = [step for step in global_vars.ingredients if all(part in step for part in ingredient_split)][0]
            ingredient_step = original_step.replace(original_amount, str(new_amount))
            ingredient_steps.append(ingredient_step)
        print("new ingredients")
        print(ingredient_steps)
        return ingredient_steps
    elif "half" in question:
        print("original ingredients")
        print(global_vars.ingredients)
        ingredient_steps = []
        for ingredient in global_vars.parsed_ingredients:
            # get ingredient_step
            original_amount = global_vars.parsed_ingredients[ingredient].amount
            print(type(original_amount))
            new_amount = float(original_amount) / 2
            ingredient_split = ingredient.split()
            original_step = [step for step in global_vars.ingredients if all(part in step for part in ingredient_split)][0]
            ingredient_step = original_step.replace(original_amount, str(new_amount))
            ingredient_steps.append(ingredient_step)
        print("new ingredients")
        print(ingredient_steps)
        return ingredient_steps

# helper to sort database.json alphabetically
def sortDict(dict):
    sorted_dict = {key: value for key, value in sorted(dict.items())}
    return sorted_dict
