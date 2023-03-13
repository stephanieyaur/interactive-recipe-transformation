# Dependency parser takes in a step and finds the cooking action, ingredients, tools/utensils, parameters (time/temp)

from json import tool
import spacy
import type_checker

class StepData:
    def __init__(self):
        self.cookingAction = []
        self.ingredients = [] #could be ingredients or tool liks
        self.tools = [] #could be utensils or appliances - "oven", "medium sized saucepan"
        self.parameters = [] #action parameters "fast", "until creamy" etc.


    def __repr__(self) -> str:
        return "\nCooking action: " + str(self.cookingAction) + "\ningredients: " + str(self.ingredients) + "\ntools: " + str(self.tools) + "\nparameters: " + str(self.parameters)

class IngredientData:
    def __init__(self):
        self.ingredient = None
        self.amount = None
        self.measurement = None
        self.parameters = None

    def __repr__(self) -> str:
        if self.parameters:
            pa = self.parameters
        else:
            pa = ""

        
        return "\n\ningredient: " + str(self.ingredient) + "\namount: " + str(self.amount) + "\nparameters: " + pa

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

    def chunker(self,text,step):
        doc = self.nlp(step)
        for chunk in doc.noun_chunks:
            if text in str(chunk):
                return str(chunk)
        return text

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
        count = 0
        for i in ingredientsArr:
            i = i.split(",")[0]
            tokens = self.tokenize(i)
            id = IngredientData()
            rootName = None
            for tname in tokens:
                token = tokens[tname]
                if not token["text"]:
                    continue
                elif token["part-of-speech"] == "nummod":
                    amountMeasurement = dfs_amount(token)
                    id.amount = str(float(amountMeasurement.split()[0]))
                    id.measurement = amountMeasurement[1:]
                if token["part-of-speech"] in ["dobj", "nsubj"]:
                    id.ingredient = dfs_ingredient_not_root(token)
                elif token["part-of-speech"] == "ROOT":
                    rootName = token["text"]
            if id.ingredient == None:
                id.ingredient = dfs_ingredient_root(tokens[rootName])
            if id.amount is None:
                first_word = list(tokens.keys())[0]
                id.amount = str(float(first_word))
            id.parameters = ingredient_parameters(tokens)
            ingredients_data[count] = id
            count += 1
        return ingredients_data

    # Returns a StepData objects given a step
    def parse_step(self, step):
        sd = StepData()
        tokens = self.tokenize(step)
        for tname in tokens:
            token = tokens[tname]
            chunk = self.chunker(token["text"],step)
            if not token["text"]:
                continue
            # find cooking methods
            elif token["text"].lower() in type_checker.methods:
                if chunk not in sd.cookingAction:
                    sd.cookingAction.append(chunk)
            # find ingredients
            elif token["part-of-speech"] in ["dobj","conj"] and chunk.strip() in type_checker.ingredients:
                if chunk not in sd.ingredients:
                    sd.ingredients.append(chunk)
            elif token["part-of-speech"] == "pobj":
                if chunk not in sd.tools:
                    sd.tools.append(chunk)
            elif token["part-of-speech"] == "advmod":
                sd.parameters.append(token["text"])
        return sd