'''
    Search Retrieval component. Does the search queries and stuff.

    Will possibly do document at a time query instead of term at a time
    Lecture 19 - Slide 34 for pseudocode

'''
import ast
import datetime
import json 

from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
from queue import PriorityQueue

# from inverted_index import doc_map, position_index, tfidf_index

'''
# This retrieval function uses Boolean Retrieval AND
def retrieve(index_dict):

  # create another porter stemmer object
  porter = SnowballStemmer(language="english")

  queries = input("Enter a query: ").lower().split(" ")

  matching_docs = set()
  first_query = True

  for query in queries:
    stem_query = porter.stem(query)
    # (Possibly include if statement to check if any of the sets are empty)
    if first_query:
      for doc, tf in index_dict[stem_query].items():
        matching_docs.add(doc)
      first_query = False
    else:
      temp_set = set()
      for doc, tf in index_dict[stem_query].items():
        temp_set.add(doc)

      matching_docs = matching_docs.intersection(temp_set)

  # send results 
  return matching_docs
'''
# returns a dictionary from files created by indexer
def store_in_memory(file_name):
  vals = {}
  with open(file_name, "r") as f:
    # for every line in file, save the key and value into dictionary
    for line in f:
      some_dict = ast.literal_eval(line)
      vals[some_dict[0]] = some_dict[1]

  return vals


# Lecture 19 - Slide 34
# f1 = inverted_index.txt, f2 = word_offsets.txt, f3 = doc_id_map, f4 = tfidf_index 
def retrieval(queries, offset_index, tfidf_index):
  #temp_list = [] 
  temp_dict = {}
  # Whoever has highest "priority" = displayed first.. 
  start_time = 0
  doc_score = defaultdict(float)

  # matching_docs = set() 
  for query in queries:
    with open("inverted_index2.txt", "r") as f:
      # start timer? 
      start_time = datetime.datetime.now() 
      # check if query is in the inverted_index
      if query in offset_index:
        # get the position
        pos = offset_index[query]
        f.seek(pos) # move the file pointer to location on file
        posting = ast.literal_eval(f.readline()) # save token and postings
        # posting[1] = { doc1: tf, doc2: tf, doc3: tf.... }
        # docId_list = posting[1].keys()
        # entry = f.readline() 
        # entry =  token: {doc1: tf, doc2: tf...} = TUPLE.. with a dict 
        # temp_list.extend(ast.literal_eval(entry)) 
        temp_dict[posting[0]] = posting[1]
      else:
        print("No word found in inverted_list")

  # for all documents in docid_index
  for doc_id in docid_index:
    for token in temp_dict:
      # get current document from token
      doc_id_int = int(doc_id)
      if doc_id_int in temp_dict[token]:
        # doc_id matches the doc_id 
        # print( doc_id ) 
        # now get temp_dict[token] -> doc_id
        # now get the tf-idf of doc_id
        temp_score = tfidf_index[doc_id_int] 

        doc_score[doc_id_int] += temp_score
    
    # to add to PriorityQueue we would have to multiply by -1 
    # so the "highest score" would be the first result in PQ

  ret_val=sorted(doc_score.items(), key=lambda x: x[1], reverse = True)

  # stop timer
  stop_time = datetime.datetime.now() 

  elapsed_time = stop_time - start_time

  print( str(elapsed_time.total_seconds() * 1000) + " milliseconds" )

  # for all documents in temp_list...

  return ret_val 


if __name__ == "__main__":
  # need a faster way to do this..
  word_offsets = store_in_memory("word_offsets.txt") 
  # docid_index = store_in_memory("doc_id_map.txt")
  docid_index = {}
  with open("doc_id_map.txt", "r") as f:
    docid_index = json.load(f)

  tfidf_index = store_in_memory("tfidf_index.txt")

  # check if it worked
  '''
  with open("test.txt", "w") as testing:
    for key in docid_index:
      #testing.write("{" + key + ": " + str(docid_index[key]) + "} \n") 
  '''

  # everything is saved correctly.. access as a dict 
  with open("test.txt", "w") as testing:
    for item in docid_index:
      # json made item (doc_id a string) 
      testing.write( docid_index[item] + "\n")

  queries = input("Enter a query: ").lower().split()

  porter = SnowballStemmer(language="english")

  # stem the queries
  stemmed_query= []
  for query in queries:
    stemmed_query.append(porter.stem(query))

  res = retrieval(stemmed_query, word_offsets, tfidf_index)

  print(res)
  print(type(res))