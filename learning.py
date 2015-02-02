import re
import sys
import random
import pickle
from collections import Counter
from collections import deque
from collections import defaultdict


def find_sentences(line):
    return re.findall(r"\w+|\.\.\.|\.|\?|!", line)


def is_punctuation_mark(word):
    return word in [".", "!", "?", "..."]


def miss_key():
    return Counter()


class WordsCounter:
    def __init__(self):
        self.statistics = defaultdict(miss_key)
        self.cur_words = deque()

    def add_word(self, word):
        if len(self.cur_words) == 0:
            self.cur_words.append(word)
            self.statistics[tuple()][word] += 1
            return

        if len(self.cur_words) == 1:
            self.cur_words.append(word)
            key = tuple([self.cur_words[0]])
            self.statistics[key][self.cur_words[1]] += 1
            return

        if len(self.cur_words) == 2:
            self.cur_words.append(word)
        else:
            self.cur_words.popleft()
            self.cur_words.append(word)

        pair_key = tuple([self.cur_words[1]])
        self.statistics[pair_key][self.cur_words[2]] += 1

        triple_key = tuple([self.cur_words[0], self.cur_words[1]])
        self.statistics[triple_key][self.cur_words[2]] += 1

    def erase_ptrs(self):
        self.cur_words.clear()

    def get_next_from_pairs(self, word):
        key = tuple([word])
        if key not in self.statistics.keys():
            return random.choice(self.statistics.keys())[0]
        return self.statistics[key].most_common(1)[0][0]

    def get_next_from_triples(self, first_word, second_word):
        key = tuple([first_word, second_word])
        if key not in self.statistics.keys():
            return random.choice(self.statistics.keys())[0]
        return self.statistics[key].most_common(1)[0][0]

    def preprocess(self, text_path):
        with open(text_path) as text_file:
            for line in text_file:
                for word in find_sentences(line):
                    self.add_word(word)
                    if is_punctuation_mark(word):
                        self.erase_ptrs()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "USAGE: learning.py <input_filepath> <pickle_info_filepath>"
        sys.exit(1)

    text_path = sys.argv[1]
    pickle_path = sys.argv[2]

    words_counter = WordsCounter()

    print "Input file processing"
    words_counter.preprocess(text_path)

    print "Saving data"
    with open(pickle_path, "wb") as pickle_file:
        pickle.dump(words_counter, pickle_file)
