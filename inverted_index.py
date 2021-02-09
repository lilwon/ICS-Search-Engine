"""
Create an inverted index for the corpus with data structures designed by you.
•Tokens:  all alphanumeric sequences in the dataset.

•Stop words:  do not use stopping while indexing, i.e.  use all words, eventhe frequently occurring ones.•Stemming: use stemming for better textual matches.  
               Suggestion: Porterstemming, but it is up to you to choose.


•Important text:  text in bold (b, strong), in headings (h1, h2, h3), andin  titles  should  be  treated  as  more  important  than  the  in  other  places.
Verify which are the relevant HTML tags to select the important words.

"""
import os # https://www.tutorialspoint.com/python/os_walk.htm
from collections import defaultdict 
from nltk.tokenize import RegexpTokenizer # use this to find tokens that are alphanumeric, but also numbers with decimals (but not next to letters) 



def inverted_index():
  
  index_dict = defaultdict(dict)
  
  for root, dirs, files in os.walk("./DEV"):
    for doc in files:
      doc_name = os.path.join(root,name)
      
      with open(doc_name, "r") as opened:
        content = opened.read() # will get an error using BeautifulSoup 
        parsed_file = BeautifulSoup(content, "html.parser")
        
        token_expression = '([1-9]\d*(.\d+)?)|\w+' # allow all alphanumeric characters, but if its a number, it will allow a decimal, but only if there is a number after it
        
          
          
          
        
  
  

