"""
Create an inverted index for the corpus with data structures designed by you.
•Tokens:  all alphanumeric sequences in the dataset.

•Stop words:  do not use stopping while indexing, i.e.  use all words, eventhe frequently occurring ones.•Stemming: use stemming for better textual matches.  
               Suggestion: Porterstemming, but it is up to you to choose.


•Important text:  text in bold (b, strong), in headings (h1, h2, h3), andin  titles  should  be  treated  as  more  important  than  the  in  other  places.
Verify which are the relevant HTML tags to select the important words.

"""
import json 
import os # https://www.tutorialspoint.com/python/os_walk.htm
from collections import defaultdict # when we find doc/term frequency. 
from nltk.tokenize import RegexpTokenizer # use this to find tokens that are alphanumeric, but also numbers with decimals (but not next to letters) 
from bs4 import BeautifulSoup


def inverted_index(): 
  # Your index should be stored in one or more files in the file system (no databases!). <<- from instructions 
  
  index_dict = defaultdict(dict)
  tokens_list = [] # list for all the tokens that are found using tokenizer + soup.find_all (hw2) 
  for root, dirs, files in os.walk("./DEV"):
    for doc in files:
      doc_name = os.path.join(root, doc)
      
      with open(doc_name, "r") as opened:
        content = opened.read() # will get an error using BeautifulSoup 

        json_fields = json.loads(content)
        parsed_file = BeautifulSoup(json_fields['content'], 'lxml') #lxml or html.parser")
        
        token_expression = r'([1-9]\d*(.\d+)?)|\w+' # allow all alphanumeric characters, but if its a number, it will allow a decimal, but only if there is a number after it
        
        tokenize = RegexpTokenizer(token_expression)
        
        #need to read file, get the content, get all the tokens, put into the tokens_list. 
        
        for text in parsed_file.get_text():
          for token in tokenize(text):
            tokens_list.append(token)
        
        
        # finding term frequency --> 
        
        
        
          
          
          
        
  
  

