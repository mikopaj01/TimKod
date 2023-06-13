import numpy as np
import bitarray
import time

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', ' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

class HuffmanTree:

    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child

    def children(self):
        return self.left_child, self.right_child


def count_letter(text, alp):
    dic_alph = dict.fromkeys(alp, 0)
    for l in text:
        dic_alph[l] += 1
    return sorted(dic_alph.items(), key=lambda x: x[1], reverse=True)


def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d


def create(text):
    nodes = count_letter(text, alphabet)

    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = HuffmanTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    huffmanCode = huffman_code_tree(nodes[0][0])

    return huffmanCode


def decode(encode_text, code):
    decoded_text = ''
    inv_code = {v: k for k, v in code.items()}
    start = 0
    for i in range(0, len(encode_text) + 1):
        if encode_text[start:i] in inv_code.keys():
            decoded_text += inv_code[encode_text[start:i]]
            start = i
    return decoded_text


def encode(text, code):
    encoded_text = ""
    for symbol in text:
        encoded_text += code[symbol]
    return encoded_text


def save(code_file_name, code, bin_file_name, encode_text):
    with open(code_file_name, 'w') as result:
        for text, num in code.items():
            result.write(text + ";" + str(num) + ";")

    bits = bitarray.bitarray(encode_text)

    with open(bin_file_name, 'wb') as bin_file:
        bits.tofile(bin_file)



def load(code_file_name, bin_file_name, len_text):
    code_file = open(code_file_name).read()
    splitted_code = code_file.split(";")
    code = {}
    for i in range(0, len(splitted_code) - 1, 2):
        code[splitted_code[i]] = splitted_code[i + 1]

    bits = bitarray.bitarray()
    with open(bin_file_name, 'rb') as bin_file:
        bits.fromfile(bin_file)
    text = bits.to01()[:len_text]

    return text, code


def compression_ratio(text, codebook):
    uncompressed_length = len(text) * 8
    compressed_length = 0
    for symbol in text:
        compressed_length += len(codebook[symbol])
    return uncompressed_length / compressed_length


def avg_length(code, text_len, count_dict):
    avg = np.sum([(int(val[1]) / text_len) * len(code[val[0]]) for val in count_dict])
    return avg


if __name__ == "__main__":
    start = time.time()
    text_file = open("norm_wiki_sample.txt").read()
    code = create(text_file)
    encode_text = encode(text_file, code)
    decode_text = decode(encode_text, code)
    print("Czy tekst po zakodowaniu i zdekodowaniu ten sam? ", text_file == decode_text)
    save("code.txt", code, "encoded_text.bin", encode_text)
    # sprawdzenie ładowania danych z pliku
    len_text = len(encode_text)
    encode_text, code = load("code.txt", "encoded_text.bin", len_text)
    decode_text_from_file = decode(encode_text, code)
    print("Czy tekst po zakodowaniu i zdekodowaniu ten sam (z pliku)? ", text_file == decode_text_from_file)
    print("Współczynnik kompresji wynosi: ", compression_ratio(text_file, code))
    count_dict = count_letter(text_file, alphabet)
    len_text = len(text_file)
    avg_length_code = avg_length(code, len(text_file), count_dict)
    print("Średnia długość słów kodowych: ", avg_length_code)
    text_entropy = np.sum([(value[1] / len_text) * np.log2(value[1] / len_text) for value in count_dict]) * -1
    print("Entropia: ", text_entropy)
    print("Efektywność kodowania: ", text_entropy / avg_length_code)
    end = time.time()
    print("Czas trwania programu: ", end - start)

