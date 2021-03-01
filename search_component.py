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
from nltk.corpus import stopwords

# from inverted_index import doc_map, position_index, tfidf_index

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
def retrieval(queries, offset_index, docid_index):
  temp_dict = {}
  # Whoever has highest "priority" = displayed first.. 
  start_time = datetime.datetime.now()  # set to a value if entered stopwords in query 
  doc_score = defaultdict(float)

  for query in queries:
    with open("new_inverted_index.txt", "r") as f:
      # start timer? 
      start_time = datetime.datetime.now() 
      # check if query is in the inverted_index
      if query in offset_index:
        # get the position
        pos = offset_index[query]
        f.seek(pos) # move the file pointer to location on file
        posting = ast.literal_eval(f.readline()) # save token and postings
        # posting[1] = { doc1: tf, doc2: tf, doc3: tf.... }
        temp_dict[posting[0]] = posting[1]
      else:
        print("No word found in inverted_list")

  # for all documents in docid_index
  for doc_id in docid_index:
    for token in temp_dict:
      # get current document from token
      doc_id_int = int(doc_id)
      if doc_id_int in temp_dict[token]:

        # check for fragment??

        temp_score =  temp_dict[token][doc_id_int] 
        # check to see if the document is a .txt page ?
        # might actually need to do a re.match/re.search for these values.. 
        if ".txt" in docid_index[doc_id] or "datasets" in docid_index[doc_id]:
          temp_score *= 0.5 

        doc_score[doc_id_int] += temp_score

  # sort values to get best score first
  ret_val=sorted(doc_score.items(), key=lambda x: x[1], reverse = True)

  # print(ret_val[0])
  # print(type(ret_val[0]))
  
  url_list = []
  # retreive the actual url here? 
  for temp_tuple in ret_val:
    url_list.append(docid_index[str(temp_tuple[0])])

  # stop timer
  stop_time = datetime.datetime.now() 

  elapsed_time = stop_time - start_time

  print( str(elapsed_time.total_seconds() * 1000) + " milliseconds" )

  # return top 20 results.
  return url_list[:20] 


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
  '''
  with open("test.txt", "w") as testing:
    for item in docid_index:
      # json made item (doc_id a string) 
      testing.write( docid_index[item] + "\n")
  '''

  stop_words = stopwords.words('english')

  while True:
    queries = input("Enter a query: ").lower().split()
    porter = SnowballStemmer(language="english")

    # stem the queries
    stemmed_query= []
    for query in queries:
      stemmed_query.append(porter.stem(query))

    
    clean_queries = []
    for query in stemmed_query: 
      if query not in stop_words:
        clean_queries.append(query) 

    res = retrieval(clean_queries, word_offsets, docid_index)

    print("Display query: " + str(clean_queries))

    # show all the urls 
    for url in res:
      print(url)