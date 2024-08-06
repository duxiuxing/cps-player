# -- coding: UTF-8 --

import os
import xml.etree.ElementTree as ET
import zlib

from local_configs import LocalConfigs


def compute_crc32(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        crc = zlib.crc32(data)
        return hex(crc & 0xFFFFFFFF)[2:].upper()


class CPS1:
    ALL_ROMS_CRC32_TO_NAME = {}


    @staticmethod
    def folder_path():
        return os.path.join(LocalConfigs.REPOSITORY_FOLDER, "cps1")
    

    @staticmethod
    def load_all_roms_crc32_to_name():
        if len(CPS1.ALL_ROMS_CRC32_TO_NAME) > 0:
            return
        xml_file_path = os.path.join(CPS1.folder_path(), "roms\\cps1.xml")    
        if os.path.exists(xml_file_path):
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            for element in root.iter():
                if element.tag == "Game":
                    crc32 = element.get("crc32")
                    zhcn = element.get("zhcn")
                    CPS1.ALL_ROMS_CRC32_TO_NAME[crc32] = zhcn


    @staticmethod
    def list_new_roms():
        CPS1.load_all_roms_crc32_to_name()

        exist_roms_crc32_to_zip = {}
        xml_root = ET.Element("Game-List")

        new_roms_folder_path = os.path.join(CPS1.folder_path(), "new_roms")
        for file_name in os.listdir(new_roms_folder_path):
            file_path = os.path.join(new_roms_folder_path, file_name)

            if os.path.isfile(file_path) is False:
                continue

            file_extension = file_path.split(".")[-1]
            if file_extension != "zip":
                continue

            crc32 = compute_crc32(file_path)
            if crc32 in CPS1.ALL_ROMS_CRC32_TO_NAME.keys():
                exist_roms_crc32_to_zip[crc32] = file_name
                continue

            attrib = {
                "crc32": crc32,
                "bytes": str(os.stat(file_path).st_size),
                "zip": str(file_name)[:-4]
            }

            xml_elem = ET.SubElement(xml_root, "Game", attrib)

        # 将树结构转换为一个可写入文件的对象
        tree = ET.ElementTree(xml_root)

        # 写入XML文件
        tree.write(os.path.join(new_roms_folder_path, "new_roms.xml"),
                   encoding="utf-8", xml_declaration=True)

        for key, value in exist_roms_crc32_to_zip.items():
            print(f"{value} 已经存在，crc32 = {key}")


CPS1.list_new_roms()
