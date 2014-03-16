import random                                                               #brings in premade code for random numbers etc
import cPickle as pickle                                                    #code for saving databases between uses
import os.path                                                              #code to check if files exist

def getCorpus():                                                            #define a function to select a text file
    corpus = raw_input("Corpus text: ")                                     #have the user specify a text file
    if len(corpus) < 4 or corpus[-4] == '.':                                #check to see if the 4th to last character is a '.'(eg example.txt)
        corpus = corpus[0:-4]                                               #   if the above is true, remove the last 4 characters (.txt)
    try:                                                                    #try to do the following, unless there is an error:
        return open(corpus+'.txt', 'r'), corpus                             #   load the text file in the program so it may be used
    except IOError:                                                         #if there is an error (the file does not exist)
        print 'No such .txt file. Try again.'                               #   tell the user of the error
        getCorpus()                                                         #   try another input

text, corpus = getCorpus()                                                  #run the above function, saving both the name of the file and its contents

wordlist = text.read().split()                                              #splits the raw text into individual words
database = {}                                                               #creates an empty dictionary

if os.path.exists(corpus + '.p'):                                           #if the database file has already been created and is saved:
    database = pickle.load(open(corpus+'.p'))                               #   load the database so it does not have to be recreated
else:                                                                       #otherwise:
    for i in range(len(wordlist)-2):                                        #   do the following to every item in the word list except the last two
        w1, w2, w3 = (wordlist[i], wordlist[i+1], wordlist[i+2])            #   give the names w1, w2, and w3 to the next three words in the list
        key = (w1, w2)                                                      #   the first two words are the 'key' to a dictionary; the third is the corresponding entry
        if key in database.keys():                                          #   if the key is already in the list of word pairs
            database[key].append(w3)                                        #       then add the following word to the list of all possible following words
        else:                                                               #   if the key is not in the list
            database[key] = [w3]                                            #       add the key, and the following word is its first entry
    pickle.dump(database, open(corpus+'.p', 'w'))                           #   save the database for later use, much faster than recreating it each time

seed = database.keys()[random.randint(0, len(database.keys())-1)]           #pick a random key from the dictionary

stringlength = int(raw_input('How many words? '))                                #this is the maximum number of words generated as defined by the user
gentext = []                                                                #this is an empty list that will contain the generated words in order

while len(gentext) < stringlength:                                          #while the number of words generated is less than the maximum, repeat this:
    gentext.append(seed[0])                                                 #   add the first word in the seed word pair to the list
    new = database[seed][random.randint(0, len(database[seed])-1)]          #   pick a random word from the seed key's entry
    
    seed = (seed[1], new)                                                   #   the new seed is the second word from the original key and the newly selected word

print " ".join(gentext)                                                     #output the generated text onto the screen, separating each word by a space
