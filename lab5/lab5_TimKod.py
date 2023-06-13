import time
import math
import bitarray


def create():
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', ' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    code_length = math.ceil(math.log2(len(alphabet)))
    codebook = {}
    for i in range(len(alphabet)):
        binary_code = bin(i)[2:].zfill(code_length)
        codebook[alphabet[i]] = binary_code
    return codebook


def decode(encode_text, start_code):
    decoded_text = ''
    symbol_length = len(list(start_code.values())[0])  # długość symbolu kodu (stała długość kodu)
    code = {v: k for k, v in start_code.items()}
    for i in range(0, len(encode_text), symbol_length):
        symbol = encode_text[i:i+symbol_length]
        decoded_text += code[symbol]

    return decoded_text


def encode(text, code):
    encoded_text = []
    for symbol in text:
        encoded_text.append(code[symbol])
    return "".join(encoded_text)


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


if __name__ == "__main__":
    start = time.time()
    code = create()
    text_file = open("norm_wiki_sample.txt").read()
    # text_file = "dwaomnfosi owa"
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
    end = time.time()
    print("Czas trwania programu: ", end - start)
