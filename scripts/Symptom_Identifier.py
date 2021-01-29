import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

# importing symptoms
symptoms = pd.read_json('data/symptoms.json', orient = 'table')

def remove_punctuations(text, punctuations = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~�0123456789®'):
    ''' remove punctuations '''
    table_ = str.maketrans(punctuations, ' '*len(punctuations))
    return text.translate(table_)

def ascii_only(text):
    ''' remove non-ascii words '''
    return text.encode("ascii", "ignore").decode()

def lemmatize(word):
    ''' lemmatize text'''
    wnl = WordNetLemmatizer()
    return wnl.lemmatize(word)

def spell_correct(text, corpus):
    ''' 
    INPUT: a string object 
    RETURN: new corrected string
    '''
    
    # for each word in text
    corrected = []
    for word in text.split():
        if word not in corpus:
            corrected.append(str(TextBlob(word).correct()))
        else:
            corrected.append(word)
    return ' '.join(corrected)

def break_sentence(text):
    '''
    INPUT: a string object
    RETURN: break sentence
    '''
    new_text = re.sub(r"\n", ". ", text)
    return re.sub(r"(\W*)(and|or|,|&|;)(\W)+", r". \3", new_text)

def preprocess_full_text(text, corpus, sw = ['i', 'me', 'my', 'myself', 'we', 'our',
                         'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your',
                         'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
                         "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
                         'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
                         'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
                         'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but',
                         'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
                         'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
                         'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                         'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
                         'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
                         'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
                         's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now',
                         'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
                         'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven',
                         "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't",
                         'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn',
                         "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'felt', 'feel', 'feels'], 
                        sentence_break = True):
    '''
    Takes a text as an input
    Preprocess (remove punctuations, turn lower case, lemmatize, remove stop words)
    Return a dictionary of sentence tokens ({1: sentence}) and a nested tokens [[tokens], ...]
    '''
    if isinstance(text, str):
        text = ascii_only(text.lower())
        
        if sentence_break:
            text = break_sentence(text)
        
        text_tokens = []
        sent_tokens = {}
        for i, sentence in enumerate(sent_tokenize(text)): 
            cl_sentence = remove_punctuations(sentence)
            cl_sentence = spell_correct(cl_sentence, corpus)
            tokens = word_tokenize(cl_sentence)
            token_set = set(lemmatize(word) for word in tokens if word not in sw)
            
            # only keep words in the corpus
            token_set = corpus & token_set
            token_set = list(token_set)
            text_tokens.append(token_set)
            sent_tokens[i] = sentence
        return sent_tokens, text_tokens
    else: 
        return 'no input'
    
def get_avg_vectors(text, model, corpus, sentence_break = True):
    '''
    INPUT
    =====
    text: str
    model: Word2Vec embedding model
    RETURN
    =====
    
    '''
    if isinstance(text, str):
        sent_tokens, text_input = preprocess_full_text(text, corpus, sentence_break = sentence_break)
    else:
        print("Input text must be a string")
        return
        
    avg_vec = []
    
    for sentence in text_input:

        vectors = []
        
        for word in sentence:

            try:
                vectors.append(model[word])
                
            except KeyError:
                print(f'{word} does not exist.')
                continue
                
        avg = np.average(vectors, axis = 0)
        avg_vec.append(avg)
        
    return sent_tokens, avg_vec

# for each sentence, see how close they are to target symptoms

def identify_symptom(text, symptom_vectors, model, corpus, threshold = 0.5):
    '''
    Find the closest symptom per sentences
    '''
    sent_tokens, avg_vec = get_avg_vectors(text, model, corpus)
    reference = {} # {1: {sentence: [(symptom, similarity), ...]}
    #pred_symptoms = {} 

    for i, sent_vec in enumerate(avg_vec): 
        
        similarity_list = []
        
        for symp, sym_vec in symptom_vectors.items():
            # get similarity between symptom and sentence
            similarity = 1 - cosine(sent_vec, sym_vec)
            if similarity > threshold: 
                similarity_list.append((symp, round(similarity, 3)))
            
        reference[i] = {sent_tokens[i] : [x for x in sorted(similarity_list, 
                                                            key = lambda v: v[1], 
                                                            reverse = True)]}
    # get the highest similarity list
    vals = [x[0] for x in [list(x.values()) for x in reference.values()] if x[0]]

    # check if it predicted ANY symptom
    if vals: 
        first_options = set(x[0][0] for x in vals)
        second_options = set(x[1][0] for x in vals if len(x) > 1)
        second = second_options - first_options
        return first_options, len(second) > 0 and second or None, reference
        
    else: 
        print('no symptom was detected')
        return ['No symptom detected'], None, reference
    

