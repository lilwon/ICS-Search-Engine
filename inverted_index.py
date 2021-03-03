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
#from urllib.parse import urldefrag

# this is for the search retrieval
#from search_component import retrieve
from index_of_index import index_of_inverted_index
from important_text import important_text

#This is for getting the size of the dict object when merging the dicts
#Used for offloading the dict after 10MB
from sys import getsizeof

# make global so we can read outside  
# might have to move all these values inside functions and use
# global keyword for all of them
index_dict = defaultdict(dict)
doc_id = 0
batch_number = 1 # set as global variable 
doc_map = {} # holds mapping of doc_id -> url
position_index = {} 
tfidf_index = {}
doc_seen = set()
important_text_index = defaultdict(dict)

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
  global doc_id
  global batch_number 
  batch_threshold = 18667 # 56000 files /3 = 18666.66 --> 18667 as our threshold to divide it into three parts

  for root, dirs, files in os.walk("./DEV"):
    for doc in files:
      doc_name = os.path.join(root, doc)
      # still doesn't remove foreign characters 
      with open(doc_name, "r", encoding='utf-8', errors='replace') as opened:
        #doc_id += 1
        content = opened.read() 
        json_fields = json.loads(content)
        # map the doc_id -> url

        # defrag the url before we save to doc_id
        # defragged = urldefrag(json_fields['url']) # defrag another way
        url = json_fields['url'] 
        url = url.split('#')[0]
        # save to seen
        if url not in doc_seen:
          doc_id += 1 
          doc_seen.add(url)
          doc_map[doc_id] = url 

          parsed_file = BeautifulSoup(json_fields['content'], 'lxml') #lxml or html.parser")

          temp_imp_index = important_text(parsed_file) # returns { important_text: score }

          for key, val in temp_imp_index.items():
            important_text_index[key][doc_id] = val

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

# Sorts and writes partial indexes based on their batch number 
def sort_and_write_to_disk():
  with open("partial_index"+str(batch_number)+".txt", "w", encoding="utf-8") as report:
    sort_inverted_index = sorted(index_dict.items(), key=lambda x:x[0])
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

# Merges the partial indexes into one giant index. Because we decided to split up our partial indexes into thirds, this merge only works for merging three opened files at once. 
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

      #Checks if any of the files are finished/end of the file has been reached. 
      # Based on how many are finished, it will compare the lines from readline() for each of the files and find the term that comes first alphabetically 
      if line1 == "" and line2 == "" and line3 == "": # If all three files are empty or the end of the files have been reached, it will break out of the while loop
        break
      elif line1 != "" and line2 == "" and line3 == "": # Second and third file are finished
        term1 = eval(line1)
        term2 = end_of_file
        term3 = end_of_file
        current_term = str(term1[0])
      elif line1 != "" and line2 != "" and line3 == "": #Third file finished
        term1 = eval(line1)
        term2 = eval(line2)
        term3 = end_of_file
        current_term = min(str(term1[0]), str(term2[0]))
      elif line1 == "" and line2 != "" and line3 == "": # First and third file are finished
        term1 = end_of_file
        term2 = eval(line2)
        term3 = end_of_file
        current_term = str(term2[0])
      elif line1 == "" and line2 != "" and line3 != "": # First file finished
        term1 = end_of_file
        term2 = eval(line2)
        term3 = eval(line3)
        current_term = min(str(term2[0]), str(term3[0]))
      elif line1 == "" and line2 == "" and line3 != "": # First and second file are finished
        term1 = end_of_file
        term2 = end_of_file
        term3 = eval(line3)
        current_term = str(term3[0])
      elif line1 != "" and line2 == "" and line3 != "": # Second file finished
        term1 = eval(line1)
        term2 = end_of_file
        term3 = eval(line3)
        current_term = min(str(term1[0]), str(term1[0]))
      else: # None of the files are finished 
        term1 = eval(line1)
        term2 = eval(line2)
        term3 = eval(line3)
        current_term = min(str(term1[0]), str(term2[0]), str(term3[0]))
      
      # Compared if the current_term is the same for any of the readline() of each file and if yes, then it will merge the postings together into the temp_dict
      if current_term == term1[0] and current_term == term2[0] and current_term == term3[0]: #If all three files match the current_term
        temp_dict[current_term] = term1[1]
        dict_merge(temp_dict[current_term], term2[1])
        dict_merge(temp_dict[current_term], term3[1])
        line1 = partial_index_1.readline()
        line2 = partial_index_2.readline()
        line3 = partial_index_3.readline()
      elif current_term == term1[0] and current_term == term2[0] and current_term != term3[0]: #If only file1 and file2 match
        temp_dict[current_term] = term1[1]
        dict_merge(temp_dict[current_term], term2[1])
        line1 = partial_index_1.readline()
        line2 = partial_index_2.readline()
      elif current_term == term1[0] and current_term != term2[0] and current_term != term3[0]: #If only file1 matches
        temp_dict[current_term] = term1[1]
        line1 = partial_index_1.readline()
      elif current_term != term1[0] and current_term == term2[0] and current_term == term3[0]: # If only file2 and file3 match
        temp_dict[current_term] = term2[1]
        dict_merge(temp_dict[current_term], term3[1])
        line2 = partial_index_2.readline()
        line3 = partial_index_3.readline()
      elif current_term != term1[0] and current_term != term2[0] and current_term == term3[0]: # If only file3 matches
        temp_dict[current_term] = term3[1]
        line3 = partial_index_3.readline()
      elif current_term == term1[0] and current_term != term2[0] and current_term == term3[0]: # If only file1 and file3 match
        temp_dict[current_term] = term1[1]
        dict_merge(temp_dict[current_term], term3[1])
        line1 = partial_index_1.readline()
        line3 = partial_index_3.readline()
      elif current_term != term1[0] and current_term == term2[0] and current_term != term3[0]: # If only file2 matches 
        temp_dict[current_term] = term2[1]
        line2 = partial_index_2.readline()
      
      #Once the temp_dict reaches 10MB in size, it will offload the temp_dict into the merged_index txt file
      #Because when parsing through the partial indexes, everything was already sorted alphabetically and the postings were sorted by docID, 
      # so no sorting is required as everything is added into the temp_dict in alnum order
      dict_threshold = 1000000 #1 mil bytes == 10 MB
      if getsizeof(temp_dict) > dict_threshold:
        for k, v in temp_dict.items():
          merged_index.write("('" + str(k) + "', " + str(v)+ ") \n")
        temp_dict.clear()
    
    #This is used for offloading the final batch that has not reached the 10MB threshold. 
    for k, v in temp_dict.items():
        merged_index.write("('" + str(k) + "', " + str(v) +") \n")
    temp_dict.clear()
      
    #Must close all open files here
    partial_index_1.close()
    partial_index_2.close()
    partial_index_3.close()
    merged_index.close()


