import json 
import os # https://www.tutorialspoint.com/python/os_walk.htm
from collections import defaultdict # when we find doc/term frequency. 
from nltk.tokenize import RegexpTokenizer # use this to find tokens that are alphanumeric, but also numbers with decimals (but not next to letters) 
from  nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import math 

ranking = defaultdict(float)

def query_search(user_input):
    queries = user_input.split()

    for query in queries:
        for document in index_dict:
            # get term freq from document 
            tf_idf = 1 + math.log( term_frequency) # TF part only
            tf_idf += math.log(len(index_dict)/ len (index_dict[query])


    if document in ranking:
        ranking[document] += tf_idf
    else:
        ranking[document] = tf_idf


    sorted_ranks = sorted(ranking.items(), key = lambda i : (-i[1])




