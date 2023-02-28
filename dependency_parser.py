# Dependency parser takes in a step and finds the cooking action, ingredients, tools/utensils, parameters (time/temp)

import spacy

class StepData:
    def __init__(self):
        self.cookingAction = None
        self.actionObjects = [] #could be ingredients or tool like oven
        self.parameters = [] #could be utensils or parameters of action

class IngredientData:
    def __init__(self):
        self.ingredient = None
        self.amount = None
        self.parameters = None

class DependencyParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    # Returns a dictionary of word -> token (incl part of speech, head, and children)
    def tokenize(self, string):
        # attempt 1: use existing dependency parser
        parsed = self.nlp(string)
        tokens = {}
        for token in parsed:
            t = {}
            t["text"] = token.text
            t["part-of-speech"] = token.dep_
            t["head"] = token.head
            t["children"] = [child for child in token.children]
            tokens[token.text] = t
        return tokens

    # Returns a dictionary of ingredient -> IngredientData given an array of all ingredients
    def parse_ingredients(self, ingredientsArr):

        def dfs_amount(token):
            if token["part-of-speech"] != "nummod":
                if token["part-of-speech"] == "ROOT":
                    return ""
                return token["text"]
            else:
                headName = token["head"].text
                return token["text"] + " " + dfs_amount(tokens[headName])

        def dfs_ingredient(token):
            if (token["part-of-speech"] != "compound" and token["part-of-speech"] != "ROOT") or token["part-of-speech"] == "compound" and tokens[token["children"][0].text]["part-of-speech"] == "nummod":
                return ""
            else:
                childName = token["children"][0].text #assume only 1 child for now
                prev = dfs_ingredient(tokens[childName])
                if prev != "":
                    return prev + " " + token["text"]
                else:
                    return token["text"]


        ingredients_data = {}
        for i in ingredientsArr:
            tokens = self.tokenize(i)
            id = IngredientData()
            for tname in tokens:
                token = tokens[tname]
                if token["part-of-speech"] == "nummod":
                    id.amount = dfs_amount(token)
                elif token["part-of-speech"] == "ROOT":
                    id.ingredient = dfs_ingredient(token)
            ingredients_data[id.ingredient] = id
        return ingredients_data

    # Returns a StepData object given a step
    def parse_step(self, stepArr):
        # TODO
        return
