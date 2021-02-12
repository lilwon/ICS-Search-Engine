# Bryan Snyder, Matthew Olitoquit, Lillian Won / Winter 2021 


"""
Create an inverted index for the corpus with data structures designed by you.
•Tokens:  all alphanumeric sequences in the dataset.

•Stop words:  do not use stopping while indexing, i.e.  use all words, eventhe frequently occurring ones.
•Stemming: use stemming for better textual matches.  
               Suggestion: Porterstemming, but it is up to you to choose.


•Important text:  text in bold (b, strong), in headings (h1, h2, h3), andin  titles  should  be  treated  as  more  important  than  the  in  other  places.
Verify which are the relevant HTML tags to select the important words.

"""
import json 
import os # https://www.tutorialspoint.com/python/os_walk.htm
from collections import defaultdict # when we find doc/term frequency. 
from nltk.tokenize import RegexpTokenizer # use this to find tokens that are alphanumeric, but also numbers with decimals (but not next to letters) 
from  nltk.stem import PorterStemmer
from bs4 import BeautifulSoup

# used for holding Simhash differences

# Added lowercase because we want unique words... 
# The -> the 
# makes it easier to find all words that are the same for the indexer for now
def lowercase(text):
  lower_text = ""
  for word in text:
    lower_text += word.lower()

  return lower_text

# make global so we can read outside  
index_dict = defaultdict(dict)
doc_id = 0

porter = PorterStemmer()

def inverted_index(): 
  # Your index should be stored in one or more files in the file system (no databases!). <<- from instructions 
  tokens_list = [] # list for all the tokens that are found using tokenizer + soup.find_all (hw2) 
  for root, dirs, files in os.walk("./DEV"):
    for doc in files:
      doc_name = os.path.join(root, doc)
      
      with open(doc_name, "r") as opened:
        # start at 1 instead of 0
        doc_id += 1

        content = opened.read() # will get an error using BeautifulSoup 
        # IMPORTANT we need to map the doc_id -> url
        
        json_fields = json.loads(content)
        parsed_file = BeautifulSoup(json_fields['content'], 'lxml') #lxml or html.parser")
        
        #token_expression = r'^([1-9]\d*(.\d+)?)|\w+' # allow all alphanumeric characters, but if its a number, it will allow a decimal, but only if there is a number after it

        token_expression = r'\w+|\$[\d\.]+\S+|\d*\.d+\)' # Lillian's regex from https://www.kite.com/python/docs/nltk.RegexpTokenizer
        tokenize = RegexpTokenizer(token_expression)
        
        #need to read file, get the content, get all the tokens, put into the tokens_list. 

        parsed_file.get_text() # make sure beautifulsoup version >= 4.9.0   

        words = ' '.join(parsed_file.stripped_strings) # words is one long string

        # lower all the words
        words = lowercase(words)

        # CURRENTLY USING URLS FOR ALL DOC IDS, CAN CHANGE LATER
        for token in tokenize(words):

          stem_word = porter(token)

          # if the word is not in the index, add the doc_id + init frequency (1)
          if stem_word not in index_dict:
            index_dict[stem_word][doc_id] = 1

          # Token is already in index, but we need to add NEW doc_id + init frequency(1) 
          elif stem_word not in index_dict and doc_id not in index_dict[stem_word]:
            index_dict[stem_word][doc_id] = 1

          # Increase the frequency if token and doc_id is in the index 
          elif stem_word in index_dict and doc_id in index_dict[stem_word]:
            index_dict[stem_word][doc_id] += 1
          


if __name__ == "__main__":

  # call inverted_index function
  inverted_index()

  # write outside otherwise O(n^4) LOL
  with open("inverted_index.txt", "w", encoding="utf-8") as report:
    for key, values in index_dict.items():
      report.write(key + " --> ") 
      for subkey, value in values.items():
       report.write('({}, {}) '.format(subkey, value))

      report.write("\n")

  print("Number of docs indexed: ", doc_id)
