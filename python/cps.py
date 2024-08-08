# -- coding: UTF-8 --

import os
import shutil
import xml.etree.ElementTree as ET
import zlib

from game_info import GameInfo
from local_configs import LocalConfigs
from wiiflow import WiiFlow


def compute_crc32(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        crc = zlib.crc32(data)
        crc32 = hex(crc & 0xFFFFFFFF)[2:].upper()
        return crc32.rjust(8, "0")


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


class CPS:
    def __init__(self, version_number):
        self.name = f"cps{version_number}"
        self.zip_crc32_to_game_info = {}

    def root_folder_path(self):
        return os.path.join(LocalConfigs.REPOSITORY_FOLDER, self.name)

    def init_crc32_to_game_info(self):
        if len(self.zip_crc32_to_game_info) > 0:
            return
        xml_file_path = os.path.join(
            self.root_folder_path(), f"roms\\{self.name}.xml")
        if os.path.exists(xml_file_path):
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            for element in root.iter():
                if element.tag == "Game":
                    zip_crc32 = element.get("crc32").rjust(8, "0")
                    zip_title = element.get("zip")
                    en_title = element.get("en")
                    zhcn_title = element.get("zhcn")
                    game_info = GameInfo(en_title, zhcn_title)
                    game_info.zip_title = zip_title
                    self.zip_crc32_to_game_info[zip_crc32] = game_info

    def verify_exist_zip_name_as_crc32(self, zip_title):
        folder_path = os.path.join(
            self.root_folder_path(), f"roms\\{zip_title}")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        default_zip_path = os.path.join(
            self.root_folder_path(), f"roms\\{zip_title}.zip")
        if os.path.exists(default_zip_path):
            dst_zip_path = os.path.join(
                folder_path, f"{compute_crc32(default_zip_path)}.zip")
            os.rename(default_zip_path, dst_zip_path)

    def import_new_roms(self):
        self.init_crc32_to_game_info()

        exist_roms_crc32_to_zip = {}
        xml_root = ET.Element("Game-List")

        new_roms_count = 0
        new_roms_folder_path = os.path.join(
            self.root_folder_path(), "new_roms")
        for file_name in os.listdir(new_roms_folder_path):
            file_path = os.path.join(new_roms_folder_path, file_name)

            if os.path.isfile(file_path) is False:
                continue

            file_extension = file_path.split(".")[-1]
            if file_extension != "zip":
                continue

            crc32 = compute_crc32(file_path)
            if crc32 in self.zip_crc32_to_game_info.keys():
                exist_roms_crc32_to_zip[crc32] = file_name
                continue

            zip_title = str(file_name)[:-4]
            self.verify_exist_zip_name_as_crc32(zip_title)

            en_title = ""
            zhcn_title = ""
            for key, game_info in self.zip_crc32_to_game_info.items():
                if zip_title == game_info.zip_title:
                    en_title = game_info.en_title
                    zhcn_title = game_info.zhcn_title
                    break

            attrib = {
                "crc32": crc32,
                "bytes": str(os.stat(file_path).st_size),
                "zip": zip_title,
                "en": en_title,
                "zhcn": zhcn_title
            }

            xml_elem = ET.SubElement(xml_root, "Game", attrib)

            dst_file_path = os.path.join(
                self.root_folder_path(), f"roms\\{zip_title}\\{crc32}.zip")
            os.rename(file_path, dst_file_path)
            new_roms_count = new_roms_count + 1

        for key, value in exist_roms_crc32_to_zip.items():
            print(f"{value} 已经存在，crc32 = {key}")

        xml_file_path = os.path.join(new_roms_folder_path, "new_roms.xml")
        if os.path.exists(xml_file_path):
            os.remove(xml_file_path)

        if new_roms_count == 0:
            print("没有新游戏")
            return
        else:
            print(f"发现 {new_roms_count} 个新游戏")
            tree = ET.ElementTree(xml_root)
            tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)

    def check_game_infos(self):
        self.init_crc32_to_game_info()

        wiiflow = WiiFlow(self.name.upper())
        wiiflow.init_zip_crc32_to_game_id()
        wiiflow.init_game_id_to_info()

        for zip_crc32, game_info in self.zip_crc32_to_game_info.items():
            id = ""
            if game_info.zip_title in wiiflow.zip_crc32_to_game_id.keys():
                id = wiiflow.zip_crc32_to_game_id[game_info.zip_title]
            elif zip_crc32 in wiiflow.zip_crc32_to_game_id.keys():
                id = wiiflow.zip_crc32_to_game_id[zip_crc32]
            else:
                print(
                    f"crc32 = {zip_crc32} 不在 {wiiflow.plugin_name}.ini 文件中，zhcn = {game_info.zhcn_title}")
                continue
            if id in wiiflow.game_id_to_info.keys():
                wii_game_info = wiiflow.game_id_to_info[id]
                if wii_game_info.en_title != game_info.en_title:
                    print("en 属性不匹配")
                    print(f"\t{game_info.en_title} 在 {self.name}.xml")
                    print(
                        f"\t{wii_game_info.en_title} 在 {wiiflow.plugin_name}.xml")

                if wii_game_info.zhcn_title != game_info.zhcn_title:
                    print("zhcn 属性不匹配")
                    print(f"\t{game_info.zhcn_title} 在 {self.name}.xml")
                    print(
                        f"\t{wii_game_info.zhcn_title} 在 {wiiflow.plugin_name}.xml")
            else:
                print(
                    f"id = {id} 不在 {wiiflow.plugin_name}.xml 文件中，zhcn = {game_info.zhcn_title}")

    def export_wii_app(self, file_tuple, sdcard_path):
        wii_folder_path = os.path.join(self.root_folder_path(), "wii")
        for item in file_tuple:
            src_path = os.path.join(wii_folder_path, item)
            dst_path = os.path.join(sdcard_path, item)

            if not os.path.exists(src_path):
                print(f"源文件缺失：{src_path}")
                continue

            if os.path.isdir(src_path):
                copy_folder(src_path, dst_path)
            elif os.path.isfile(src_path):
                copy_file(src_path, dst_path)

    def main_menu(self, sdcard_path, wii_app_file_tuple):
        plugin_name = self.name.upper()
        while True:
            print("\n\n请输入数字序号，选择要执行的操作：")
            print(f"\t1. 导入新游戏 {self.name}.import_new_roms()")
            print(f"\t2. 检查游戏信息 {self.name}.check_game_infos()")
            print("\t3. 转换封面图片 WiiFlow.convert_wfc_files()")
            print("\t4. 导出 WiiFlow 的文件 WiiFlow.export_all()")
            print("\t5. 导出空白的.zip文件 WiiFlow.export_fake_roms()")
            print(f"\t6. 导出 Wii APP 的文件 {self.name}.export_wii_app()")
            print("\t7. 退出程序")

            input_value = str(input("Enter the version number: "))
            if input_value == "1":
                self.import_new_roms()
            elif input_value == "2":
                self.check_game_infos()
            elif input_value == "3":
                wiiflow = WiiFlow(plugin_name)
                wiiflow.convert_wfc_files()
            elif input_value == "4":
                wiiflow = WiiFlow(plugin_name)
                wiiflow.export_all(sdcard_path)
            elif input_value == "5":
                wiiflow = WiiFlow(plugin_name)
                wiiflow.export_fake_roms(sdcard_path)
            elif input_value == "6":
                self.export_wii_app(wii_app_file_tuple, sdcard_path)
            elif input_value == "7":
                break
