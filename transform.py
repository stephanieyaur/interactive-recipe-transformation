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
        transform("meat-substitutions", option)
    elif "vegetarian" in question:
    # convert to vegetarian
        option = "vegetarian"
        transform("veggie-substitutes", option)
    elif "non-healthy" in question or ("not" in question and "healthy" in question):
    # convert to non-healthy
        option = "unhealthy"
        transform("unhealthy-substitutions", option)
    elif "healthy" in question:
    # convert to healthy
        option = "healthy"
        transform("healthy-substitutions", option)
    elif "lactose" in question or "dairy" in question:
        option = "lactose-free"
        transform("lactose-free", option)
    elif "cuisine" in question or "chinese" in question or "kosher" in question:
        if "chinese" in question:
            option = "chinese"
            transform("to-chinese", option)
        elif "kosher" in question:
            option = "kosher"
            transform("to-kosher", option)
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

def transform(option, strOption):
    f = open("./database.json")
    tdict = json.load(f)
    # replace title, ingredients, and steps
    for k in tdict[option]:
        if k in global_vars.title.lower():
            global_vars.title = global_vars.title.lower().replace(k, tdict[option][k])
            global_vars.title = global_vars.title.title()
            global_vars.transformations[k] = tdict[option][k]
    for k in tdict[option]:
        for i in range(len(global_vars.ingredients)):
            if k in global_vars.ingredients[i].lower():
                if (k != "cream" or k != "cheese") or (k == "cream" or k == "cheese") and "cream cheese" not in global_vars.ingredients[i].lower():
                    global_vars.ingredients[i] = global_vars.ingredients[i].replace(k, tdict[option][k])
                    global_vars.transformations[k] = tdict[option][k]
        global_vars.dp.parse_ingredients(global_vars.ingredients)
    for k in tdict[option]:
        for i in range(len(global_vars.steps)):
            if k in global_vars.steps[i].lower():
                global_vars.steps[i] = global_vars.steps[i].replace(k, tdict[option][k])
                global_vars.transformations[k] = tdict[option][k]
    if global_vars.transformations != {}:
        global_vars.title += " (" + strOption + ")"

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
        listTransformations = list(global_vars.transformations.keys())
        for i in range(len(listTransformations)):
            t = listTransformations[i]
            if i == len(global_vars.transformations) -1:
                if output != "Substituted ":
                    output += "and "
                output += t + " for " + global_vars.transformations[t] + "."
            else:
                output += t + " for " + global_vars.transformations[t] + ", "
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