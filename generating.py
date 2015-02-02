import random
import sys
import pickle

from learning import WordsCounter
from learning import is_punctuation_mark
from learning import miss_key

MIN_SENTENCES_IN_PARAGRAPH = 1
MAX_SENTENCES_IN_PARAGRAPH = 10

MIN_COMMON_COUNTER = 100
MAX_COMMON_COUNTER = 5000


class TextGenerator:
    def __init__(self, _words_counter):
        self.words_counter = _words_counter

    def generate_sentence(self):
        sentence = list()
        punctuation_mark = str()

        common_counter = random.randint(MIN_COMMON_COUNTER,
                                        MAX_COMMON_COUNTER)
        first_words = words_counter.statistics[tuple()]
        prev_word = random.choice(first_words.most_common(common_counter))[0]
        sentence.append(prev_word)

        word = words_counter.get_next_from_pairs(prev_word)
        if is_punctuation_mark(word):
            punctuation_mark = word
        else:
            sentence.append(word)

        words = 2
        while not is_punctuation_mark(word):
            generated_word = \
                words_counter.get_next_from_triples(prev_word, word)
            if is_punctuation_mark(generated_word):
                punctuation_mark = generated_word
                break
            sentence.append(generated_word)
            prev_word = word
            word = generated_word

            words += 1
            if words >= 30:
                punctuation_mark = "."
                break

        new_sentence = " ".join(sentence)
        return "".join([new_sentence, punctuation_mark])

    def generate_paragraph(self, sentence_number):
        paragraph = list()
        for i in range(sentence_number):
            paragraph.append(self.generate_sentence())
        paragraph.append("\n")
        return " ".join(paragraph)

    def generate_text(self, paragraph_number):
        text = list()
        for i in range(paragraph_number):
            sentence_number = random.randint(MIN_SENTENCES_IN_PARAGRAPH,
                                             MAX_SENTENCES_IN_PARAGRAPH)
            text.append(self.generate_paragraph(sentence_number))
        return "".join(text)


def generate_text(words_counter, generated_text_path, paragraphs):
    text_generator = TextGenerator(words_counter)
    with open(generated_text_path, "w+") as output_file:
        output_file.write(text_generator.generate_text(paragraphs))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "USAGE: generating.py <output_filepath>" \
              "<paragraph_number> <pickle_info_filepath>"
        sys.exit(1)

    generated_text_path = sys.argv[1]
    paragraphs = int(sys.argv[2])
    pickle_path = sys.argv[3]

    print "Loading data"
    with open(pickle_path, "rb") as pickle_file:
        words_counter = pickle.load(pickle_file)

    print "Generating text"
    generate_text(words_counter, generated_text_path, paragraphs)
