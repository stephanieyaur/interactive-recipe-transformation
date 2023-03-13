from dependency_parser import DependencyParser

url = ""
title = ""
ingredients = []
steps = []
prep_time = "" 
cook_time = "" 
total_time = ""

dp = DependencyParser()
tools = []
parsed_steps = []
parsed_ingredients = []

last_bot = ""
last_user = ""

transformations = {}

curr_step = -1