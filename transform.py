import json
import global_vars
from dependency_parser import DependencyParser

# Given a transformation, transform the recipe
def transformDriver(question):
    global_vars.transformations = {}
    option = ""
    if "non-vegetarian" in question or ("not" in question and "vegetarian" in question):
    # convert to non-vegetarian
        option = "non-vegetarian"
        transform("meat-substitutions")
    elif "vegetarian" in question:
    # convert to vegetarian
        option = "vegetarian"
        transform("veggie-substitutes")
    elif "non-healthy" in question or ("not" in question and "healthy" in question):
    # convert to non-healthy
        option = "unhealthy"
        transform("unhealthy substitutions")
    elif "healthy" in question:
    # convert to healthy
        option = "healthy"
        transform("healthy substitutions")
    elif "lactose" in question or "dairy" in question:
        option = "lactose-free"
        transform("lactose-free")
    elif "cuisine" in question or "chinese" in question or "kosher" in question:
        if "chinese" in question:
            option = "chinese"
            transform("to-chinese")
        elif "kosher" in question:
            if "meat" in question:
                option = "kosher meat"
                transform("to-kosher-meat")
            else:
                option = "kosher milk"
                transform("to-kosher-milk")
        else:
            print("Sorry, the only cuisines we are currently able to transform a recipe into are chinese and kosher. Please try one of those.")
    elif "double" in question:
        return change_amount(True)
    elif "half" in question:
        return change_amount(False)

# helper to sort database.json alphabetically
def sortDict(dict):
    sorted_dict = {key: value for key, value in sorted(dict.items())}
    return sorted_dict

def transform(option):
    with open('database.json') as json_file:
        tdict = json.load(json_file)
    for ingrObj in global_vars.parsed_ingredients:
        i = ingrObj.ingredient
        if i in tdict[option]:
            global_vars.transformations[i] = tdict[option][i]
    if global_vars.transformations != {}:
        # replace title, ingredients, and steps
        for k in global_vars.transformations:
            if k in global_vars.title.lower():
                global_vars.title.replace(k, global_vars.transformations[k])
        for k in global_vars.transformations:
            for i in range(len(global_vars.ingredients)):
                if k in global_vars.ingredients[i].lower():
                    global_vars.ingredients[i].replace(k, global_vars.transformations[k])
            global_vars.dp.parse_ingredients([global_vars.ingredients])
        for k in global_vars.transformations:
            for i in range(len(global_vars.steps)):
                if k in global_vars.steps[i].lower():
                    global_vars.steps[i].replace(k, global_vars.transformations[k])

def printTransformation(option):
    print("Done!")
    if option == "Doubled" or option == "Halved":
        print(option + " the recipe.")
        return
    if global_vars.transformations == {}:
        print("No transformations were needed to make the recipe " + option + ".")
    else:
        if option == "chinese" or option == "kosher":
            print("Converted the cuisine to " + option + ".")
        else:
            print("The recipe is now " + option + ".")
        output = "Substituted "
        for i in range(len(global_vars.transformations)):
            t = global_vars.transformations[i]
            if i == len(global_vars.transformations) -1:
                output += " and "
                output += t + " for " + global_vars.transformations[t] + "."
            else:
                output += t + " for " + global_vars.transformations[t] + ","
        print(output)
    return

def change_amount(isDouble):
    amount = 2
    if isDouble is False:
        amount = 0.5
    ingredient_steps = []
    for i in range(len(global_vars.ingredients)):
        ingredient = global_vars.parsed_ingredients[i].ingredient
        # get original and new amount
        original_amount = global_vars.parsed_ingredients[i].amount
        if original_amount is None:
            ingredient_steps.append(global_vars.ingredients[i])
            continue
        new_amount = float(original_amount) * amount
        new_amount = str(new_amount)

        # get original step
        ingredient_split = ingredient.split()
        original_step = global_vars.ingredients[i]

        # check if floating point is an int
        original_num, original_decimal = [int(part) for part in original_amount.split('.')]
        new_num, new_decimal = [int(part) for part in str(new_amount).split('.')]
        if new_decimal == 0:
            new_amount = str(new_num)

        # replace old amount with new amount
        if original_decimal == 0:
            ingredient_step = original_step.replace(str(original_num), new_amount)
        else:
            ingredient_step = original_step.replace(original_amount, new_amount)
        ingredient_steps.append(ingredient_step)
    return ingredient_steps