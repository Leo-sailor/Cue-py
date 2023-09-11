from typing import Any
from LocalDependencies.Framework.base_ui import callback
from LocalDependencies.Framework.text_ui import text_ui
from LocalDependencies.Framework import base_func as base
import pickle
import datetime
from LocalDependencies.Framework.logger import log
from colorama import Fore

log = log()


def green_print(*args):
    print(Fore.GREEN + f'{args}' + Fore.RESET)


class fake_input_error(TypeError):
    pass


# noinspection PyMethodFirstArgAssignment
class custom_string(str):
    def lower(self) -> str:
        self = custom_string(super().lower())
        return self

    def upper(self) -> str:
        self = custom_string(super().upper())
        return self

    def find_and_replace(self, find, replace):
        self = base.findandreplace(self, find, replace, True)
        return self

    def strip(self, chars=None):
        self = custom_string(super().strip(chars))
        return self


def compare_strings(a: str, b: str) -> bool:
    a = custom_string(a)
    b = custom_string(b)
    a.strip()
    b.strip()
    a.lower()
    b.lower()
    a.find_and_replace('\n', ' | ')
    b.find_and_replace('\n', ' | ')
    log.queue(0, 'comparing strings', (a, b, a == b))
    return a == b


def call_default(func: callable, *args, **kwargs):
    log.queue(0, 'calling a function from somewhere else', (str(func), args, kwargs))
    return func(*args, **kwargs)


