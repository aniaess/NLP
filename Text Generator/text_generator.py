from nltk.tokenize import WhitespaceTokenizer
import nltk, random
filename = "corpus.txt"


def read_file():
    with open(filename, encoding="utf-8") as file:   # open corpus.txt file
        content = file.read()
        return content

def tokenization():
    content = read_file()
    wpt = WhitespaceTokenizer()   # tokens are separated by whitespace characters such as spaces, tabulation,
    words = wpt.tokenize(content)  # and newline characters
    return words

def create_bigrams():
    words = tokenization()
    bigrms = list(nltk.bigrams(words))
    return bigrms

def choose_first_word(words):
    word = random.choice(words)
    while word[0] != word[0].capitalize() or ("." in word[0] or "?" in word[0] or "!" in word[0]):
        word = random.choice(words)
    return " ".join(word)

def create_freq_dict(list_of_bigram):  # create a model that will consider all the possible transitions from one word to another and choose the most probable one based on the previous word.
    freq_dictionary = {}
    for i in range(len(list_of_bigram) - 1):
        freq_dictionary.setdefault(" ".join(list_of_bigram[i]), {}).setdefault(list_of_bigram[i + 1][1], 0)
        freq_dictionary[" ".join(list_of_bigram[i])][list_of_bigram[i + 1][1]] += 1
    return freq_dictionary

def capitalize_word(word, freq_dict):
    x = word
    word = random.choices(tuple(freq_dict[word]), weights=tuple(freq_dict[word].values()))[0]  # select the most probable tail from the list of possible tails
    while word[0] != word[0].capitalize() or ("." in word or "?" in word or "!" in word):  # based on the corresponding repetition counts. World must starts with big letter
          word = random.choices(tuple(freq_dict[x]), weights=tuple(freq_dict[x].values()))[0] # and not ends with punctuation marks
    return word

def create_sentences(): # generating pseudo-random text based on Markov chains.
    list_of_bigram = create_bigrams() # Transform the corpus into a collection of bigrams
    word = choose_first_word(list_of_bigram)
    freq_dictionary = create_freq_dict(list_of_bigram)
    text = []
    x = ""
    while len(text) < 10: # Generate and print exactly 10 pseudo-sentences
        sentence = [word]
        if x:
            word = x[1] + " " + word
        while True:
            if len(sentence) >= 5 and ("." in word[-1] or "!" in word[-1] or "?" in word[-1]):
                break # sentence should not be shorter than 5 tokens and always end with a sentence-ending punctuation mark like
            else:
                next_word = random.choices(tuple(freq_dictionary[word]),  weights=tuple(freq_dictionary[word].values()))[0]
                sentence.append(next_word)
                word = word.split()[1] + " " + next_word
        x = word.split()
        word = capitalize_word(word, freq_dictionary)
        sentence = " ".join(sentence)
        text.append(sentence)
    text = "\n".join(text)
    print(text)

create_sentences()
