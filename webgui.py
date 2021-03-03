import ast
import datetime
import json

from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

from flask import Flask, request, redirect, render_template
app = Flask(__name__) # used for app route 

# global in memory dictionaries for fast seek
stemmer = SnowballStemmer(language="english")
word_offsets = {}
important_offsets = {}
docid_index = {}

def store_in_memory(file_name):
    vals = {}
    with open(file_name, "r") as f:
        for line in f:
            some_dict = ast.literal_eval(line)
            vals[some_dict[0]] = some_dict[1]

    return vals

# returns a list of top urls for the query
def retrieval(queries):
    temp_dict = {}
    doc_score = defaultdict(float)
    imp_temp_dict = {}
    # start timer here
    start_time = datetime.datetime.now() 
  
    # this for loop checks for the offset of IMPORTANT texts
    for query in queries:
        with open("important_text_inverted.txt", "r") as f:
            if query in important_offset:
                pos = important_offset[query]
                f.seek(pos)
                posting = ast.literal_eval(f.readline())  
                imp_temp_dict[posting[0]] = posting[1]

    # this checks for all tokens in inverted_index
    for query in queries:
        with open("new_inverted_index.txt", "r") as f:
          # check if query is in the inverted_index
           if query in word_offsets:
                #get the position
                pos = word_offsets[query]
                f.seek(pos) # move the file pointer to location on file
                posting = ast.literal_eval(f.readline()) # save token and postings
                # posting[1] = { doc1: tf, doc2: tf, doc3: tf.... }
                temp_dict[posting[0]] = posting[1]
           #else:
                #  print("No word found in inverted_list")

    # do Boolean Retrieval first? + important text ? 
    # then calculate tf-idf scores + important text? 


    # for all documents in docid_index
    for doc_id in docid_index:
        for token in temp_dict:
        # get current document from token
            doc_id_int = int(doc_id)
            if doc_id_int in temp_dict[token]:
                temp_score =  temp_dict[token][doc_id_int] 

                # add important text to the score 
                if token in imp_temp_dict:
                    if doc_id_int in imp_temp_dict[token]:
                        temp_score += imp_temp_dict[token][doc_id_int]

                # check to see if the document is a .txt page? lower the values for these docs because they aren't valid "websites" 
                # might actually need to do a re.match/re.search for these values..
                if ".txt" in docid_index[doc_id] or "datasets" in docid_index[doc_id] \
                or ".sql" in docid_index[doc_id]:
                    temp_score *= 0.5 

                doc_score[doc_id_int] += temp_score

    # sort values to get best score first
    ret_val=sorted(doc_score.items(), key=lambda x: x[1], reverse = True)

    # print(ret_val[0])
    # print(type(ret_val[0]))

    url_list = []
    # retreive the actual url here 
    for temp_tuple in ret_val:
        url_list.append(docid_index[str(temp_tuple[0])])

    # stop timer
    stop_time = datetime.datetime.now() 
    elapsed_time = stop_time - start_time
    print( str(elapsed_time.total_seconds() * 1000) + " milliseconds" )

    # return top 20 results.
    return url_list[:20], elapsed_time.total_seconds() * 1000



# GET - A GET msg is sent and server returns data
# POST -  Send HTML form data to server. Data received POST 
@app.route('/', methods=['GET', 'POST'])
def search_page():
    results = []
    # Gets the search form from HTML  
    if request.method == 'POST':
        queries = request.form['query'] # get the user queries 
        queries = queries.lower().split()
        stemmed_query = []
        for query in queries:
            stemmed_query.append(stemmer.stem(query))

        # comment stop words implementation for now
        stop_words = stopwords.words('english')
        clean_queries = []
        for query in stemmed_query:
           if query not in stop_words:
            clean_queries.append(query)

        results, timer = retrieval(clean_queries) 

    return render_template("search_page.html", query=queries, timer=round(timer, 2), results=results)



# This is so you can just do py -3 webgui.py
if __name__ == '__main__':
    # store data in memory
    word_offsets = store_in_memory("word_offsets.txt")
    important_offset = store_in_memory("imptext_offsets.txt")

    with open("doc_id_map.txt", "r") as f:
        docid_index = json.load(f)

    app.run(debug = True)