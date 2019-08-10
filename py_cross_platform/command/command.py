import subprocess
import re
import os
from enum import Enum
from py_cross_platform.env import DEV_NULL

__all__ = [
    "Command",
    "RunningType",
]


class RunningType(Enum):
    RUN = "RUN"
    EXEC = "EXEC"


class Command(object):
    is_test = False

    @staticmethod
    def __check(t, p) -> bool:
        for x in t:
            if re.match(p, x):
                return False
        return True

    def __init__(self, cmd: str):
        self.__cmd = cmd
        self.__param_list = []
        self.__exec_times = 0
        self.__exec_out = []
        self.__return_code = []
        self.__run_times = 0
        self.__error_ignore = False

    def set_error_ignore(self, enable_ignore=True):
        self.__error_ignore = enable_ignore

    def make(self) -> str:
        cmd = self.__cmd
        for param in self.__param_list:
            param = " ".join(param)
            cmd += " " + param

        if self.__error_ignore:
            cmd += " 2> " + DEV_NULL

        return cmd

    def build(self) -> str:
        return self.make()

    def print(self) -> 'Command':
        cmd = self.make()
        print(cmd)
        return self

    def add_param(self, *param_list: list or str) -> 'Command':
        if len(param_list) == 0:
            return self
        self.__param_list.append(tuple(param_list))
        return self

    def run(self) -> int:
        if Command.is_test:
            self.print()
        self.__return_code.append(os.system(self.make()))
        self.__run_times += 1
        return self.__return_code[-1]

    def exec(self) -> str:
        if Command.is_test:
            self.print()
        sp = subprocess.run(self.make(), shell=True, stdout=subprocess.PIPE)
        self.__exec_out.append(sp.stdout.decode("utf-8"))
        self.__return_code.append(sp.returncode)
        self.__exec_times += 1
        return self.__exec_out[-1]

    def get_param(self, n: int) -> str:
        try:
            return re.split(r"\s+", self.make())[n]
        except IndexError:
            return ""

    def get_param_re(self, check_value: str) -> str:
        for t in self.__param_list:
            for p in t:
                if self.__check(check_value, p):
                    return " ".join(t)
        return ""

    def rm_param(self, check_value: str) -> None:
        self.__param_list = list(filter(lambda t: self.__check(t, check_value), self.__param_list))

    def rm_param_re(self, check_value: str) -> None:
        self.__param_list = list(filter(lambda t: self.__check(t, check_value), self.__param_list))

    def clean(self) -> None:
        self.__param_list = []
        self.__exec_times = 0
        self.__run_times = 0
        self.__return_code = []
        self.__exec_out = []

    def __str__(self) -> str:
        return self.make()

    def __call__(self, *args, **kwargs):
        self.add_param(*args)
        for k, v in kwargs:
            self.add_param(k, v)
        return self.exec()
