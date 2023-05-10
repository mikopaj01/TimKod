from bitarray import bitarray
import math


def create():
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', ' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    code_length = math.ceil(math.log2(len(alphabet)))
    codebook = {}
    for i in range(len(alphabet)):
        binary_code = bin(i)[2:].zfill(code_length)
        codebook[alphabet[i]] = bitarray(binary_code)
    return codebook


def decode(encode_text, code):
    decoded_text = ''
    symbol_length = len(list(code.values())[0])  # długość symbolu kodu (stała długość kodu)
    for i in range(0, len(encode_text), symbol_length):
        symbol = encode_text[i:i+symbol_length]
        for key, value in code.items():
            if value.to01() == symbol:
                decoded_text += key
                break
    return decoded_text


def encode(text, code):
    encoded_text = ""
    for symbol in text:
        encoded_text += code[symbol].to01()
    return encoded_text


def save(code_file_name, code, bin_file_name, encode_text):
    with open(code_file_name, 'w') as result:
        for text, num in code.items():
            result.write(text + ";" + str(num.to01()) + ";")

    with open(bin_file_name, 'w') as bin_file:
        bin_file.write(encode_text)


def load(code_file_name, bin_file_name):
    code_file = open(code_file_name).read()
    splitted_code = code_file.split(";")
    code = {}
    for i in range(0, len(splitted_code) - 1, 2):
        code[splitted_code[i]] = bitarray(splitted_code[i + 1])

    with open(bin_file_name, 'r') as fh:
        text = fh.read()
    return text, code


def compression_ratio(text, codebook):
    uncompressed_length = len(text) * 8
    compressed_length = 0
    for symbol in text:
        compressed_length += len(codebook[symbol])
    return uncompressed_length / compressed_length


if __name__ == "__main__":
    code = create()
    text_file = open("norm_wiki_sample.txt").read()
    encode_text = encode(text_file, code)
    decode_text = decode(encode_text, code)
    print("Czy tekst po zakodowaniu i zdekodowaniu ten sam? ", text_file == decode_text)
    save("code.txt", code, "encoded_text.txt", encode_text)
    # sprawdzenie ładowania danych z pliku
    encode_text, code = load("code.txt", "encoded.txt")
    decode_text_from_file = decode(encode_text, code)
    print("Czy tekst po zakodowaniu i zdekodowaniu ten sam (z pliku)? ", text_file == decode_text_from_file)
    print("Współczynnik kompresji wynosi: ", compression_ratio(text_file, code))
