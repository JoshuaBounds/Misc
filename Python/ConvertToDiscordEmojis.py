
table = {
    'q': ':black_circle:',
    'w': ':blue_circle:',
    'e': ':brown_circle:',
    'r': ':green_circle:',
    't': ':orange_circle:',
    'y': ':purple_circle:',
    'u': ':red_circle:',
    'i': ':white_circle:',
    'o': ':yellow_circle:',
    'p': ':black_large_square:',
    'a': ':blue_square:',
    's': ':brown_square:',
    'd': ':green_square:',
    'f': ':orange_square:',
    'g': ':purple_square:',
    'h': ':red_square:',
    'j': ':white_large_square:',
    'k': ':yellow_square:',
    'l': ':black_heart:',
    'z': ':blue_heart:',
    'x': ':brown_heart:',
    'c': ':green_heart:',
    'v': ':orange_heart:',
    'b': ':purple_heart:',
    'n': ':heart:',
}

if __name__ == '__main__':

    sentence = input('convert to discord emojis:')
    message = ''.join(table.get(c, c) for c in sentence)
    print(message)
