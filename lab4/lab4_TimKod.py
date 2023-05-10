import string
import random
import numpy as np
import sys


def count_letter(text, alp):
    dic_alph = dict.fromkeys(alp, 0)
    for l in text:
        dic_alph[l] += 1
    return dic_alph


def generate_dict_with_count(level, text, choice):
    dictionary = {}
    for i in range(level, len(text)):
        if choice == "letters":
            key = text[i - level:i]
        elif choice == "words":
            key = ' '.join(text[i - level:i])
        if not key in dictionary:
            dictionary[key] = 1
        else:
            dictionary[key] += 1

    return dictionary


def get_probabilities(dictionary):
    count = sum(dictionary.values())
    for key in dictionary.keys():
        if count != 0:
            dictionary[key] /= count
    return dictionary


if __name__ == "__main__":
    files = [
        "norm_wiki_en.txt",
        "norm_wiki_la.txt",
        "sample0.txt",
        "sample1.txt",
        "sample2.txt",
        "sample3.txt",
        "sample4.txt",
        "sample5.txt"
    ]
    filename = "norm_wiki_en.txt"
    # size = int(sys.argv[2])
    # output_file_name = sys.argv[3]
    text_file = open(filename, "r")
    data = text_file.read()
    text_file.close()

    print("Zadanie 1")
    alphabet = list(string.ascii_lowercase)
    alphabet.append(" ")
    numbers = list(str(x) for x in range(0, 10))
    alphabet.extend(numbers)
    print(alphabet)
    prob = 1 / len(alphabet)
    alphabet_entropy = prob * np.log2(prob) * len(alphabet) * -1
    print("Entropia dla alfabetu: ", alphabet_entropy)

    count_dict = count_letter(data, alphabet)
    print(count_dict)
    text_entropy = np.sum([(value / len(data)) * np.log2(value / len(data)) for value in count_dict.values()]) * -1
    print("Entropia dla tekstu: ", text_entropy)

    # H(X|Y) = H(X,Y) - H(Y)
    # data = "bananas"
    for file in files:
        text_file = open(file, "r")
        data = text_file.read()
        text_file.close()
        for i in range(1, 6):
            print("Litery dla rzędu ", i, " pliku ", file)
            letter_dict_count = generate_dict_with_count(i, data, "letters")
            letter_dict_prob = get_probabilities(letter_dict_count)
            letter_dict_count_down = generate_dict_with_count(i - 1, data, "letters")
            letter_dict_prob_down = get_probabilities(letter_dict_count_down)
            h_x_y = np.sum([value * np.log2(value) for value in letter_dict_prob.values()]) * -1
            h_y = np.sum([value * np.log2(value) for value in letter_dict_prob_down.values()]) * -1
            final_entropy = h_x_y - h_y
            print(final_entropy if final_entropy >= 0 else 0)
            splitted_data = data.split(" ")
            print("Słowa dla rzędu ", i, " pliku ", file)
            words_dict_count = generate_dict_with_count(i, splitted_data, "words")
            words_dict_prob = get_probabilities(words_dict_count)
            words_dict_count_down = generate_dict_with_count(i - 1, splitted_data, "words")
            words_dict_prob_down = get_probabilities(words_dict_count_down)
            h_x_y = np.sum([value * np.log2(value) for value in words_dict_prob.values()]) * -1
            h_y = np.sum([value * np.log2(value) for value in words_dict_prob_down.values()]) * -1
            final_entropy = h_x_y - h_y
            print(final_entropy if final_entropy >= 0 else 0)
