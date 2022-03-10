def encoding(word, key):
    new_word = ""
    for k, i in enumerate(word):
        new_word += chr(ord(i) ^ ord(key[k % len(key)]))
    return new_word
