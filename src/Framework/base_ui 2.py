from datetime import date,datetime
from typing import Any
import LocalDependencies.Framework.base_func as base
from bcrypt import gensalt


class callback:
    def display_text(self, text: str):
        return None

    def display_table(self, table: list[list[Any]]):
        return None

    def display_dict(self, dictionary: dict[Any:Any], key_delimiter: str = ' -> ',
                     delimiter: str = '\n', raw: bool = False):
        return None

    def g_str(self, prompt: str, length: int = None, char_level: int = 0, chars_allowed: list[str] = None,
              chars_not_allowed: list[str] = None) -> str:
        return ''

    def g_int(self, prompt: str, range_low: int = None, range_high: int = None, allow_skip=False) -> int | None:
        return 0

    def g_list(self, prompt: str, length: int = None) -> list:
        return []

    def g_float(self, prompt: str, range_low: int | float = None, range_high: int | float = None) -> float:
        return 0.0

    def g_date(self, prompt: str, earliest: date | datetime = datetime(100, 1, 1),
               latest: date | datetime = datetime(3100, 1, 1)) -> date:
        return date.today()

    def g_date_int(self, prompt: str, earliest: date | datetime = datetime(100, 1, 1),
                   latest: date | datetime = datetime(3100, 1, 1)) -> int:
        return 0

    def g_datetime(self, prompt: str, earliest: date | datetime = datetime(100, 1, 1),
                   latest: date | datetime = datetime(3100, 1, 1)) -> datetime:
        return datetime.now()

    def g_bool(self, prompt: str) -> bool:
        return True

    def g_password_receive(self, prompt: str, correct_hash: bytes, hash_method: str, salt: bytes = None) -> bool:
        prompt = 'Press (enter) to skip entering a password\n' + prompt
        while True:
            inp = self.g_str(prompt)
            if base.password_hash(inp, hash_method, salt)[0] == correct_hash:
                self.display_text('Password is correct')
                return True
            elif inp == '':
                self.display_text('Password entry is skipped')
                return False
            else:
                self.display_text('That password was incorrect, please try again')

    def __g_new_password(self, prompt) -> str:
        password_a = None
        same = False
        while not same:
            password_a = self.g_str(prompt)
            password_b = self.g_str('Please it again to confirm: ')
            same = password_b == password_a
            if not same:
                self.display_text('\nThose passwords did not match, Please try again')
        return password_a

    def g_make_password_with_salt(self, prompt, hash_method) -> tuple[str, str]:
        password = self.__g_new_password(prompt)
        salt = gensalt()
        tup = base.password_hash(password, hash_method, salt)
        hashed = tup[0]
        return hashed.hex(), salt.hex()

    def g_make_password_without_salt(self, prompt, hash_method) -> bytes:
        password = self.__g_new_password(prompt)
        tup = base.password_hash(password, hash_method, '')
        hashed = tup[0]
        return hashed

    def g_choose_options(self, options: list[str], prompt=None, default: int = None) -> int:
        return 0

    def g_file_loc(self, mode='r', **args) -> str:
        return "c:\\Users\\"

    def g_nat(self, obj_of_nationality: str, return_type: int = 1) -> str:
        """
        This function gets the current computer's address and uses that to generate a suggested 3-letter country code
        :param obj_of_nationality:
        :param return_type: 1 for 3-letter country code, 2 for country name, 3 for 2-letter code, 4 for telephone code
        5 for capital, and 6 for location, 7 for boarders
        """
        return "GBR"

    def g_folder_loc(self, **args) -> str:
        return "c:\\Users\\"

    def g_many_file_locs(self, mode='r', **args) -> list[str]:
        return ["c:\\Users\\"]