class test_ui(callback):
    # noinspection SpellCheckingInspection
    def __init__(self, inp_file: str, out_file: str = None, display_outs: callback | bool = None):
        if isinstance(display_outs, bool):
            if display_outs:
                display_outs = text_ui()
            else:
                display_outs = None
        self.out_obj = display_outs
        self.inp_index = -1
        self.inps = []
        self.out_index = -1
        self.outs = []
        self.use_canned_inps = True
        self.use_canned_outs = True
        inp_file = '    ' + inp_file
        if inp_file[-4:] in ['inps', '.inp', 'puts', 'nput']:  # .inps, .inp, .inputs, .input
            log.queue(1, 'reading faked inputs from text file')
            with open(inp_file.strip(), encoding='utf-8') as f:
                for line in f:
                    self.inps.append(eval(line))
        elif inp_file[-4:] == 'ckle':  # .picle
            log.queue(1, 'reading faked inputs from pickle file')
            with open(inp_file.strip(), 'rb') as f:
                self.inps = pickle.load(f)
        else:
            log.queue(3, 'unable to recognise file format for faked inputs')
            self.inps = []
        if out_file is not None:
            out_file = '    ' + out_file
            if out_file[-4:] in ['outs', '.out', 'puts', 'tput']:
                log.queue(1, 'reading expected outputs from text file')  # .outs, .out, .outputs . output
                with open(out_file.strip(), encoding='utf-8') as f:
                    for line in f:
                        self.outs.append(eval(line))
            elif out_file[-4:] == 'ckle':  # .picle
                log.queue(1, 'reading expected outputs from pickle file')
                with open(out_file.strip(), 'rb') as f:
                    self.outs = pickle.load(f)
        else:
            log.queue(3, 'unable to recognise file format for expected outputs')
            self.use_canned_outs = False
            self.outs = []
        if len(self.inps) == 0:
            self.use_canned_inps = False
        if len(self.outs) == 0:
            self.use_canned_outs = False
        log.flush()

    def canned_user_input(self, expected_type: type, func: callable, *args, **kwargs) -> Any:
        if self.use_canned_inps:
            self.inp_index += 1
            if self.inp_index == len(self.inps):
                log.queue(2, 'out of preprogrammed inputs')
                if self.out_obj:
                    self.out_obj.display_text('OUT OF PRE-PROGRAMMED INPUTS')
                else:
                    print(Fore.RED + 'Out of PRE-PROGRAMMED INPUTS' + Fore.RESET)
                self.use_canned_inps = False
                res = call_default(func, *args, **kwargs)
            else:
                res = self.inps[self.inp_index]
                log.queue(0, 'pre programmed input used', ({self.inp_index + 1, res}))
                green_print(f'--Input {self.inp_index + 1}: {res}')
        else:
            res = call_default(func, *args, **kwargs)
        if isinstance(res, expected_type):
            return res
        else:
            message = f'input number: {self.inp_index} using canned inps: {self.use_canned_inps}\n' \
                      f'expected type: {expected_type} got type: {type(res)}\n with input: {res}'
            log.log(4, 'faked input typing error', message)
            raise fake_input_error(message)

    def force_output(self, out):
        if self.out_obj:
            self.out_obj.display_text(out)
        else:
            print(out)

    def check_output(self, out: Any, func: callable, *args, **kwargs):
        if self.use_canned_outs:
            self.out_index += 1
            if self.out_index == len(self.outs):
                self.force_output('OUT OF EXPECTED OUTPUTS')
                self.use_canned_outs = False
            elif not compare_strings(self.outs[self.out_index], str(out)):
                message = f"Output is not as expected, expected: {self.outs[self.out_index]} actual: {out}"
                log.log(4, 'output is not expected', message)
                raise AssertionError(message)
            else:
                log.queue(0, f'Test line [{self.out_index + 1}] succes', (self.outs[self.out_index], str(out)))
                green_print(f'Test line [{self.out_index + 1}] : passed')
        if self.out_obj:
            return call_default(func, out, *args, **kwargs)
        elif not self.use_canned_outs:
            green_print("All tests passed")
            log.log(2, 'all tests passed')
            exit(0)
        else:
            return None

    def g_date_int(self, *args, **kwargs) -> int:
        return self.canned_user_input(int, self.out_obj.g_date_int, *args, **kwargs)

    def display_text(self, obj, *args, **kwargs):
        return self.check_output(obj, self.out_obj.display_text, *args, **kwargs)

    def display_table(self, obj, *args, **kwargs):
        return self.check_output(obj, self.out_obj.display_text, *args, **kwargs)

    def display_dict(self, obj, *args, **kwargs):
        return self.check_output(obj, self.out_obj.display_text, *args, **kwargs)

    def g_str(self, *args, **kwargs) -> str:
        return self.canned_user_input(str, self.out_obj.g_str, *args, **kwargs)

    def g_int(self, *args, **kwargs) -> int:
        return self.canned_user_input(int, self.out_obj.g_int, *args, **kwargs)

    def g_list(self, *args, **kwargs) -> list:
        return self.canned_user_input(list, self.out_obj.g_list, *args, **kwargs)

    def g_folder_loc(self, *args, **kwargs) -> str:
        return self.canned_user_input(str, self.out_obj.g_folder_loc, *args, **kwargs)

    def g_many_file_locs(self, *args, **kwargs) -> list[str]:
        return self.canned_user_input(list, self.out_obj.g_many_file_locs, *args, **kwargs)

    def g_float(self, *args, **kwargs) -> float:
        return self.canned_user_input(float, self.out_obj.g_float, *args, **kwargs)

    def g_date(self, *args, **kwargs) -> datetime.date:
        return self.canned_user_input(datetime.date, self.out_obj.g_date, *args, **kwargs)

    def g_datetime(self, *args, **kwargs) -> datetime.datetime:
        return self.canned_user_input(datetime.datetime, self.out_obj.g_datetime, *args, **kwargs)

    def g_bool(self, *args, **kwargs) -> bool:
        return self.canned_user_input(bool, self.out_obj.g_bool, *args, **kwargs)

    def g_choose_options(self, *args, **kwargs) -> int:
        return self.canned_user_input(int, self.out_obj.g_choose_options, *args, **kwargs)

    def g_file_loc(self, *args, **kwargs) -> str:
        return self.canned_user_input(str, self.out_obj.g_file_loc, *args, **kwargs)

    def g_nat(self, *args, **kwargs) -> str:
        return self.canned_user_input(str, self.out_obj.g_nat, *args, **kwargs)


class record(test_ui):

    def __init__(self, inp_file: str, out_file: str|None, original_ui: callback):
        log.queue(2, ' input and output recording started')
        if ('        ' + inp_file)[-7:] != '.pickle':
            inp_file += '.pickle'
        if out_file is not None:
            if ('        ' + out_file)[-7:] != '.pickle':
                out_file += '.pickle'
        self.input_file = inp_file
        self.output_file = out_file
        self.out_obj = original_ui
        self.out = []
        self.inp = []
        self.open = open  # fudging thr garbage collector at delete time

    def check_output(self, out: Any, func: callable, *args, **kwargs) -> None:
        if self.output_file is not None:
            log.queue(0, 'new output recoreded', out)
            self.out.append(out)
        return call_default(func, out, *args, **kwargs)

    def canned_user_input(self, expected_type: type, func: callable, *args, **kwargs) -> Any:
        res = call_default(func, *args, **kwargs)
        self.inp.append(res)
        log.queue(0, 'new input recoreded')
        return res

    def __del__(self):
        with self.open(self.input_file, 'wb') as f:
            pickle.dump(self.inp, f)
            log.queue(2, ' recorded inputs saved')
        if self.output_file is not None:
            with self.open(self.output_file, 'wb') as f:
                pickle.dump(self.out, f)
                log.log(2, ' recorded outputs saved')
