# -- coding: UTF-8 --

import os
import xml.etree.ElementTree as ET
import zlib

from configparser import ConfigParser
from local_configs import LocalConfigs


def compute_crc32(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        crc = zlib.crc32(data)
        return hex(crc & 0xFFFFFFFF)[2:].upper()


class GameInfo:
    def __init__(self, en, zhcn):
        self.en = en
        self.zhcn = zhcn


class CPS:
    def __init__(self, version_number):
        self.name = f"cps{version_number}"
        self.all_crc32_to_game_info = {}

    def root_folder_path(self):
        return os.path.join(LocalConfigs.REPOSITORY_FOLDER, self.name)

    def load_all_roms_crc32_to_name(self):
        if len(self.all_crc32_to_game_info) > 0:
            return
        xml_file_path = os.path.join(
            self.root_folder_path(), f"roms\\{self.name}.xml")
        if os.path.exists(xml_file_path):
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            for element in root.iter():
                if element.tag == "Game":
                    crc32 = element.get("crc32")
                    en = element.get("en")
                    zhcn = element.get("zhcn")
                    self.all_crc32_to_game_info[crc32] = GameInfo(en, zhcn)

    def list_new_roms(self):
        self.load_all_roms_crc32_to_name()

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
            if crc32 in self.all_crc32_to_game_info.keys():
                exist_roms_crc32_to_zip[crc32] = file_name
                continue

            attrib = {
                "crc32": crc32,
                "bytes": str(os.stat(file_path).st_size),
                "zip": str(file_name)[:-4]
            }

            xml_elem = ET.SubElement(xml_root, "Game", attrib)
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
