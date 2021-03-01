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
import re
import ast
import math


from collections import defaultdict, Mapping # when we find doc/term frequency. Mapping is used for the dict_merge function
#from nltk.tokenize import RegexpTokenizer # use this to find tokens that are alphanumeric, but also numbers with decimals (but not next to letters) 
#from nltk.tokenize import WordPunctTokenizer 
# from nltk.corpus import words not working for some reason.. program gets stuck
from nltk.stem.snowball import SnowballStemmer 
from bs4 import BeautifulSoup

# this is for the search retrieval
#from search_component import retrieve
from index_of_index import index_of_inverted_index

#This is for getting the size of the dict object when merging the dicts
#Used for offloading the dict after 10MB
from sys import getsizeof

# make global so we can read outside  
# might have to move all these values inside functions and use
# global keyword for all of them
index_dict = defaultdict(dict)
doc_id = 0
#batch_number = 1 # set as global variable 
doc_map = {} # holds mapping of doc_id -> url
position_index = {} 
tfidf_index = {}

porter = SnowballStemmer(language='english') 
# https://www.geeksforgeeks.org/snowball-stemmer-nlp/

# The -> the 
# makes it easier to find all words that are the same for the indexer for now
def lowercase(text):
  lower_text = [] 
  for word in text:
    lower_text.append(word.lower())

  return lower_text

# create inverted_index files
def inverted_index(): 
  # Your index should be stored in one or more files in the file system (no databases!). <<- from instructions 
  #tokens_list = [] # list for all the tokens that are found using tokenizer + soup.find_all (hw2) 
  global doc_id
  global batch_number 
  batch_threshold = 18667 # 56000 files /3 = 18666.66 --> 18667 as our threshold to divide it into three parts

  for root, dirs, files in os.walk("./DEV"):
    for doc in files:
      doc_id += 1
      doc_name = os.path.join(root, doc)

      # still doesn't remove foreign characters 
      with open(doc_name, "r", encoding='utf-8', errors='replace') as opened:
        content = opened.read() 
        json_fields = json.loads(content)
        # map the doc_id -> url
        doc_map[doc_id] = json_fields['url']
        parsed_file = BeautifulSoup(json_fields['content'], 'lxml') #lxml or html.parser")

        #token_expression = r'^([1-9]\d*(.\d+)?)|\w+' # allow all alphanumeric characters, but if its a number, it will allow a decimal, but only if there is a number after it

        #token_expression = r'\w+|\$[\d\.]+\S+|\d*\.d+\)' # Lillian's regex from https://www.kite.com/python/docs/nltk.RegexpTokenizer
        #tokenize = RegexpTokenizer(token_expression)

        #need to read file, get the content, get all the tokens, put into the tokens_list. 

        parsed_file.get_text() # make sure beautifulsoup version >= 4.9.0  
        tokens = ' '.join(parsed_file.stripped_strings) # words is one long string
        # lower all the words

        tokens = re.split(r"[^0-9a-zA-Z]+", tokens) # puts string to list and tokenize. only accept numbers and letters 

        tokens = lowercase(tokens)
        # tokens = WordPunctTokenizer().tokenize(tokens) # doesn't remove foreign characters  

        #tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+\S+')

        # Tokenize the words and put them in the inverted index_dict 
        #for token in tokenizer.tokenize(words):
        for token in tokens:
          # only add alphanumeric words to index also check if the token is in nltk corpus words
          if token.isalnum(): 
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

        
        if ( doc_id % batch_threshold == 0): 
          sort_and_write_to_disk()
          index_dict.clear()
          batch_number += 1

        
  # check if there's anything inside the index dict to write last batch to disk
  if ( any(index_dict) ):
    sort_and_write_to_disk()
    index_dict.clear()
    
  

def sort_and_write_to_disk():
  with open("partial_index"+str(batch_number)+".txt", "w", encoding="utf-8") as report:
    sort_inverted_index = sorted(index_dict.items(), key = lambda x: x[0])
    for item in sort_inverted_index:
      report.write(str(item) + "\n")


