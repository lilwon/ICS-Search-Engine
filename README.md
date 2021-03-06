# INF_141/CS 121 - Building a Search Engine
Milestone 1: Index construction <br>
Milestone 2: Search Retrieval construction <br>
Milestone 3: Working Prototype of a Search Engine <br>


## Starting the Indexer 
Install the following python libraries through the command prompt:<br> 
- Beautifulsoup <br> 
- nltk <br> 
- flask <br> 



**The following files should be created from our indexer prior to starting the search engine:** <br>

1. doc_id_map.txt<br>
2. important_text_inverted.txt<br>
3. imptext_offsets.txt<br>
4. merged_index.txt<br>
5. new_inverted_index.txt<br>
6. partial_index_1.txt<br>
7. partial_index_2.txt<br>
8. partial_index_3.txt<br>
9. word_offsets.txt<br>
 

To run the indexer (on Windows), run the command prompt and input py -3 inverted_index.py <br> 

## Starting up the Search Engine
**Only do this if it's necessary** <br>
Follow the [Flask installation page](https://flask.palletsprojects.com/en/1.1.x/installation/) 
to set up and activate the envrionment, then install Flask. <br> 

To start the search engine, enter 
`py -3 webgui.py`
on your command prompt or terminal. 

After everything has finished loading, you can now access the web site through your browser with the following url: http://127.0.0.1:5000/ 
