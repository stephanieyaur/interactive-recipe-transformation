import requests
from bs4 import BeautifulSoup
import nltk
import webbrowser
import re
from requests_html import HTMLSession



# given a question, returns a youtube video to answer it
def search_youtube(question):

    # gets all nouns and verbs from sentence
    text = nltk.word_tokenize(question)
    pos_tagged = nltk.pos_tag(text)
    print(pos_tagged)
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
        print("No results found on YouTube")
    else:
        first_link = links[0]
        webbrowser.open_new(first_link)
        print(first_link)
        return first_link

test = search_youtube("How to cook onions")