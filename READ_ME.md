pip install spacy
python -m spacy download en_core_web_sm

Strategy for parse_ingredients
- Look for the amount by finding the first occurence of a nummod in the sentence and traverse through heads to find more words related to amounts - stop once reach a word that is not a nummod or is a ROOT word (don't add) or is a dobj or nsubj (don't add)
- Look for the ingredient by seeing if there are 
  1. dobj and adding its children until no more valid children (not nummod or punct)
  2. nsubj and adding its children until no more valid children (not nummod or punct)
  3. if none of those, then it's the root and add its children until no more valid children (not nummod or punct)
- Look for the parameters
  1. Unused root and adding unused children that aren't punct

Fix 1 cup dried bread crumbs
Fix salt and pepper, to taste
Fix 2 tablespoons brown sugar
Fix 2 tablespoons prepared mustard

Strategy for Parsing Steps:
 - Using SpaCy - tokenize text, assign parts of speech.
 - Loop through each token
      - For each, if it's in the list of cooking methods, add it to cooking methods
      - if its a direct object and in the list of ingredients - add it to ingredients
      - if its an indirect object - add to tools
      - if its an adverb - add to parameters
 - chunker helper function - Returns the noun chunk that the token is a part of, if any. Helps keep track of "bread crumbs" as one entity



Potential questions:

What is the first step?
How much xx?
What size should the pan be?
How many tomatoes?
What equipment do I need?