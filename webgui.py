import datetime
import json

from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

from flask import Flask, request, render_template
app = Flask(__name__) # used for app route 

# global in memory dictionaries for fast seek
stemmer = SnowballStemmer(language="english")
word_offsets = {}
important_offsets = {}
docid_index = {}

# wasn't sure if this was taking too much time. So used json.load instead
def store_in_memory(file_name):
    vals = {}
    with open(file_name, "r") as f:
        for line in f:
            some_dict = eval(line)
            vals[some_dict[0]] = some_dict[1]

    return vals

# returns a list of top urls for the query
def retrieval(queries):
    temp_dict = {}
    doc_score = defaultdict(float)
    imp_temp_dict = {}
    # start timer here
    start_time = datetime.datetime.now() 

    with open("important_text_inverted.txt", "r") as f, open("new_inverted_index.txt", "r") as g:
        for query in queries:
            if query in important_offsets:
            #if important_offsets.get(query) is not None: 
                pos = important_offsets[query]
                f.seek(pos)
                posting = eval(f.readline())
                imp_temp_dict[posting[0]] = posting[1]

            if query in word_offsets:
            #if word_offsets.get(query) is not None:
                pos = word_offsets[query]
                g.seek(pos)
                posting = eval(g.readline())
                temp_dict[posting[0]] = posting[1]


    # temp_dict: { token1: {docid1: tfidf...}, token2: {docid2: tfidf }}
    # take the doc_id keys from the temp_dict..
    # have a set to hold it
    '''
    temp_docids = set() 
    for key in temp_dict.values():
        for some_docid in key.keys():
            temp_docids.add(some_docid)
    '''

    temp_docids = sorted(list({some_docid for key in temp_dict.values() for some_docid in key.keys()}))

    #temp_docids = sorted(list(temp_docids))

    temp_dict = dict(sorted(temp_dict.items(), key=lambda x:len(x[1]))) 

    # for all documents in from temporary doc_ids
    # no longer searching through all documents, only relevant ones   
    for doc_id in temp_docids:
        for token in temp_dict:
        # get current document from token
            if doc_id in temp_dict[token]:
                temp_score =  temp_dict[token][doc_id] 

                # add important text to the score 
                if token in imp_temp_dict:
                    if doc_id in imp_temp_dict[token]:
                        temp_score += imp_temp_dict[token][doc_id] * 1.50

                # check to see if the document is a .txt page? lower the values for these docs because they aren't valid "websites" 
                # below takes too much time since it searches 55k docs 
                #if ".txt" in docid_index[doc_id] or "datasets" in docid_index[doc_id] \
                #or ".sql" in docid_index[doc_id]:
                #    temp_score *= 0.5 

                doc_score[doc_id] += temp_score

    # sort values to get best score first
    ret_val=sorted(doc_score.items(), key=lambda x: x[1], reverse = True)[:10]

    # print(ret_val[0])
    # print(type(ret_val[0]))

    '''

    url_list = []
    # retreive the actual url here 
    for temp_tuple in ret_val:
        url_list.append(docid_index[str(temp_tuple[0])])

    '''
    url_list = [docid_index[str(temp_tuple[0])] for temp_tuple in ret_val]

    # stop timer
    stop_time = datetime.datetime.now() 
    elapsed_time = stop_time - start_time
    print( str(elapsed_time.total_seconds() * 1000) + " milliseconds" )

    # return top 10 results.
    return url_list, elapsed_time.total_seconds() * 1000



# GET - A GET msg is sent and server returns data
# POST -  Send HTML form data to server. Data received POST 
@app.route('/', methods=['GET', 'POST'])
def search_page():
    results = []
    queries = []
    timer = 0 

    stop_words = stopwords.words('english')

    # Gets the search form from HTML  
    if request.method == 'POST':
        queries = request.form['query'] # get the user queries 
        queries = queries.lower().split()

        if not queries:
            # if user didnt enter anything return
            return render_template("search_page.html", query=queries, timer=round(timer, 2), results=results)        

        stemmed_query = set() 
        for query in queries:
            stemmed_query.add(stemmer.stem(query))

        # systematically remove stop words from queries if possible
        stopword_count = 0
        for query in stemmed_query:
            if query in stop_words:
                stopword_count += 1

        stemmed_query = list(stemmed_query)

        check_query = []
        # calculate if stopwords are more prevalent than other words
        if float(stopword_count/len(stemmed_query)) <= 0.50: 
            # remove the stop words from query
            for query in stemmed_query:
                if query not in stop_words:
                    check_query.append(query)
        else: # keep all the stopwords :(
            check_query = stemmed_query

        check_query = sorted(check_query, reverse=False)

        print(check_query)

        results, timer = retrieval(check_query) 

    return render_template("search_page.html", query=queries, timer=round(timer, 2), results=results)



# This is so you can just do py -3 webgui.py
if __name__ == '__main__':
    # store data in memory
    #word_offsets = store_in_memory("word_offsets.txt")
    with open("word_offsets.txt", "r") as offset1:
        word_offsets = json.load(offset1)

    #important_offset = store_in_memory("imptext_offsets.txt")
    with open("imptext_offsets.txt", "r") as offset2:
        important_offsets = json.load(offset2)

    with open("doc_id_map.txt", "r") as f:
        docid_index = json.load(f)

    app.run(debug = True)