# position_index is a dict { token: position}
def get_tfidf_index(file_name):
  # need to iterate over merged inverted_index.txt
  with open("new_inverted_index.txt", "w") as new_index_file:
    with open(file_name, "r") as inverted_index_file:
      # for every token in the document.. 
      for line in inverted_index_file:
        tfidf_index = {} 
        posting = ast.literal_eval(line) # ( token, {doc1: tf, doc2: tf, doc3: tf, ... } )
        # for every doc_id we need to extract the term frequency of the token..compute the tf-idf.  
        # posting[1] = { doc1: tf, doc2: tf, doc3:tf, ...}
        temp_dict = posting[1]
        for doc_num in temp_dict: 
          # ( 1 + log(term-freq) ) * log(  # docs  / # times appear in docs )
          tfidf_index[doc_num] = round((1 + math.log10(temp_dict[doc_num])) * math.log10( doc_id / len(temp_dict)), 3) 
          # tfidf_index[doc_num] = round((1 + math.log10(temp_dict[doc_num])) * math.log10( 53792 / len(temp_dict)), 3) 

        transfer_posting = (posting[0], tfidf_index) # save as a set to store to write to a new inverted_index file
        new_index_file.write( str(transfer_posting) + "\n")
        

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

  with open("important_text_inverted.txt", "w") as imp_text_file:
    sorted_imp_text = sorted(important_text_index.items(), key = lambda x: x[0])
    for item in sorted_imp_text:
      imp_text_file.write(str(item) + "\n")
  # need to figure out merging files

  # save all docs as a tuple... to make it much easier to save as dict later on
  # dont have to write the mapping since it doesn't use that much in-memory
  with open("doc_id_map.txt", "w") as mapping:
    #for key in doc_map:
    # having problems saving the URL and reading with ast.literal_eval
    #  mapping.write("(" + str(key) + ", '" + doc_map[key] + "') \n" )
    json.dump(doc_map, mapping, indent=2)

  # get all position of inverted_index. but we want to do tf-idf of entire inverted_index
  get_tfidf_index("merged_index.txt")

  # after finished merging, create an index of the inverted index
  # change filename to w.e merged inverted_index file is called
  position_index = index_of_inverted_index("new_inverted_index.txt")
  # Save to an output file if needed, but we can keep above in memory! (~1mil tokens)
  with open("word_offsets.txt", "w") as f2:
    for key in position_index:
      f2.write("('" + key + "', " + str(position_index[key]) + ") \n")  


  imptext_position_index = index_of_inverted_index("important_text_inverted.txt")
  with open("imptext_offsets.txt","w") as f3:
    for key in imptext_position_index:
     f3.write("('" + key + "', " + str(imptext_position_index[key]) + ") \n")  