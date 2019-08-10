import os
import re

__all__ = ["FileScanner"]


class FileScanner:

    def __init__(self, root_dir_list: list, re_file_list=None, re_dir_list=None, enable_link=False):
        self.__root_dir_list = root_dir_list
        self.__re_file_list = [] if not re_file_list else re_file_list
        self.__re_dir_list = [] if not re_dir_list else re_dir_list
        self.__enable_link = enable_link

        self.files = set()
        self.dirs = set()

    def __find_file(self, root):
        try:
            files = os.listdir(root)
        except FileNotFoundError:
            return
        for file in files:
            real_path = os.path.abspath(root + "/" + file)
            # print("now " + real_path)
            if os.path.isdir(real_path):
                if os.path.islink(real_path) and not self.__enable_link:
                    continue
                is_my_dir = False
                for reg in self.__re_dir_list:
                    if re.match(reg, real_path):
                        # print("find " + file)
                        self.dirs.add(real_path.replace("\\", "/"))
                        is_my_dir = True
                        continue
                    # print("into "+real_path)
                if not is_my_dir:
                    self.__find_file(real_path)
            else:
                for reg in self.__re_file_list:
                    if re.match(reg, real_path):
                        # print("find " + file)
                        self.files.add(real_path.replace("\\", "/"))

    def find(self):
        for root in self.__root_dir_list:
            self.__find_file(root)

        return {
            "files": list(self.files),
            "dirs": list(self.dirs),
        }
