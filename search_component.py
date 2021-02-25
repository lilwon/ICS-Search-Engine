'''
    Search Retrieval component. Does the search queries and stuff.

'''

from nltk.stem.snowball import SnowballStemmer

def retrieve(index_dict):
  '''
      Currently uses boolean retrieval for queries with AND
  '''

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