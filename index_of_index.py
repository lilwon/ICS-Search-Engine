'''
    Index of the inverted index. 

    After the inverted index is merged/finalized. You would need to create another bookkeeping file 
    (possibly just another dictionary) that only contains the WORD and the position of the 
    word from the inverted index. 

'''
import ast

def index_of_inverted_index(file_name):
    new_index = {} # index that would return WORD @ position

    offset = 0  
    # get the inverted_index file 
    with open(file_name, "r") as f:
        for line in f:
            # get the file's current line information
            posting = ast.literal_eval(line)
            # save the token and position to a new dict
            new_index[posting[0]] = offset
            # move offset (file pointer position)
            offset += len(line)+1

    # return the index of the inverted index -> { token: numPos }
    return new_index 
