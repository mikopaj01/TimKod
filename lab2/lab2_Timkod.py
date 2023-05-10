import string
import random
import numpy as np
import sys
import itertools


def generate_dict_with_count(level, text):
    dictionary = {}
    for index, word in enumerate(text[level:]):
        key = ' '.join(text[index: level + index])
        if not key in dictionary:
            dictionary[key] = {}
        if word in dictionary[key]:
            dictionary[key][word] += 1
        else:
            dictionary[key][word] = 1

    return dictionary


def get_probabilities(dictionary):
    for key in dictionary:
        count = sum(dictionary[key].values())
        for childKey in dictionary[key]:
            if count != 0:
                dictionary[key][childKey] /= count
    return dictionary


def markov(textLen, level, data):

    if level == 3:
        level = 2
        dictionary = generate_dict_with_count(level, data)
        probabilities_dict = get_probabilities(dictionary)
        text = 'probability of '
        text_list = ['probability', 'of']
    else:
        dictionary = generate_dict_with_count(level, data)
        probabilities_dict = get_probabilities(dictionary)
        text_list = random.choice(list(probabilities_dict.keys())).split(' ')
        text = " ".join(text_list) + " "

    for i in range(level, textLen):
        key = ' '.join(text_list[-level:])
        if key not in probabilities_dict:
            word = random.choice(list(probabilities_dict.keys()))
            text += word + " "
            text_list.append(word)
        else:
            source = list(probabilities_dict[key].keys())
            probabilities = list(probabilities_dict[key].values())
            word = np.random.choice(source, p=probabilities)
            text += word + " "
            text_list.append(word)

    return text


def create_sentence_using_probability(l, prob_dict):
    text = ''
    for i in range(l):
        word = random.choices(list(prob_dict.keys()), tuple(prob_dict.values()), k=1)[0]
        text += word + " "

    return text


def count_identical_words(text):
    words = text.split(" ")
    num = len(words)
    word_count = {}
    for word in words:
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1
    return dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True)), num


def first_n_elements(dictionary, n):
    return itertools.islice(dictionary.values(), n)


if __name__ == "__main__":
    filename = sys.argv[1]
    size = int(sys.argv[2])
    output_file_name = sys.argv[3]

    print("Zadanie 1")
    text_file = open(filename, "r")
    data = text_file.read()
    text_file.close()
    dict_word, words_num = count_identical_words(data)
    dict_word_percentage = {key: value / words_num for key, value in dict_word.items()}
    print("Liczba wyrazów w tekście: ", words_num)
    print("Liczba unikalnych wyrazów: ", len(dict_word))
    percent_6k = sum(first_n_elements(dict_word_percentage, 6000))
    percent_30k = sum(first_n_elements(dict_word_percentage, 30000))
    print("Procent pierwszych 6000 wyrazow:", percent_6k)
    print("Procent pierwszych 30000 wyrazow:", percent_30k)

    print("\nZadanie 2")
    gen_text = create_sentence_using_probability(size, dict_word_percentage)
    print(gen_text)

    f = open(output_file_name, 'w')
    text = data.split(" ")
    for i in range(3):
        print(f"\nZadanie 3.{i + 1}\n")
        f.write(f"\nZadanie 3.{i + 1}\n")
        gen_text = markov(size, i + 1, text)
        print(gen_text + '\n')
        f.write(gen_text + '\n')


