from collections import Counter
import words

def pairwise(iter):
    """Pariwise generator from iterator, yields element (1st, 2nd), (2nd, 3rd), ... (n-1st, nst)"""
    from itertools import tee, izip
    it, it_next = tee(iter)
    next(it_next)
    for first, second in izip(it, it_next):
        yield first, second

class Model():
    def __init__(self):
        # keep number of observed transitions ("from_word", "to_word") =  #transitions
        self._transitions = Counter()

        self._words = words.Words()

    def train(self):
        import nltk

        self._words = words.Words.brown_corpus()

        observed_transitions = Counter()

        for sentence in nltk.corpus.brown.sents():
            # traverse pairs: word->next_word
            sentence.insert(0,words.Tokens.start.value)
            sentence.append(words.Tokens.end.value)

            for word, next_word in pairwise(sentence):
                index = (word.lower(), next_word.lower())
                observed_transitions[index] += 1


def train():
    from collections import Counter
    markov = Counter()
    dictionary = set()
    sums = Counter()

    import nltk
    from itertools import tee, chain

    sententes_count = len(nltk.corpus.brown.sents())
    counter = 0

    for sentence in nltk.corpus.brown.sents():
        line = "\rDictionary buildind Processing sentence %d of %d" % (counter,sententes_count)
        # print (line, end='')
        counter+=1
        sys.stdout.flush()
        for word in sentence:
            dictionary.add(word.lower)

    # smoothing
    for word in chain(['__start__'], dictionary):
        for next_word in dictionary:
            markov[word, next_word] += 1

    for word in dictionary:
        markov[word, '__end__'] += 1

    counter = 0
    for sentence in nltk.corpus.brown.sents():

        # print ("\rProcessing sentence {} of {} text: {}".format(counter,sententes_count, sentence)) ,
        line = "\rProcessing sentence %d of %d" % (counter,sententes_count)
        # print (line, end='')
        counter+=1
        sys.stdout.flush()

        sentence.insert(0,words.Tokens.start.value)
        sentence.append(words.Tokens.end.value)

        it, it_next = tee(sentence)
        next(it_next)
        for word, next_word in zip(it, it_next):

            # word_index = w[word]
            # next_word_index = w[next_word]
            # markov[word_index,next_word_index] += 1
            markov[word.lower(),next_word.lower()] += 1
            sums[word.lower()] += 1

            dictionary.add(word.lower())

    for pair in markov:
        markov[pair] = markov[pair]/float(sums[pair[0]])

    return markov

def save_model(model, filename="model_markov.pickle"):
    import pickle
    pickle.dump(model, open(filename, "wb"))

def load_model(filename="model_markov.pickle"):
    import pickle
    return pickle.load(open(filename, "rb"))

def find_max_next(word, model):
    # row = ( ('from_word', 'to_word'), occurences)
    row = max( [(k,v) for k,v in model.items() if k[0] == word], key = lambda x: x[1])
    return row[0][1]

def find_rand_next(word, model):
    import numpy as np
    # row = ( ('from_word', 'to_word'), occurences)
    rows =  [(k,v) for k,v in model.items() if k[0] == word]
    words = [ i[0][1] for i in rows ]
    dist = [ i[1] for i in rows ]
    # already normalized
    # s = float(sum(dist))
    # dist = [ i/s for i in dist ]
    # import pdb; pdb.set_trace()
    rand_row = np.random.choice(words, p=dist)
    return rand_row

def max_path(model, start = "__start__"):
    pass

def max_sentence(model):
    import string

    start = "__start__"
    sentence = []
    next_word = find_rand_next(start, model)
    guard = 0
    while next_word != "__end__":
        # print("\r" + string.join(sentence), end='')
        sys.stdout.flush()

        sentence.append(next_word)
        next_word = find_rand_next(next_word, model)
        guard += 1
        if guard > 50:
            break

    return sentence
