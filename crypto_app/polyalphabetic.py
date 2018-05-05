""" This programme implements a polyalphabetic cipher. """

import string

from crypto_app.models import Alphabed

ALPHABET = Alphabed.objects.all().last().title
CHARACTERS_THAT_MUST_REMAIN_THE_SAME = string.digits + string.punctuation + string.whitespace


def cycle_get(lst, index):
    """
    If the list ends go back to the start.
    >>> cycle_get(["lorem","ipsum","dolor","sit"],8)
    "lorem"
    """
    new_index = index % len(lst)
    return (lst[new_index])


def cycle_increment_index(index, lst):
    """
    If at the end: go back to the start
    else: increment.
    >>> cycle_increment_index(0,["a","b","c"])
    1
    >>> cycle_increment_index(2,["a","b","c"])
    0
    """
    if index == len(lst) - 1:
        index = 0
    else:
        index += 1
    return (index)


def shift(letter, value):
    """
    Shifts a letter in the alphabet by the value,
    if the alphabet ends go back to the start.
    >>> shift('a',5)
    f
    >>> "".join([shift(i,20) for i in "hello"])
    'byffi'
    """
    current_letter_value = ALPHABET.find(letter)
    end_value = current_letter_value + value
    return (cycle_get(ALPHABET, end_value))


def convert_key_to_numbers(key):
    """
    Uses the alphabetic value of letters to convert a word
    to a list of numbers.
    >>> convert_key_to_numbers("abcde")
    [0,1,2,3,4]
    >>> convert_key_to_numbers("example")
    [4, 23, 0, 12, 15, 11, 4]
    """
    return ([ALPHABET.find(i) for i in key])


def encrypt(text, key, reverse_operation=False):
    """
    Encrypts the text with a polyalphabetic cipher.
    >>> encrypt("lorem ipsum dolor sit amet, consectetur adipiscing elit","latine")
    'wokmz masnu qswok avx lmxb, psysxkgieuk iqmailkvrr eeqg'
    >>> encrypt("the quick brown fox jumps over the lazy dog","gvufigfwiufw")
    'zcy vcohg jltst aic rarla iaax obj tgeu lil'
    """
    text = text.lower()
    key = convert_key_to_numbers(key)
    index_of_key = 0
    result = ""
    for char in text:
        if char in CHARACTERS_THAT_MUST_REMAIN_THE_SAME:
            result += char
        else:
            if not reverse_operation:
                result += shift(char, key[index_of_key])
            else:
                result += shift(char, - key[index_of_key])
            index_of_key = cycle_increment_index(index_of_key, key)
    return (result)


def decrypt(text, key):
    """
    Decrypts the text previously encrypted with a polyalphabetic cipher.
    >>> decript('wokmz masnu qswok avx lmxb, psysxkgieuk iqmailkvrr eeqg',"latine")
    'lorem ipsum dolor sit amet, consectetur adipiscing elit'
    >>> decrypt("zcy vcohg jltst aic rarla iaax obj tgeu lil","gvufigfwiufw")
    'the quick brown fox jumps over the lazy dog'
    """
    return (encrypt(text, key, reverse_operation=True))
