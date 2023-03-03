## Class Recipe
from posixpath import split
from nltk import ne_chunk, pos_tag, word_tokenize
import fractions
import re
import type_checker

class recipe:
    def __init__(self,ingredients,steps):
        self.ingredients = ingredients
        self.steps = []
        self.curr = 0
        # self.prep_time
        # self.cook_time
        # self.servings

    
        """
        for ingredient in ingredients:
            amount = 0
            split_text = ingredient.split(' ')
            for i in range(len(split_text)):
                if split_text[i][0].isdigit():
                    try:
                        amount += float(split_text[i])
                    except:
                        if regex.search("^[1-9\/]*$",split_text[i]):
                            frac = fractions.Fraction(split_text[i])
                            amount += frac.numerator/frac.denominator
                # this might break for "fluid ounces" - might change to NLTK parser
                elif type_checker.is_measurement(split_text[i]):
                    unit = split_text[i]
                else:
                    food = split_text[i:]
                    self.ingredient_dict[food] = str(amount) + unit
                    break
        """

        for step in steps:
            substeps = step.split('. ')
            for substep in substeps:
                ## TODO ##
                # Parse steps (stanford dependency parser?)
                # verb is cooking method, DO is ingredient, IO will have tools (and maybe other ingredients)
                self.steps.append(substep)

    def print_current_step(self):
        print(self.steps[self.curr])

    def change_step(self,n):
        # n is how many steps to move (+ for forward, - for backward)
        if self.curr + n >= len(self.steps):
            print("Not enough steps left, changing to last")
            self.curr = len(self.steps)-1
        elif self.curr + n < 0:
            print("Can't move back that far, changing to first:")
            self.curr = 0
        else:
            self.curr += n

    def how_much(self,food):
        for ing in self.ingredients:
            if re.search(food,ing):
                return "You need: " + ing
        return "You dont need any " + food




    
    
        


    

        

        
    



            










        
    
