import re
import math

from bs4 import BeautifulSoup # to get soup object
from nltk.stem.snowball import SnowballStemmer

# wouldn't let me import from inverted_index >:( 
def lowercase(text):
  lower_text = [] 
  for word in text:
    lower_text.append(word.lower())

  return lower_text

'''
    Checks for bold, strong, h1, h2, and h3 tags

    This will help create another inverted_index specifically for impotant text 
'''
def important_text(parsed_file):
    porter = SnowballStemmer(language='english')

    b_tokens = [] # used to create a list of strings
    for item in parsed_file.find_all('b'):
        b_tokens.append(' '.join(item.find_all(text=True)))
    b_string = ' '.join(b_tokens) # create one long string of all B texts 

    s_tokens = []
    for item in parsed_file.find_all('strong'):
        s_tokens.append(' '.join(item.find_all(text=True)))
    s_string = ' '.join(s_tokens) # create one long string of all S texts 

    h1_tokens = []
    for item in parsed_file.find_all('h1'):
        h1_tokens.append(' '.join(item.find_all(text=True)))
    h1_string = ' '.join(h1_tokens) # create one long string of all h1 texts 

    h2_tokens = []
    for item in parsed_file.find_all('h2'):
        h2_tokens.append(' '.join(item.find_all(text=True)))
    h2_string = ' '.join(h2_tokens) # create one long string of all h2 texts 

    h3_tokens = []
    for item in parsed_file.find_all('h3'):
        h3_tokens.append(' '.join(item.find_all(text=True)))
    h3_string = ' '.join(h3_tokens) # create one long string of all h3 texts 

    # might need it to be a {token1: weight, token2:}
    final_dict = {} # token : weighted_val
    val_return = {} 

    b_tokens =re.split(r"[^0-9a-zA-Z]+", b_string)
    b_tokens = lowercase(b_tokens) 
    for term in b_tokens:
        if term.isalnum():
            stem_term = porter.stem(term)
            if stem_term in final_dict:
                final_dict[stem_term] += 6
            else:
                final_dict[stem_term] = 6
        
    
    s_tokens =re.split(r"[^0-9a-zA-Z]+", s_string)
    s_tokens = lowercase(s_tokens)
    for term in s_tokens:
        if term.isalnum():
            stem_term = porter.stem(term)
            if stem_term in final_dict:
                final_dict[stem_term] += 5
            else:
                final_dict[stem_term] = 5

    
    h1_tokens =re.split(r"[^0-9a-zA-Z]+", h1_string)
    h1_tokens = lowercase(h1_tokens) 
    for term in h1_tokens:
        if term.isalnum():
            stem_term = porter.stem(term) 
            if stem_term in final_dict:
                final_dict[stem_term] += 4
            else: 
                final_dict[stem_term] = 4


    h2_tokens =re.split(r"[^0-9a-zA-Z]+", h2_string)
    h2_tokens = lowercase(h2_tokens)
    for term in h2_tokens:
        if term.isalnum(): 
            stem_term = porter.stem(term)
            if stem_term in final_dict:
                final_dict[stem_term] += 3
            else:
                final_dict[stem_term] = 3 
    
    h3_tokens =re.split(r"[^0-9a-zA-Z]+", h3_string)
    h3_tokens = lowercase(h3_tokens)
    for term in h3_tokens: # need to implement proper tokenizer
        if term.isalnum():
            stem_term = porter.stem(term)
            if stem_term in final_dict:
                final_dict[stem_term]+= 2
            else:
                final_dict[stem_term] = 2 


    for key,val in final_dict.items():
        val_return[key] = math.log10(val)


    # print(str(val_return))
    return val_return 

