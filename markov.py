import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    return " ".join(words)

def split_chain(chains):
    """Takes in string, and returns a string that is less than 140 characters"""
    char_count = 0
    character_limit = 140
    final_string = ""

    # todo : FINAL_STRING = CHAINS[:139]
    for i in range(len(chains)):
        if i < character_limit:
            final_string = final_string + chains[i]
            # print chains[i]
        else:
            break 


    return final_string
    



def tweet(chains, my_dict):
    """Takes in string and tweets it to our twitter acount"""

    api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print api.VerifyCredentials()

    user_input = raw_input("Enter to tweet again [q to quit] > ")
    while user_input != "q":
        final_string = make_text(my_dict)
        chains = split_chain(final_string)
        status = api.PostUpdate(chains)
        print status.text
        if user_input == "q":
            break
        else:
            user_input = raw_input("Enter to tweet again [q to quit] > ")
           

            

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
  
    # to make sure these environmental variables are set.

# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

# Get a Markov chain

final_string = make_text(chains)
chains_1 = split_chain(final_string)
tweet(chains_1, chains)
   
# TODO 3 THINGS
# Create Robertina mashup! Use a different .txt file for the text generator
# use a while loop in the main to call our functions (take out of tweet function)
# use a slice in our make_function chains[:139] instead of split_chain function

# optional
# be creative with where you end your text! i.e. punctuation marks?

