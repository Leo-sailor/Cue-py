from datetime import datetime
from typing import Literal, Any, Callable
import os
import sys
from timeit import default_timer as ns_time
from LocalDependencies.Framework.constants import constants
from colorama import Fore
from LocalDependencies.Framework.base_func import findandreplace

c = constants()
log_levels = {0: 'Debug', 1: 'Info', 2: 'Event', 3: 'Warning', 4: 'ERROR', 5: 'FATAL'}
production_env = c.get('production')


def green_print(*args):
    print(Fore.GREEN + f'{args}' + Fore.RESET)


def line_factory(level: Literal[0, 1, 2, 3, 4, 5], message: str, data: Callable[[], str] = None, stack: list = None,
                 time_str: str = None) -> str:
    if data is None:
        data = ''
    else:
        data = findandreplace(data, '\n', '(\\n)')
    if stack is None:
        stack = get_stack()
    if time_str is None:
        time_str = time()
    if len(stack) > 0:
        return f'{time_str}, {level}-{log_levels.get(level)}, {len(stack)}, {stack[0]}, {message}, {data}, {stack}\n'
    else:
        return f'{time_str}, {level}-{log_levels.get(level)}, {len(stack)}, del stack, {message}, {data}, {stack}\n'


def get_stack():
    stack = []
    start = 2
    while True:
        try:
            frame = sys._getframe(start + 1)
        except ValueError:
            return stack
        res = f"{os.path.basename(frame.f_code.co_filename)}/{frame.f_lineno} {frame.f_code.co_name}()"
        stack.append(res)
        start += 1
        if '<module>' in res:
            break
    return stack


def time(detail: Literal[0, 1] = 1, date=None) -> str:
    """
    Returns the current time in UTC as a formatted string.
    """
    if date is None:
        date = datetime.utcnow()
    if detail == 0:
        return date.strftime('%Y-%m-%d--%H-%M-%S')
    elif detail == 1:
        return date.isoformat(' ', 'microseconds')
    else:
        return time(date=date)


def log(file_loc: str = None):
    if _log._self is None:
        if file_loc is None:
            raise TypeError("Log missing 1 required positional argument: 'file_loc'")
        else:
            _log._self = obj = _log(file_loc)
    else:
        obj = _log._self
    return obj


class _log:
    _self = None

    def __init__(self, file_loc: str):
        self.to_write = None
        self.log_levels = log_levels
        file_loc = '    ' + file_loc
        if file_loc[-4:] != '.log':
            file_loc += '.log'
        file_loc = file_loc.split('\\')
        if len(file_loc) == 0:
            file_loc = file_loc[0].split('/')
        file_loc[-1] = time(0) + '-' + file_loc[-1]
        self.file = '\\'.join(file_loc)[4:]
        with open(self.file, 'x') as f:
            f.write(line_factory(2, 'Logging Initialized'))
        self.queue_list = []
        self.open = open

    def log(self, level: Literal[0, 1, 2, 3, 4, 5], message: str, data: Any = None):
        self.to_write = line_factory(level, message, data)
        self.flush()
        self.to_write = None

    def queue(self, level: Literal[0, 1, 2, 3, 4, 5], message: str, data: Any = None):
        self.queue_list.append((level, message, data, get_stack(), datetime.utcnow()))

    def flush(self):
        start_time = ns_time()
        completed_queue = [line_factory(*args) for args in self.queue_list]
        if self.to_write:
            completed_queue.append(self.to_write)

        with self.open(self.file, 'a') as f:
            f.write(''.join(completed_queue))
            # f.write(line_factory(0, 'Logging queue flush'))
        self.queue_list = []
        end_time = ns_time()
        self.queue(1, 'flush complete, time takes in ms', (end_time - start_time) * 1000)
        if not production_env:
            green_print(f'{(end_time - start_time) * 1000} milliseconds for flush')

    def __del__(self):
        self.queue(2, 'Logger deleted and terminated')
        self.flush()

    @property
    def self(self):
        return self._self
