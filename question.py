import requests
from bs4 import BeautifulSoup
import nltk
import webbrowser
import re
import json

import global_vars
from dependency_parser import DependencyParser
# import requests_html
from nltk.stem.snowball import SnowballStemmer
from word2number import w2n
from number_parser import parse_ordinal
from requests_html import HTMLSession
from transform import transformDriver


# returns response as json object with 'text' and 'url' fields
def get_response(question):
    response = question_parser(question)
    global_vars.last_bot = response
    return response

def question_parser(question):
    def go_over_step():
        if (global_vars.curr_step < len(global_vars.steps)):
            return set_phrases[5] + " " + str(global_vars.curr_step + 1) + ": " + global_vars.steps[global_vars.curr_step]
        else:
            return set_phrases[6]

    # question = [q.lower() for q in question.split()] 
    question = question.lower().strip()
    set_phrases= ["Please specify a URL.", "What do you want to do? [1] Go over ingredients list or [2] Go over recipe steps.", "I didn't quite catch that. Can you please rephrase?",
                  " Would you like to begin Step 1?", "Would you like to continue to Step", "Step", "Congrats - you've gone through all the steps! Would you like to go over the steps again? [yes] or [no]", "Ok, how would you like to convert the recipe? Type [convert to] along with an option: vegetarian, non-vegetarian, healthy, unhealthy, lactose-free, chinese, kosher milk, or kosher meat"]
    stemmer = SnowballStemmer("english") 

    text = nltk.word_tokenize(question)
    pos_tagged = nltk.pos_tag(text)
    numerical_words = [x[0] for x in filter(lambda x:x[1]=='CD' or x[1]=='JJ', pos_tagged)]
    
    if global_vars.url == "":
        if question.startswith("http"):
            # should try catch calling get_recipe
            url = question
            return "Let's start cooking " + global_vars.title + "! " + set_phrases[1]
        else:
            return set_phrases[0]
    else:
        # thank you
        if question == "thank you" or question == "thanks" or question == "thank you." or question == "thanks." or question == "thank you!" or question == "thanks!":
            if global_vars.curr_step == -1:
                return set_phrases[3]
            else:
                return set_phrases[4] + " " + str(global_vars.curr_step+2) + "?"
        else:
            # remove thank you/thanks, please, periods, and whitespace
            question = question.replace("thank you", "")
            question = question.replace("thanks", "")
            question = question.replace("please", "")
            question = question.replace(".", "")
            question = question.replace("!", "")
            question = question = question.strip()

        # yes no
        if question == "yes" or question == "yes.":
            if global_vars.last_bot == set_phrases[3] or global_vars.last_bot.startswith(set_phrases[4]):
                global_vars.curr_step += 1
                return go_over_step()
            elif global_vars.last_bot == set_phrases[6]:
                global_vars.curr_step = 0
                return go_over_step()
        elif question == "no" or question == "no.":
            return set_phrases[1]

        # option 1 or 2
        if question =="1" or question == "one" or question == "go over ingredients list":
            print("Ingredients:")
            for i in global_vars.ingredients:
                print(" - " + i)
            return
        elif question =="2" or question == "two" or question == "go over recipe steps" or question == "go over steps" or question == "recipe steps" or question == "steps":
            global_vars.curr_step += 1
            return go_over_step()
        elif question == "3" or question == "three" or question == "Transform the recipe" or ("convert" in question and "convert to" not in question) or "transform" in question:
            return set_phrases[7]
        elif "steps" in question and "all" in question:
            for i in range(len(global_vars.steps)):
                print(str(i+1) + ". " + global_vars.steps[i])
            return
        
        # times
        if "time" in question:
            if "prep" in question or "prepare" in question or "preparation" in question or "preparing" in question:
                return "The prep time is: " + str(global_vars.prep_time) + ". Note that prep time + cook time = total time."
            if "cook" in question or "cooking" in question:
                return "The cook time is: " + str(global_vars.cook_time) + ". Note that prep time + cook time = total time."
            else:
                return "The total time is: " + str(global_vars.total_time) + ". Note that prep time + cook time = total time."
        
        # many means quantity of either an ingredient or steps
        if "many" in question or "much" in question:
            if "steps" in question:
                return "There are " + str(len(global_vars.steps)) + " total steps."
            if "ingredients" in question:
                return "The recipe calls for " + str(len(global_vars.ingredients)) + " ingredients."
            if "tools" in question:
                return "The recipe calls for " + str(len(global_vars.tools)) + " tools."
            else:
                stopwords = ['i']
                q_ingredients = filter(lambda x:x[1]=='NN' or x[1]=='NNS', pos_tagged)
                q_ingredients = [word for word in q_ingredients if word not in stopwords]
                ingredient = stemmer.stem(q_ingredients[0][0])
                amounts = [ingredient_step for ingredient_step in global_vars.ingredients if ingredient in ingredient_step]
                if amounts == []:
                    return set_phrases[2]
                return [ingredient_step for ingredient_step in global_vars.ingredients if ingredient in ingredient_step][0]
            
        # get next step
        if "next" in question:
            if global_vars.curr_step < len(global_vars.steps) - 1:
                global_vars.curr_step += 1
                return go_over_step()
            else:
                return "Well done, that's the end of the recipe steps!"
            
        # go back step
        if "back" in question:
            if global_vars.curr_step > 0:
                global_vars.curr_step -= 1
                return go_over_step()
            else:
                return "This is the first step."

        # get nth step
        if len(numerical_words) != 0 and "step" in question:
            chunk = " ".join([word for word in numerical_words])
            try:
                step_index = w2n.word_to_num(chunk)
            except:
                try:
                    step_index = parse_ordinal(chunk)
                except:
                    return "I can see you're trying to get a certain number step. Please enter a valid number word (eg. two or second)"
            if not step_index:
                return "I can see you're trying to get a certain number step. Please enter a valid number word (eg. two or second)"
            if step_index <= len(global_vars.steps):
                global_vars.curr_step = step_index - 1
                return go_over_step()
            else:
                return "Not a valid step number. There are " + str(len(global_vars.steps)) + " total steps."
            
        
        # youtube tutorial
        if "how to" in question or "how do" in question:
            return search_youtube(question)
        
        # repeat
        if "repeat" in question:
            if "step" in question:
                return set_phrases[5] + " " + str(global_vars.curr_step+1) + ": " + global_vars.steps[global_vars.curr_step]
            else:
                return global_vars.last_bot
        
        # tools list
        if "tools" in question:
            for t in global_vars.tools:
                print(" - " + t)
            return

        # ingredients list
        if "ingredients" in question:
            for i in global_vars.ingredients:
                print(" - " + i)
            return
        
        # steps list
        if "steps" in question:
            for i in range(len(global_vars.steps)):
                print(str(i+1) + ". " + global_vars.steps[i])
            return

        if "recipe" in question:
            if "for" in question or "make" in question:
                return global_vars.title
            return displayEntireRecipe()

        if "convert to" in question:
            print("Ok, give me one second to convert the recipe...")
            return transformDriver(question)

    return set_phrases[2]

