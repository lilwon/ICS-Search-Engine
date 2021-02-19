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

# make global so we can read outside  
index_dict = defaultdict(dict)
doc_id = 0

doc_map = {} # holds mapping of doc_id -> url

porter = PorterStemmer()
# Added lowercase because we want unique words... 
# The -> the 
# makes it easier to find all words that are the same for the indexer for now
def lowercase(text):
  lower_text = ""
  for word in text:
    lower_text += word.lower()

  return lower_text


def inverted_index(): 
  # Your index should be stored in one or more files in the file system (no databases!). <<- from instructions 
  #tokens_list = [] # list for all the tokens that are found using tokenizer + soup.find_all (hw2) 
  global doc_id
  for root, dirs, files in os.walk("./DEV"):
    for doc in files:
      doc_id += 1
      doc_name = os.path.join(root, doc)
       
      with open(doc_name, "r") as opened:

        content = opened.read() # will get an error using BeautifulSoup 
        
        json_fields = json.loads(content)
        # map the doc_id -> url
        doc_map[doc_id] = json_fields['url']

        parsed_file = BeautifulSoup(json_fields['content'], 'lxml') #lxml or html.parser")
        
        #token_expression = r'^([1-9]\d*(.\d+)?)|\w+' # allow all alphanumeric characters, but if its a number, it will allow a decimal, but only if there is a number after it

        #token_expression = r'\w+|\$[\d\.]+\S+|\d*\.d+\)' # Lillian's regex from https://www.kite.com/python/docs/nltk.RegexpTokenizer
        #tokenize = RegexpTokenizer(token_expression)

        #need to read file, get the content, get all the tokens, put into the tokens_list. 

        parsed_file.get_text() # make sure beautifulsoup version >= 4.9.0  


        words = ' '.join(parsed_file.stripped_strings) # words is one long string

        # lower all the words
        words = lowercase(words)

        tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+\S+|\d*\.d+\)')

        # CURRENTLY USING URLS FOR ALL DOC IDS, CAN CHANGE LATER
        for token in tokenizer.tokenize(words):

          stem_word = porter.stem(token)

          # if the word is not in the index, add the doc_id + init frequency (1)
          if stem_word not in index_dict:
            index_dict[stem_word][doc_id] = 1

          # Token is already in index, but we need to add NEW doc_id + init frequency(1) 
          elif stem_word in index_dict and doc_id not in index_dict[stem_word]:
            index_dict[stem_word][doc_id] = 1

          # Increase the frequency if token and doc_id is in the index 
          elif stem_word in index_dict and doc_id in index_dict[stem_word]:
            index_dict[stem_word][doc_id] += 1


def retrieve():
  '''
      Currently uses boolean retrieval for queries with AND
  '''

  queries = input("Enter a query: ").lower().split(" ")

  matching_docs = set()
  first_query = True

  for query in queries:
    stem_query = porter.stem(query)

    if first_query:
      for doc, tf in index_dict[stem_query].items():
        matching_docs.add(doc)
      first_query = False
    else:
      temp_set = set()
      for doc, tf in index_dict[stem_query].items():
        temp_set.add(doc)

      matching_docs.intersection(temp_set)

  return matching_docs

# write outside otherwise O(n^4) LOL
'''
with open("inverted_index.txt", "w", encoding="utf-8") as report:
  for key, values in index_dict.items():
    report.write(key + " --> ") 
    for subkey, value in values.items():
      report.write('({}, {}) '.format(subkey, value))

    report.write("\n")

print("Number of docs indexed: ", doc_id)

with open("docmap.txt", "w", encoding="utf-8") as mapping:
    for key, value in doc_map.items():
        mapping.write(str(key) + ", " + value + "\n")
'''

if __name__ == "__main__":

  # call inverted_index function
  inverted_index()

  while True:
    docs_set = retrieve()
    docs_list = list(docs_set)[:5] # get top 5 links

    for item in docs_list:
      print(doc_map[item])