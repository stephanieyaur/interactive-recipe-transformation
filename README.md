# Chef Bot
Chef Bot is an interactive NLP recipe chatbot that given a recipe url, answers user's recipe questions. 

_Frontend Repo:_ https://github.com/stephanieyaur/recipe-bot

_Backend Repo:_ https://github.com/meganyaur/recipe

## How To Use:
Note that due to latency issues with a free Azure subscription, deployed APIs took too long to load. Instead, our project is run locally for best performance.
1. Clone the frontend repo. Clone the backend repo. 
2. Inside the root directory of the frontend repo, run ````npm start````
3. Inside the root directory of the backend repo, run ````python app.py````
4. Go to http://localhost:3000/ and start asking Chef Bot your recipe questions! An example recipe could be https://www.allrecipes.com/recipe/16354/easy-meatloaf/

## Description
To begin, it offers 2 user flows: 
1. Go over ingredients list
2. Go over recipe steps

A user can ask questions while Chef Bot reviews recipe steps or ask follow up questions about the ingredients. Example questions include:
- Recipe retrieval and display (see example above, including "Show me the ingredients list");
- Navigation utterances ("Go back one step", "Go to the next step", "Repeat please", "Take me to the 1st step", "Take me to the n-th step");
- Vague "how to" questions ("How do I do that?", in which case you can infer a context based on what's parsed for the current step);
- Specific "how to" questions ("How do I <specific technique>?");
- Simple "what is" questions ("What is a <tool being mentioned>?");
- Asking about the parameters of the current step ("How much of <ingredient> do I need?", "What temperature?", "How long do I <specific technique>?", "When is it done?");
- Ingredient substitution questions ("What can I substitute for <ingredient>?");

## Code Structure
Chef Bot is a full stack project comprising of a React frontend and Python backend. The frontend communicates with the backend through 2 APIs:
1. API that parses a recipe in preparation of user flows
2. API that understands a question and returns an answer

Since we used RESTful APIs, the frontend stores the state returned from the first API, which is used as inputs for the second API.

_Frontend Repo:_ https://github.com/stephanieyaur/recipe-bot

_Backend Repo:_ https://github.com/meganyaur/recipe

### Frontend Explanation
After a user enters a recipe url and hits "Go" or ENTER, the user sees the conversational interface. The user is prompted to select one of the user flows and can type in the textbox to ask questions.

### Backend Function Explanations
Strategy for parse_ingredients
- Look for the amount by finding the first occurence of a nummod in the sentence and traverse through heads to find more words related to amounts - stop once reach a word that is not a nummod or is a ROOT word (don't add) or is a dobj or nsubj (don't add)
- Look for the ingredient by seeing if there are 
  1. dobj and adding its children until no more valid children (not nummod or punct)
  2. nsubj and adding its children until no more valid children (not nummod or punct)
  3. if none of those, then it's the root and add its children until no more valid children (not nummod or punct)
- Look for the parameters
  1. Unused root and adding unused children that aren't punct


Strategy for Parsing Steps:
 - Using SpaCy - tokenize text, assign parts of speech.
 - Loop through each token
      - For each, if it's in the list of cooking methods, add it to cooking methods
      - if its a direct object and in the list of ingredients - add it to ingredients
      - if its an indirect object - add to tools
      - if its an adverb - add to parameters
 - chunker helper function - Returns the noun chunk that the token is a part of, if any. Helps keep track of "bread crumbs" as one entity
