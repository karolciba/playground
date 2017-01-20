from enum import Enum

class Tokens(Enum):
    start = '__start__'
    end = '__end__'

class Words():
    def __init__(self, database = None):
        # set of known words
        tokens = [ Tokens.start.value, Tokens.end.value ]
        # map from word to id
        self._words = { word: index for index, word in enumerate(tokens) }
        # id's for words
        self._words_vector = [ word for word in tokens ]

        self._count = len(self._words)
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
            return self._words[key]

    def __iadd__(self, word):
        word = word.lower()
        if word not in self._words:
            self._words[word] = self._count
            self._count += 1
            self._words_vector.append(word)
        return self

    def close(self, database = None):
        """If opened from database will persist it, optinally save to specified file"""
        import pickle
        if self._database or database:
            target = self._database or database
            pickle.dump( [ self._dictionary, self._words_ids, self._words_vector ], open(target, "wb" ))
