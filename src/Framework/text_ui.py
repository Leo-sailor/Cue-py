from datetime import date, datetime
from typing import Any
from LocalDependencies.Framework import base_ui
from tkinter import filedialog
import requests
from LocalDependencies.Framework.base_func import fixed_country_info as country_info

base_nat = ''
valid_nat = {'ALG', 'ASA', 'AND', 'ANT', 'ARG', 'ARM', 'ARU', 'AUS', 'AUT', 'AZE', 'BAH', 'ARN', 'BAR',
             'BLR', 'BEL', 'BIZ', 'BER', 'BRA', 'BOT', 'IVB', 'BRU', 'BUL', 'CAM', 'CAN', 'CAY', 'CHI',
             'CHN', 'TPE', 'COL', 'COK', 'CRO', 'CUB', 'CYP', 'CZE', 'DEN', 'DJI', 'DOM', 'ECU', 'EGY',
             'ESA', 'EST', 'FIJ', 'FIN', 'FRA', 'GEO', 'GER', 'GBR', 'GRE', 'GRN', 'GUM', 'GUA', 'HKG',
             'HUN', 'ISL', 'IND', 'INA', 'IRN', 'IRQ', 'IRL', 'ISR', 'ITA', 'JAM', 'JPN', 'KAZ', 'KE',
             'PRK', 'KOR', 'KOS', 'KUW', 'KGZ', 'LAT', 'LIB', 'LBA', 'LIE', 'LTU', 'LUX', 'MAC', 'MAD',
             'MAS', 'MLT', 'MRI', 'MEX', 'MDA', 'MON', 'MNE', 'MNT', 'MAR', 'MOZ', 'MYA', 'NAM', 'NED',
             'AHO', 'NZL', 'NGR', 'MKD', 'NOR', 'OMA', 'PAK', 'PLE', 'PAN', 'PNG', 'PAR', 'PER', 'PHI',
             'POL', 'POR', 'PUR', 'QAT', 'ROM', 'RUS', 'SAM', 'SMR', 'SEN', 'SRB', 'SEY', 'SGP', 'SVK',
             'SLO', 'RSA', 'ESP', 'SRI', 'SKN', 'LCA', 'SUD', 'SWE', 'SUI', 'TAH', 'TAN', 'THA', 'TLS',
             'TTO', 'TUN', 'TUR', 'TKS', 'UGA', 'UKR', 'UAE', 'USA', 'URU', 'ISV', 'VAN', 'VEN', 'ZIM'}


