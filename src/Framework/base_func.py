from hashlib import md5, sha3_256, sha256
from bcrypt import gensalt, hashpw
from difflib import SequenceMatcher
from countryinfo import CountryInfo
from numpy import diff as np_diff
from typing import Any
# noinspection PyPackageRequirements
from argon2 import PasswordHasher
import pyscrypt

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def first_capital(word: str) -> str:
    """
    This function takes a string and returns that string with a capitalized first letter
    :param word:
    :return: string with capitalized first letter
    """
    word = word.lower()
    word = word.strip()
    try:
        new_word = word[0].upper() + word[1:]
        return new_word
    except IndexError:
        return word


def sort_on_element(sub_li: list[list], element: int, reverse: bool = True, zero_is_big=True) -> list[list]:
    sub_li.sort(reverse=reverse, key=lambda x: x[element] if (x[element] == 0 and zero_is_big) else 9999999)
    return sub_li


def multiindex(inlist: list, term: Any) -> list[int]:
    """
    This function takes a list and finds all occurrences of the term inside of that list,
    will not return the first one
    :param inlist: the list to be searched through
    :param term: the term to be searched for
    :return: all indexes of the term inside of that list
    """
    term = str(term)
    for x in range(len(inlist)):
        if type(inlist[x]) != str:
            inlist[x] = str(inlist[x])

    indices = []
    start = 0
    end = False
    while not end:
        try:
            indices.append(inlist.index(term, start))
            start = indices[-1] + 1
        except ValueError:
            end = True
    return indices


def password_hash(password: str, hash_method: str, salt: bytes | str = None) -> tuple[bytes, bytes]:
    """
    This function will hash a password using the password and a salt and will generate a salt if it is put in without it
    :param password:
    :param salt:
    :param hash_method: either 'bcrypt' or 'md5' or 'sha2' or 'sha3' or 'sha' or 'scrypt' or 'argon2'
    :return:
    """
    match hash_method:
        case 'bcrypt':
            if salt is None:
                salt = gensalt()
            elif salt == '':
                salt = b'0000000000000000'
            hashed = hashpw(password.encode(), salt)
        case 'md5':
            if salt is None:
                salt = ''
            else:
                salt = salt.hex()
            hashed = md5(password + salt)
        case 'scrypt':
            if salt is None:
                salt = ''
            else:
                salt = salt.hex()
            hashed = pyscrypt.hash(password, salt, 256, 256, 256, 256)
            hashed = hashed.digest()
        case 'argon2':
            if salt is None:
                salt = ''
            else:
                salt = salt.hex()
            ph = PasswordHasher()
            hashed = ph.hash(password + salt).encode()
        case 'sha' | 'sha3':
            if salt is None:
                salt = ''
            else:
                salt = salt.hex()
            hashed = sha3_256((password + salt).encode())
            hashed = hashed.digest()
        case 'sha2' | 'sha256':
            if salt is None:
                salt = ''
            else:
                salt = salt.hex()
            hashed = sha256((password + salt).encode())
            hashed = hashed.digest()
        case _:
            return password_hash(password, 'bcrypt', salt)
    return hashed, salt


def hashfile(file: str) -> str:
    """
    This function takes a file address and opens it as a text file and produces a md5 hash of it
    :param file: the file address of the file to be hashed
    :return: the string of the md5 hash
    """
    with open(file) as actual_file:
        str2hash = actual_file.read()
    result = md5(str2hash.encode()).hexdigest()
    return str(result)


def findandreplace(inp, find: str, replace: str, preserve_type=False):
    """
    a recursive find and replace algorithm which searches through lists and theirs sub it's up to the recursion limit
    in search of strings, when a string is found, a normal find and replace algorithm on is applied to the string.
    intended side effect: all int
    THIS IS A TIME CRITICAL FUNCTION, TIME TO RUN > READABILITY OR MAINTAINABILITY OR LOC (LINES OF CODE)
    :param inp:
    :param find:
    :param replace:
    :param preserve_type: if true, all types other than a string will stay in their original types, otherwise they will
    be converted
    :return:
    """
    match inp:
        case str():
            return inp.replace(find, replace)
        case list():
            out = []
            for item in inp:
                out.append(findandreplace(item, find, replace))
            return out
        case float() | int():
            if preserve_type:
                return inp
            return str(inp)
        case _:
            if preserve_type:
                return inp
            try:
                return str(inp)
            except ValueError:
                raise TypeError('Expected type list or str or struct which str() can be applied not ' + str(type(inp)))


def force_int(inp: str | float | int) -> int:
    inp = str(inp)
    numbers_new = numbers[:]
    numbers_new.append('.')
    new_str = []
    for char in inp:
        if char in numbers_new:
            new_str.append(char)
    if len(new_str) == 0:
        return 0
    return int(float(''.join(new_str)))


def clean_table(table: list[list[Any]],wanted_type: type = None):
    initial_vals = table[1]
    cols_to_remove = list(range(len(table[1])))
    for row_index in range(1, len(table)):
        good_cols = []
        for col in cols_to_remove:
            if table[row_index][col] != initial_vals[col]:
                good_cols.append(col)
        [cols_to_remove.pop(cols_to_remove.index(item)) for item in good_cols]
    cols_to_remove.sort(reverse=True)
    for loc, row in enumerate(table):
        for col in cols_to_remove:
            try:
                table[loc].pop(col)
            except AttributeError:
                table.pop(loc)
            except IndexError:
                pass
    if wanted_type is not None:
        for row_num,row in enumerate(table):
            for col_num,cell in enumerate(row):
                table[row_num][col_num] = wanted_type(cell)
    return table


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def ordinal(num) -> str:
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = suffixes.get(num % 10, 'th')
    return str(num) + suffix


def is_iterable(inp: Any) -> bool:
    try:
        iter(inp)
    except TypeError:
        return False
    return True


def check_consecutive(array: list) -> bool:
    n = len(array) - 1
    return sum(np_diff(sorted(array)) == 1) >= n


def r_in(term, inp: list[Any]) -> bool:
    if not is_iterable(inp) or len(inp) <= 1:
        if term == inp:
            return True
        else:
            return False
    else:
        if term in inp:
            return True
        for item in inp:
            if r_in(term, item):
                return True
        return False


class fixed_country_info(CountryInfo):
    # noinspection PyUnresolvedReferences
    def __init__(self, country_name):
        super().__init__(country_name)
        to_remove = ['wales', 'scotland']
        for country in to_remove:
            self._CountryInfo__countries.pop(country)
        for country in self._CountryInfo__countries.values():
            if country_name.upper() in country.get('ISO', {}).values():
                self._CountryInfo__country_name = country['name'].lower()
                break
