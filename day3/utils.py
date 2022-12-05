'''
from letter to int value
remember a-z are 97 to 122 in ascii and A - Z are 65 to 90 in ascii
but here a-z are 0 to 26 and A - Z are 26 to 52
'''


def char_to_int(charData):
    raw_value = ord(charData)
    if raw_value > 90:
        return raw_value - 97 + 1
    else:
        return raw_value - 65 + 27


def test_char_to_int():
    assert char_to_int('a') == 1
    assert char_to_int('z') == 26
    assert char_to_int('A') == 27
    assert char_to_int('Z') == 52

if __name__ == '__main__':
    test_char_to_int()