import random                                                               #brings in premade code for random numbers etc
import cPickle as pickle
import os.path

def getCorpus():
    corpus = raw_input("Corpus text: ")
    if corpus[-4] == '.':
        corpus = corpus[0:-4]
    try:
        return open(corpus+'.txt', 'r'), corpus                             #load the text file in the program so it may be used
    except IOError:
        print 'No such .txt file. Try again.'
        getCorpus()

text, corpus = getCorpus()

wordlist = text.read().split()                                              #splits the raw text into individual words
database = {}                                                               #creates an empty dictionary

if os.path.exists(corpus + '.p'):
    database = pickle.load(open(corpus+'.p'))
else:
    for i in range(len(wordlist)-2):                                        #do the following to every item in the word list except the last two
        w1, w2, w3 = (wordlist[i], wordlist[i+1], wordlist[i+2])            #give the names w1, w2, and w3 to the next three words in the list
        key = (w1, w2)                                                      #the first two words are the 'key' to a dictionary; the third is the corresponding entry
        if key in database.keys():                                          #if the key is already in the list of word pairs
            database[key].append(w3)                                        #   then add the following word to the list of all possible following words
        else:                                                               #if the key is not in the list
            database[key] = [w3]                                            #   add the key, and the following word is its first entry
    pickle.dump(database, open(corpus+'.p', 'r'))

seed = database.keys()[random.randint(0, len(database.keys())-1)]           #pick a random key from the dictionary

stringlength = 500                                                          #this is the maximum number of words generated
gentext = []                                                                #this is an empty list that will contain the generated words in order

while len(gentext) < stringlength:                                          #while the number of words generated is less than the maximum, repeat this:
    gentext.append(seed[0])                                                 #   add the first word in the seed word pair to the list
    new = database[seed][random.randint(0, len(database[seed])-1)]          #   pick a random word from the seed key's entry
    
    seed = (seed[1], new)                                                   #   the new seed is the second word from the original key and the newly selected word

print " ".join(gentext)                                                     #output the generated text onto the screen, separating each word by a space
