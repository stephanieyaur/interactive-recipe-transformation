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
            t["index"] = token.i
            tokens[token.text] = t
        return tokens

    # Returns a dictionary of ingredient -> IngredientData given an array of all ingredients
    def parse_ingredients(self, ingredientsArr):

        def dfs_amount(token):
            if not token or token["part-of-speech"] != "nummod":
                if not token["text"] or token["part-of-speech"] in ["ROOT"]:
                    return ""
                tokenName = token["text"]
                token["text"] = None
                return tokenName
            else:
                tokenName = token["text"]
                token["text"] = None
                headName = token["head"].text
                return tokenName + " " + dfs_amount(tokens[headName])

        def dfs_ingredient_root(token):
            if (not token["text"] or token["part-of-speech"] not in ["compound", "ROOT", "cc", "conj", "amod"]):
                return ""
            else:
                childName = token["children"][0].text if len(token["children"]) > 0 else None #assume only 1 child for now
                tokenName = token["text"]
                tokenIndex = token["index"]
                token["text"] = None
                prev = dfs_ingredient_root(tokens[childName]) if childName else ""
                if prev != "":
                    if tokenIndex > tokens[childName]["index"]:
                        return prev + " " + tokenName
                    else:
                        return tokenName + " " + prev
                else:
                    return tokenName

        def dfs_ingredient_not_root(token):
            if (not token["text"] or token["part-of-speech"] not in ["compound", "amod", "dobj", "nsubj", "cc", "conj"]):
                return ""
            else:
                tokenName = token["text"]
                tokenIndex = token["index"]
                token["text"] = None
                childName = token["children"][0].text if len(token["children"]) > 0 else None# assume only 1 child for now
                prev = dfs_ingredient_not_root(tokens[childName]) if childName else ""
                if prev != "":
                    if tokenIndex > tokens[childName]["index"]:
                        return prev + " " + tokenName
                    else:
                        return tokenName + " " + prev
                else:
                    return tokenName

        def ingredient_parameters(tokens):
            parameters = ""
            for tname in tokens:
                if tokens[tname]["text"] != None and tokens[tname]["part-of-speech"] != "punct":
                    parameters += tokens[tname]["text"] + " "
            return parameters.strip()


        ingredients_data = {}
        for i in ingredientsArr:
            tokens = self.tokenize(i)
            id = IngredientData()
            rootName = None
            for tname in tokens:
                token = tokens[tname]
                if not token["text"]:
                    continue
                elif token["part-of-speech"] == "nummod":
                    id.amount = dfs_amount(token)
                if token["part-of-speech"] in ["dobj", "nsubj"]:
                    id.ingredient = dfs_ingredient_not_root(token)
                elif token["part-of-speech"] == "ROOT":
                    rootName = token["text"]
            if id.ingredient == None:
                id.ingredient = dfs_ingredient_root(tokens[rootName])
            id.parameters = ingredient_parameters(tokens)
            ingredients_data[id.ingredient] = id
        return ingredients_data

    # Returns a StepData object given a step
    def parse_step(self, stepArr):
        # TODO
        return
