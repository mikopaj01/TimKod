import string
import random
import numpy as np
import sys

def generator(len, l):
    sen = ""
    for i in range(len):
        sen += random.choice(l)
    return sen


def avg_words(text):
    split_text = text.split(" ")
    sum = 0
    for word in split_text:
        sum += len(word)
    return sum / len(split_text)


def count_letter(text, alp):
    dic_alph = dict.fromkeys(alp, 0)
    for l in text:
        dic_alph[l] += 1
    return dic_alph


def create_sentence_using_probability(l, prob_dict):
    text = ''
    for i in range(l):
        text += random.choices(list(prob_dict.keys()), tuple(prob_dict.values()), k=1)[0]
    return text


def generate_dict_with_count(level, text):
    dictionary = {}
    for index, letter in enumerate(text[level:]):
        key = text[index: level + index]

        if not key in dictionary:
            dictionary[key] = {}

        if letter in dictionary[key]:
            dictionary[key][letter] += 1
        else:
            dictionary[key][letter] = 1

    return dictionary


def get_probabilities(dictionary):
    for key in dictionary:
        count = sum(dictionary[key].values())
        for childKey in dictionary[key]:
            if count != 0:
                dictionary[key][childKey] /= count
    return dictionary


def markov(textLen, level, data, alph):
    dictionary = generate_dict_with_count(level, data)
    probabilities_dict = get_probabilities(dictionary)

    text = data[:level]
    if level == 5:
        text = 'probability'

    for i in range(level, textLen):
        key = text[-level:]
        if key not in probabilities_dict:
            text += np.random.choice(alph)
        else:
            source = list(probabilities_dict[key].keys())
            probabilities = list(probabilities_dict[key].values())
            text += np.random.choice(source, p=probabilities)[0]

    return text


if __name__ == "__main__":
    filename = sys.argv[1]
    size = int(sys.argv[2])
    output_file_name = sys.argv[3]

    print("Zadanie 1")
    alphabet = list(string.ascii_lowercase)
    alphabet.append(" ")
    numbers = list(str(x) for x in range(0, 10))
    alphabet.extend(numbers)
    print(alphabet)
    sen = generator(size, alphabet)
    print(sen)
    print("Średnia długość słowa:")
    print(avg_words(sen), '\n')

    print("Zadanie 2")
    text_file = open(filename, "r")
    data = text_file.read()
    text_file.close()
    count_dict = count_letter(data, alphabet)
    print(count_dict)
    print("Prawdopodobieństwo:")
    probability = {}
    suma = 0
    for item in count_dict.items():
        print(str(item[0]) + " = " + str(item[1] / len(data)))
        probability[item[0]] = item[1] / len(data)

    print("\nZadanie 3")
    new_sen = create_sentence_using_probability(size, probability)
    print(new_sen)
    print('Średnia długość słowa = ', avg_words(new_sen))

    print('\nZadanie 4')
    dic_alph = generate_dict_with_count(1, data)
    dict_max = sorted(probability.items(), key=lambda x: x[1], reverse=True)[:2]
    for key, value in dic_alph.items():
        for letter, count in value.items():
            if dict_max[0][0] == key or dict_max[1][0] == key:
                print("'", letter, "'", " po ", "'", key, "'", " z prawdopodobienstwem ",
                      (count / len(data)) / probability[key])

    f = open(output_file_name, 'w')

    print('\nZadanie 5')
    f.write('\nZadanie 5\n')
    text = ''
    for index, level in enumerate(range(1, 6, 2)):
        text = markov(size, level, data, alphabet)
        print(f'\nPrzybliżenie {level} rzędu:\n')
        f.write(f'\n\nPrzybliżenie {level} rzędu:\n\n')
        print(text + '\n')
        f.write(text + '\n')
        print(f'Średnia długość słowa = {avg_words(text)}')
        f.write(f'\nŚrednia długość słowa = {avg_words(text)}')
    f.close()