# given a question, returns a youtube video to answer it
def search_youtube(question):

    # gets all nouns and verbs from sentence
    text = nltk.word_tokenize(question)
    pos_tagged = nltk.pos_tag(text)
    query_terms = [x[0] for x in filter(lambda x:x[1]=='NN' or x[1]=='VB' or x[1]=='NNS', pos_tagged)]

    # get first YouTube result
    search_link = "http://www.youtube.com/results?search_query=" + '+'.join(query_terms)

    session = HTMLSession()
    response = session.get(search_link)
    response.html.render(sleep=1, keep_page = True, scrolldown = 2)

    links = []
    for l in response.html.find('a#video-title'):
        link = next(iter(l.absolute_links))
        links.append(link)
    if len(links) == 0:
        # No results found on YouTube
        return "No results found on YouTube"
    else:
        first_link = links[0]
        webbrowser.open_new(first_link)
        return first_link

# test = search_youtube("How to cook onions")

def displayEntireRecipe():
    print(global_vars.title)
    print("--------------------------")
    print("Prep Time: " + global_vars.prep_time)
    print("Cook Time: " + global_vars.cook_time)
    print("Total Time: " + global_vars.total_time)
    print("--------------------------")
    print("Ingredients:")
    for i in global_vars.ingredients:
        print(" - " + i)
    print("--------------------------")
    print("Tools:")
    for t in global_vars.tools:
        print(" - " + t)
    print("--------------------------")
    print("Steps:")
    for i in range(len(global_vars.steps)):
        print(str(i + 1) + ". " + global_vars.steps[i])
    return