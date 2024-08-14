# -- coding: UTF-8 --

import os

from console_base import ConsoleBase
from local_configs import LocalConfigs
from wiiflow import WiiFlow


class CPS(ConsoleBase):
    def __init__(self, version_number):
        super().__init__()
        self.version_number = version_number
        self.wiiflow = WiiFlow(self, f"CPS{self.version_number}")

    def root_folder_path(self):
        return os.path.join(LocalConfigs.REPOSITORY_FOLDER, f"cps{self.version_number}")
