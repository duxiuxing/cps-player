# -- coding: UTF-8 --

import fnmatch
import os

from console_impl import ConsoleImpl
from local_configs import LocalConfigs
from wiiflow import WiiFlow


class CPS(ConsoleImpl):
    def __init__(self, version_number):
        self.version_number = version_number
        super().__init__()

    def create_wiiflow(self):
        return WiiFlow(self, f"CPS{self.version_number}")

    def root_folder_path(self):
        return os.path.join(LocalConfigs.repository_folder_path(), f"cps{self.version_number}")

    def rom_extension(self):
        return ".zip"

    def rom_extension_match(self, file_name):
        return fnmatch.fnmatch(file_name, "*.zip")