# Found online: https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
# dict_merge created by Paul Durivage for free use! :D
def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items(): # changed .iteritems() to .items() for python3 as someone mentioned in the comments on the site this code was taken from
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]

def merge_all():
  with open("partial_index1.txt", "r", encoding="utf-8") as partial_index_1, open("partial_index2.txt", "r", encoding="utf-8") as partial_index_2, open("partial_index3.txt", "r", encoding="utf-8") as partial_index_3, open("merged_index.txt", "w", encoding="utf-8") as merged_index:
    line1 = partial_index_1.readline()
    line2 = partial_index_2.readline()
    line3 = partial_index_3.readline()
    current_term = ""
    temp_dict = defaultdict(dict)
    end_of_file = ("", "")

    while True:
      term1 = ()
      term2 = ()
      term3 = ()
      
      if line1 == "" and line2 == "" and line3 == "":
        #print("All done")
        break
      elif line2 == "" and line2 != "" and line3 == "":
        #print("Only line1")
        term1 = eval(line1)
        term2 = end_of_file
        term3 = end_of_file
        current_term = str(term1[0])
      elif line1 != "" and line2 != "" and line3 == "":
        #print("Line3 out")
        term1 = eval(line1)
        term2 = eval(line2)
        term3 = end_of_file
        current_term = min(str(term1[0]), str(term2[0]))
      elif line1 == "" and line2 != "" and line3 == "":
        #print("only line2")
        term1 = end_of_file
        term2 = eval(line2)
        term3 = end_of_file
        current_term = str(term2[0])
      elif line1 == "" and line2 != "" and line3 != "":
        #print("line1 out")
        term1 = end_of_file
        term2 = eval(line2)
        term3 = eval(line3)
        current_term = min(str(term2[0]), str(term3[0]))
      elif line1 == "" and line2 == "" and line3 != "":
        #print("Only line3")
        term1 = end_of_file
        term2 = end_of_file
        term3 = eval(line3)
        current_term = str(term3[0])
      elif line1 != "" and line2 == "" and line3 != "":
        #print("line2 out")
        term1 = eval(line1)
        term2 = end_of_file
        term3 = eval(line3)
        current_term = min(str(term1[0]), str(term1[0]))
      else:
        term1 = eval(line1)
        term2 = eval(line2)
        term3 = eval(line3)
        current_term = min(str(term1[0]), str(term2[0]), str(term3[0]))
      
      if current_term == term1[0] and current_term == term2[0] and current_term == term3[0]:
        temp_dict[current_term] = term1[1]
        dict_merge(temp_dict[current_term], term2[1])
        dict_merge(temp_dict[current_term], term3[1])
        line1 = partial_index_1.readline()
        line2 = partial_index_2.readline()
        line3 = partial_index_3.readline()
      elif current_term == term1[0] and current_term == term2[0] and current_term != term3[0]:
        temp_dict[current_term] = term2[1]
        dict_merge(temp_dict[current_term], term2[1])
        line1 = partial_index_1.readline()
        line2 = partial_index_2.readline()
      elif current_term == term1[0] and current_term != term2[0] and current_term != term3[0]:
        temp_dict[current_term] = term1[1]
        line1 = partial_index_1.readline()
      elif current_term != term1[0] and current_term == term2[0] and current_term == term3[0]:
        temp_dict[current_term] = term1[1]
        dict_merge(temp_dict[current_term], term3[1])
        line2 = partial_index_2.readline()
        line3 = partial_index_3.readline()
      elif current_term != term1[0] and current_term != term2[0] and current_term == term3[0]:
        temp_dict[current_term] = term3[1]
        line3 = partial_index_3.readline()
      elif current_term == term1[0] and current_term != term2[0] and current_term == term3[0]:
        temp_dict[current_term] = term1[1]
        dict_merge(temp_dict[current_term], term3[1])
        line1 = partial_index_1.readline()
        line3 = partial_index_3.readline()
      elif current_term != term1[0] and current_term == term2[0] and current_term != term3[0]:
        temp_dict[current_term] = term2[1]
        line2 = partial_index_2.readline()
      
      dict_threshold = 1000000 #1 mil bytes == 10 MB
      if getsizeof(temp_dict) > dict_threshold:
        for k, v in temp_dict.items():
          merged_index.write(str(k) + " : " + str(v)+"\n")
        temp_dict.clear()
    
    for k, v in temp_dict.items():
        merged_index.write(str(k) + " : " + str(v)+"\n")
    temp_dict.clear()
      
    
    partial_index_1.close()
    partial_index_2.close()
    partial_index_3.close()


