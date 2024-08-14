# -- coding: UTF-8 --

import os
import shutil

from console_base import ConsoleBase
from local_configs import LocalConfigs
from main_menu import CmdHandler
from main_menu import MainMenu


def create_folder_if_not_exists(folder_full_path):
    folder_path = ""
    for folder_name in folder_full_path.split("\\"):
        if folder_path == "":
            folder_path = folder_name
            if not os.path.exists(folder_path):
                return False
        else:
            if not os.path.exists(folder_path):
                return False
            folder_path = f"{folder_path}\\{folder_name}"
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
    return os.path.exists(folder_full_path)


def copy_folder(src, dst):
    if not create_folder_if_not_exists(dst):
        return
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_folder(s, d)
        elif not os.path.exists(d):
            shutil.copy2(s, d)


def copy_file(src, dst):
    if not create_folder_if_not_exists(os.path.dirname(dst)):
        return
    if not os.path.exists(dst):
        shutil.copy2(src, dst)


class ExportWiiApps(CmdHandler):
    def __init__(self, files_tuple):
        super().__init__("导出独立模拟器 APP 的文件到 Wii 的 SD 卡")
        self.files_tuple = files_tuple

    def run(self):
        wii_folder_path = os.path.join(
            MainMenu.console.root_folder_path(), "wii")
        for relative_path in self.files_tuple:
            src_path = os.path.join(wii_folder_path, relative_path)
            dst_path = os.path.join(LocalConfigs.SDCARD_ROOT, relative_path)

            if not os.path.exists(src_path):
                print(f"源文件缺失：{src_path}")
                continue

            if os.path.isdir(src_path):
                copy_folder(src_path, dst_path)
            elif os.path.isfile(src_path):
                copy_file(src_path, dst_path)
