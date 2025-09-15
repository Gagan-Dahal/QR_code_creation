NUMERIC = 1
ALPHA_NUMERIC = 2
BYTE = 4
KANJI = 8
MAX_BYTES_MESSAGE = 14 #with version 1 and error correction level Medium
DATA_CODEWORD_LEN = 16
PAD_BYTES = [0XEC, 0X11]

def to_byte(value, bit_length):
    return format(value, f'0{bit_length}b')

def encode(string_input):
    data_type = BYTE
    char_count = 0

    char_count = len(string_input)
    if char_count >MAX_BYTES_MESSAGE:
        raise RuntimeError("Invalid Input")

    bit_stream = to_byte(data_type, 4)
    bit_stream += to_byte(char_count, 8)

    for x in string_input:
        bit_stream += to_byte(ord(x), 8)

    #Adding terminators to signal end of data words, at max 4 bits
    max_bits_message = MAX_BYTES_MESSAGE*8          
    rem_bits = min(4, max_bits_message - len(bit_stream))
    bit_stream += '0'*rem_bits

    while len(bit_stream) % 8 != 0: #Not needed in byte mode but may be needed in other modes to make the bit stream a multiple of 8
        bit_stream += '0'


    data_codeword = [int(bit_stream[i:i+8], 2) for i in range(0, len(bit_stream), 8)] #Data word paired in groups of 8 and converted into integer

    alternate = 0
    while len(data_codeword) < DATA_CODEWORD_LEN: #Pad the message to the maximum limit
        data_codeword.append(PAD_BYTES[alternate%2])
        alternate += 1

    return data_codeword