# position_index is a dict { token: position}
def get_tfidf_index(file_name):
  # this would contain { doc_id: tf-idfscore }
  tfidf_index = defaultdict(float) 
  # need to iterate over merged inverted_index.txt
  with open(file_name, "r") as inverted_index_file:
    # for every token in the document.. 
    for line in inverted_index_file:
      posting = ast.literal_eval(line) # ( token, {doc1: tf, doc2: tf, doc3: tf, ... } )
      # for every doc_id we need to extract the term frequency of the token..compute the tf-idf.  
      # posting[1] = { doc1: tf, doc2: tf, doc3:tf, ...}
      temp_dict = posting[1]
      for doc_num in temp_dict: 
        # ( 1 + log(term-freq) ) * log(  # docs  / # times appear in docs ) 
        #tfidf_score = (1 + math.log10(temp_dict[doc_num])) * math.log10(doc_id / len(temp_dict))
        tfidf_score = (1 + math.log10(temp_dict[doc_num])) * math.log10( 55393 / len(temp_dict))

        if doc_num in tfidf_index:
          tfidf_index[doc_num] += tfidf_score
        else: 
          tfidf_index[doc_num] = tfidf_score


  # write tfidf_index to another file?
  with open("tfidf_index.txt", "w") as tfidf_file:
    for key in sorted(tfidf_index):
      tfidf_file.write("(" + str(key) + ", " + str(round(tfidf_index[key], 3)) + ") \n" )

  return tfidf_index

if __name__ == "__main__":

  # call inverted_index function
  #print("Inverted index started")
  inverted_index()
  #print("Inverted index finished")
  merge_all()
  '''
  with open("inverted_index2.txt", "w", encoding="utf-8") as report:
    sort_inverted_index = sorted(index_dict.items(), key=lambda x: x[0])
    for item in sort_inverted_index:
      report.write(str(item) + "\n")
  '''
  # need to figure out merging files

  # save all docs as a tuple... to make it much easier to save as dict later on
  # dont have to write the mapping since it doesn't use that much in-memory
  with open("doc_id_map.txt", "w") as mapping:
    #for key in doc_map:
    # having problems saving the URL and reading with ast.literal_eval
    #  mapping.write("(" + str(key) + ", '" + doc_map[key] + "') \n" )
    json.dump(doc_map, mapping, indent=2)
  
  # after finished merging, create an index of the inverted index
  # change filename to w.e merged inverted_index file is called
  position_index = index_of_inverted_index("inverted_index2.txt")

  tfidf_index = get_tfidf_index("inverted_index2.txt")

  # get all position of inverted_index. but we want to do tf-idf of entire inverted_index

  # Save to an output file if needed, but we can keep above in memory! (~1mil tokens)
  with open("word_offsets.txt", "w") as f2:
    for key in position_index:
      f2.write("('" + key + "', " + str(position_index[key]) + ") \n")  

  # dont need below to test the indexer
  '''
  while True:
    docs_set = retrieve(index_dict)
    docs_list = list(docs_set)[:5] # get top 5 links

    for item in docs_list:
      print(doc_map[item])
  ''' 