from enum import Enum

class Tokens(Enum):
    start = '__start__'
    end = '__end__'

class Words():
    def __init__(self, database = None):
        # set of known words
        self._dictionary = set( [ Tokens.start.value, Tokens.end.value ] )
        # map from word to id
        self._words_ids = { word: index for index, word in enumerate(self._dictionary) }
        # id's for words
        self._words_vector = { index: word for word, index in self._words_ids.items() }
        self._database = None
        if database:
            self._database = database
            import pickle
            self._dictionary, self._words_ids, self._words_vector = pickle.load(open(self._database, "rb"))

    @staticmethod
    def brown_corpus():
        w = Words()
        import nltk
        for word in nltk.corpus.brown.words():
            w += word
        return w

    def __len__(self):
        return len(self._dictionary)

    def __getitem__(self, key):
        if isinstance(key, (int, long)):
            return self._words_vector[key]
        else:
            key = key.lower()
            return self._words_ids[key]

    def __iadd__(self, word):
        if word not in self._dictionary:
            word = word.lower()
            last_index = len(self._dictionary)
            self._dictionary.add(word)
            self._words_ids[word] = last_index
            self._words_vector[last_index] = word
        return self

    def close(self, database = None):
        """If opened from database will persist it"""
        import pickle
        if self._database or database:
            target = self._database or database
            pickle.dump( [ self._dictionary, self._words_ids, self._words_vector ], open(target, "wb" ))
