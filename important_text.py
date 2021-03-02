def important_text(parsed_file):
    b = parsed_file.get_text('b')
    bold_tokens = ''.join(b.stripped_strings) 
    strong = parsed_file.get_text('strong')
    strong_tokens = ''.join(strong.stripped_strings) 
    h1 = parsed_file.get_text('h1')
    h1_tokens = ''.join(h1.stripped_strings)
    h2 = parsed_file.get_text('h2')
    h2_tokens = ''.join(h2.stripped_strings) 
    h3 = parsed_file.get_text('h3')
    h3_tokens = ''.join(h3.stripped_strings) 
    body = parsed_file.get_text('body')
    body_tokens = ''.join(body.stripped_strings) 

    final_dict = defaultdict(int) # token : weighted_val
    val_return = defaultdict(int)



    bold_tokens =re.split(r"[^0-9a-zA-Z]+", bold_tokens)
    for term in bold_tokens: 
        term = term.lower()
        if term in final_dict:
            final_dict[term]+= 6
        else:
            final_dict[term] = 6
        
    
    strong_tokens =re.split(r"[^0-9a-zA-Z]+", strong_tokens)
    for term in strong_tokens:
        term = term.lower()
        if term in final_dict:
            final_dict[term]+= 5
        else:
            final_dict[term] = 5 
    
    h1_tokens =re.split(r"[^0-9a-zA-Z]+", h1_tokens)
    for term in h1_tokens: 
        term = term.lower()
        if term in final_dict:
            final_dict[term]+= 4
        else:
            final_dict[term] = 4

    
    h2_tokens =re.split(r"[^0-9a-zA-Z]+", h2_tokens)
    for term in h2_tokens: # need to implement proper tokenizer
        term = term.lower()
        if term in final_dict:
            final_dict[term]+= 3
        else:
            final_dict[term] = 3 
    
    h3_tokens =re.split(r"[^0-9a-zA-Z]+", h3_tokens)
    for term in h3_tokens: # need to implement proper tokenizer
        term = term.lower()
        if term in final_dict:
            final_dict[term]+= 2
        else:
            final_dict[term] = 2 


    for key,val in final_dict:
        val_return[key] += log10(val)

    return val_return 

