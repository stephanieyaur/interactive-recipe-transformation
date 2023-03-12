import json
import global_vars

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