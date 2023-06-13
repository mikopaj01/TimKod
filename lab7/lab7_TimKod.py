import math
import os


def encode(text, max_codebook_length):
    codebook = {(i,): i for i in range(256)}
    last_code = 256

    encoded_data = []
    text = [char for char in text]

    prefix = (text[0],)
    for char in text[1:]:
        current_code = (*prefix, char)
        if current_code in codebook:
            prefix = current_code
        else:
            if last_code >= max_codebook_length:
                encoded_data.append(codebook[prefix])
                prefix = (char,)
                continue

            encoded_data.append(codebook[prefix])
            codebook[current_code] = last_code
            last_code += 1
            prefix = (char,)

    encoded_data.append(codebook[prefix])

    code_length = math.ceil(math.log2(last_code))
    fixed_length_codebook = {v: f'{v:0{code_length}b}' for k, v in codebook.items()}

    encoded_bitstring = ''.join(fixed_length_codebook[char] for char in encoded_data)
    encoded_bitstring += '0' * (8 - len(encoded_bitstring) % 8)

    encoded_bytes = bytearray()
    for i in range(0, len(encoded_bitstring), 8):
        encoded_bytes.append(int(encoded_bitstring[i:i + 8], 2))

    return bytes(encoded_bytes), code_length


def decode(encoded_bytes, code_length):
    code = {i: chr(i) for i in range(256)}
    last_code = 256
    decoded_bitstring = ''.join(f'{byte:08b}' for byte in encoded_bytes)

    result = bytearray()
    c = ''

    char_length = code_length

    chunks = [int(decoded_bitstring[i:i + char_length], 2) for i in range(0, len(decoded_bitstring), char_length)]
    old = chunks.pop(0)
    result.append(ord(code[old]))

    for chunk in chunks:
        if chunk in code:
            word = code[chunk]
        else:
            word = code[old] + c

        for char in word:
            result.append(ord(char))
        c = word[0]

        if last_code >= codebook_length:
            old = chunk
            continue

        code[last_code] = code[old] + c
        last_code += 1
        old = chunk

    return result


if __name__ == '__main__':
    files = ['wiki_sample.txt', 'norm_wiki_sample.txt', 'lena.bmp']
    size_dict = {}
    for file in files:
        print('Plik', file)
        filename, extension = file.split('.')
        max_codebook_lengths = {'12': 2 ** 12, '18': 2 ** 18, 'max': 2 ** 128}
        for variant, codebook_length in max_codebook_lengths.items():
            print('Wariant dlugosci kodu 2^', variant)
            with open(f'{filename}.{extension}', 'rb') as file:
                text = file.read()

            encoded_text, code_length = encode(text, codebook_length)
            print('Dlugosc kodu 2^', code_length)

            with open(f'output/{filename}_{variant}.bin', 'wb') as file:
                file.write(encoded_text)

            with open(f'output/{filename}_{variant}.bin', 'rb') as file:
                text = file.read()

            decoded_text = decode(text, code_length)
            with open(f'proof/{filename}_{variant}.{extension}', 'wb') as file:
                file.write(decoded_text)

            file_size = os.stat(f'output/{filename}_{variant}.bin').st_size
            size_dict[f'output/{filename}_{variant}.bin'] = file_size

    for key, val in size_dict.items():
        print(f"Rozmiar {key} to {val}")