class text_ui(base_ui.callback):
    def display_text(self, text: str):
        print(text)

    def display_table(self, table: list[list[Any]]):
        header = str(table) + '\n'
        long_blank = "                        "
        p = header + '\n'.join(
            [''.join([f'{"".join((item, long_blank))[:15]}  ' for item in row]) for row in table[1:]])
        print(p)

    def display_dict(self, dictionary: dict[Any:Any], key_delimiter: str = ' -> ',
                     delimiter: str = '\n', raw: bool = False):
        if raw:
            print(dictionary)
            return None
        print(delimiter.join([key_delimiter.join([key, val]) for key, val in dictionary]))

    def g_str(self, prompt: str, length: int = None, char_level: int = 0, chars_allowed: list[str] = None,
              chars_not_allowed: list[str] = None) -> str:
        if chars_not_allowed is None:
            chars_not_allowed = []
        all_chars = [char for char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ¬`!"£$%^&*()_+=-098765432'
                                      '1  {}[]:;@\'#~,./?>< |\\/`']
        if char_level == 1:
            all_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                         'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                         'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4',
                         '5', '6', '7', '8', '9', '.', '_', '\'', '(', ')', ':']
        elif char_level == 2:
            all_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                         'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                         'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-', ' ', '0', '1',
                         '2', '3', '4', '5', '6', '7', '8', '9']
        elif char_level == 3:
            all_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                         'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                         'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-', ' ']

        for char in chars_not_allowed:
            try:
                all_chars.pop(all_chars.index(char))
            except ValueError:
                pass
        if chars_allowed is not None:
            for val, char in enumerate(all_chars[:]):
                if char not in chars_allowed:
                    all_chars.pop(val)
        new = []
        old = input(prompt)
        for char in old:
            if char in all_chars:
                new.append(char)
        if length is not None:
            new.append("                                                                                              ")
            new_str = ''.join(new)[:length]
        else:
            new_str = ''.join(new)
        if old == new_str:
            return old
        choice = self.g_bool(f'\nYour string is "{new_str}". Is this what you expected?')
        if choice:
            return new_str
        return self.g_str(prompt, length, chars_allowed=all_chars)

    def g_int(self, prompt: str, range_low: int = None, range_high: int = None, allow_skip=False) -> int | None:
        if range_high is None:
            range_low = float('-inf')
        if range_low is None:
            range_low = float('inf')
        while True:  # is it wrong
            try:
                inp = input(prompt)
                if inp == '':
                    if allow_skip:
                        # noinspection PyTypeChecker
                        return None
                    inp = 0
                else:
                    inp = int(inp)
            except ValueError:
                self.display_text('That input was not a integer, please enter a whole number')
                continue
            if range_high >= inp >= range_low:
                return inp
            else:
                self.display_text(f'That input was not between {range_high} and {range_low} inclusive')

    def g_list(self, prompt: str, length: int = None) -> list:
        old = input(prompt)
        new = old.split(',')
        if length is not None:
            new += [None] * length
            new = new[:length]
        choice = self.g_bool(f'\nYour string is {new}. Is this what you expected?')
        if choice:
            return new
        else:
            return self.g_list(prompt, length)

    def g_float(self, prompt: str, range_low: int | float = None, range_high: int | float = None) -> float:
        if range_high is None:
            range_low = float('-inf')
        if range_low is None:
            range_low = float('inf')
        while True:  # is it wrong
            try:
                inp = float(input(prompt))
            except ValueError:
                self.display_text('That input was not a float (number), please enter a normal number')
                continue
            if range_high >= inp >= range_low:
                return inp
            else:
                self.display_text(f'That input was not between {range_high} and {range_low} inclusive')

    def g_date(self, prompt: str, earliest: date | datetime = datetime(100, 1, 1),
               latest: date | datetime = datetime(3100, 1, 1)) -> date:
        if prompt[-2:] == ': ':
            prompt += ': '
        year = self.g_int(f"Please enter the year {prompt}", -2000, 3000)
        month = self.g_int(f"Please enter the month {prompt}", 1, 12)
        if month in [4, 6, 9, 11]:
            day = self.g_int(f"Please enter the day {prompt}", 1, 30)
        elif month in [1, 3, 5, 7, 8, 10, 12]:
            day = self.g_int(f"Please enter the day {prompt}", 1, 31)
        else:
            day = self.g_int(f"Please enter the day {prompt}", 1, 28)
        dates = datetime(year, month, day)
        if earliest < dates < latest:
            return dates
        else:
            self.display_text(f"that date is not between {earliest} and {latest}. please try again.")
            return self.g_date(prompt, earliest, latest)

    def g_date_int(self, prompt: str, earliest: date | datetime = datetime(100, 1, 1),
                   latest: date | datetime = datetime(3100, 1, 1)) -> int:
        now = self.g_date(prompt, earliest, latest)
        thousand = date(2000, 1, 1)
        day = now - thousand
        return day.days

    def g_datetime(self, prompt: str, earliest: date | datetime = datetime(100, 1, 1),
                   latest: date | datetime = datetime(3100, 1, 1)) -> datetime:
        dates = self.g_date(prompt)
        year, month, day = dates.year, dates.month, dates.day
        hours = self.g_int(f"Please enter the hour (24hr clock) {prompt}", 0, 24)
        minutes = self.g_int(f"Please enter the minute {prompt} - (enter) to skip", 0, 60)
        seconds = self.g_int(f"Please enter the seconds {prompt} - (enter) to skip", 0, 60)
        dates = datetime(year, month, day, hours, minutes, seconds)
        if earliest < dates < latest:
            return dates
        else:
            self.display_text(f"that date is not between {earliest} and {latest}. please try again.")
            return self.g_datetime(prompt, earliest, latest)

    def g_bool(self, prompt: str) -> bool:
        inp = self.g_int(f'{prompt} - please enter 1 for yes and 0 for no: ', 0, 1)
        if inp == 1:
            return True
        else:
            return False

    def g_choose_options(self, options: list[str], prompt=None, default: int = None) -> int:
        if prompt is None:
            prompt = 'please select one of the following options'
        print(prompt)
        for val, item in enumerate(options):
            print(f'({val + 1}) - {item}')
        if default:
            res = self.g_int('Which would you like to choose: ', 1, len(options), allow_skip=True)
            if res:
                return res - 1
            else:
                return default
        else:
            return self.g_int('Which would you like to choose: ', 1, len(options)) - 1

    def g_file_loc(self, mode='r', **args) -> str:
        file_getter = filedialog.askopenfile(mode, **args)
        file_getter.close()
        return file_getter.name

    def g_folder_loc(self, **args) -> str:
        file_getter = filedialog.askdirectory(**args)
        return file_getter

    def g_many_file_locs(self, mode='r', **args) -> list[str]:
        file_getter = filedialog.askopenfiles(mode, **args)
        [file.close() for file in file_getter]
        files = [file.name for file in file_getter]
        return files

    def g_nat(self, obj_of_nationality: str, return_type: int = 1) -> str:
        """
        This function gets the current computer's address and uses that to generate a suggested 3-letter country code
        :param obj_of_nationality:
        :param return_type: 1 for 3-letter country code, 2 for country name, 3 for 2-letter code, 4 for telephone code
        5 for capital, and 6 for location, 7 for boarders
        """

        def code_to_out(nat):
            global base_nat
            country = country_info(nat)
            base_nat = country.iso(3)
            match return_type:
                case 1:
                    return base_nat
                case 2:
                    return country.name()
                case 3:
                    return country.iso(2)
                case 4:
                    return country.calling_codes()
                case 5:
                    return country.capital()
                case 6:
                    return country.latlng()
                case 7:
                    return country.borders()

        global base_nat
        if base_nat == '':
            try:
                ip = requests.get('https://geolocation-db.com/json').json()
                nat_name = ip['country_name']
            except requests.exceptions.ConnectionError:
                nat_name = 'Netherlands'
        else:
            nat_name = base_nat

        choice = self.g_bool(f'Is {nat_name} the correct nationality of {obj_of_nationality}?')
        if choice:
            # use py pi country info to get country
            return code_to_out(nat_name)

        else:
            while base_nat == '':
                base_nat_possible = self.g_str(f'Please enter {obj_of_nationality}\'s 3 Letter country code', 3, 3)
                if base_nat_possible.upper() in valid_nat:
                    base_nat = base_nat_possible.upper()
                    return code_to_out(base_nat)
                else:
                    print('Sorry, that country code is not valid please try again')
