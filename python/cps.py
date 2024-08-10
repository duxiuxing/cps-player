# -- coding: UTF-8 --

import os
from console_base import ConsoleBase
from local_configs import LocalConfigs


class CPS(ConsoleBase):
    def __init__(self, version_number):
        super().__init__()
        self.version_number = version_number

    def folder_path(self):
        return os.path.join(LocalConfigs.REPOSITORY_FOLDER, f"cps{self.version_number}")

    def wiiflow_plugin_name(self):
        return f"CPS{self.version_number}"
