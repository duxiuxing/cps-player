# -- coding: UTF-8 --

import fnmatch
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET

from game_info import GameInfo
from configparser import ConfigParser
from console import Console
from local_configs import LocalConfigs
from wiiflow_plugins_data import WiiFlowPluginsData


def folder_exist(folder_path):
    # 判断指定文件夹是否存在
    # Args:
    #     folder_path (str): 待判断的文件夹路径
    # Returns:
    #     bool: 如果文件夹存在则返回 True，否则返回 False
    if os.path.isdir(folder_path):
        return True
    else:
        print(f"无效的文件夹：{folder_path}")
        return False


def verify_folder_exist(folder_path):
    # 判断指定文件夹是否存在，如果不存在则创建该文件夹
    # Args:
    #     folder_path (str): 待判断的文件夹路径，要求父文件夹必须是存在的
    # Returns:
    #     bool: 如果文件夹存在或创建成功，则返回 True，否则返回 False
    if os.path.isdir(folder_path):
        return True
    else:
        os.mkdir(folder_path)
        if os.path.isdir(folder_path):
            return True
        else:
            print(f"无效文件夹：{folder_path}")
            return False


def verify_folder_exist_ex(folder_full_path):
    # 判断指定文件夹是否存在，如果不存在则逐级创建
    # Args:
    #     folder_path (str): 待判断的文件夹路径，如果父文件夹不存在会逐级创建
    # Returns:
    #     bool: 如果文件夹存在或创建成功，则返回 True，否则返回 False
    folder_path = ""
    for folder_name in folder_full_path.split("\\"):
        if folder_path == "":
            folder_path = folder_name
            if not os.path.isdir(folder_path):
                return False
        else:
            if not os.path.isdir(folder_path):
                return False
            folder_path = f"{folder_path}\\{folder_name}"
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)
    return os.path.isdir(folder_full_path)


def copy_file_if_not_exist(src_file_path, dst_file_path):
    # 复制源文件到目标路径，如果目标文件已存在则跳过
    # Args:
    #     src_file_path (str): 源文件路径
    #     dst_file_path (str): 目标文件路径
    if not os.path.exists(src_file_path):
        print(f"源文件缺失：{src_file_path}")
    elif not os.path.exists(dst_file_path):
        shutil.copyfile(src_file_path, dst_file_path)


class WiiFlow:
    def __init__(self, console, plugin_name):
        self.console = console

        # 机种对应的 WiiFlow 插件名称
        self._plugin_name = plugin_name

        # 默认的 WiiFlowPluginsData 实例
        self._plugins_data = WiiFlowPluginsData(console, plugin_name)

        # ROM 的目标文件标题为键，ROM 的源文件路径为值的字典
        # 内容来自 wiiflow\\roms_export.xml，其实就是 WiiFlow 用的所有 ROM 文件
        # 读取操作在 self.init_rom_dst_name_to_src_path() 中实现
        self.rom_dst_name_to_src_path = {}

    def plugin_name(self):
        return self._plugin_name

    def plugins_data(self):
        return self._plugins_data

    def roms_export_to_folder_path(self):
        return os.path.join(LocalConfigs.sd_path(),
                            f"roms\\{self.plugin_name()}")

    def init_rom_dst_name_to_src_path(self):
        # 本函数执行的操作如下：
        # 1. 读取 roms_export.xml
        # 2. 设置 self.rom_dst_name_to_src_path
        # 3. 有防止重复读取的逻辑
        if len(self.rom_dst_name_to_src_path) > 0:
            return

        xml_path = os.path.join(self.console.root_folder_path(),
                                "wii\\wiiflow\\roms_export.xml")

        if not os.path.exists(xml_path):
            print(f"无效的文件：{xml_path}")
            return

        tree = ET.parse(xml_path)
        root = tree.getroot()

        for game_elem in root.findall("Game"):
            rom_crc32 = game_elem.get("crc32").rjust(8, "0")
            rom_path = self.console.query_rom_path(rom_crc32)
            if rom_path is None:
                print(f"crc32 = {rom_crc32} 的 ROM 文件不存在")
                continue
            if not os.path.exists(rom_path):
                print(f"无效的文件：{rom_path} in WiiFlow.init_rom_dst_name_to_src_path()")
                continue

            rom_name = game_elem.get("rom") + self.console.rom_extension()
            self.rom_dst_name_to_src_path[rom_name] = rom_path

    def convert_wfc_files(self):
        # 调用 wfc_conv.exe 生成 WiiFlow 专用的游戏封面文件（.png 格式转 .wfc 格式）
        # .wfc 格式的文件都存放在 wiiflow\\cache 文件夹里
        if not os.path.exists(LocalConfigs.wfc_conv_exe_path()):
            print(f"无效的文件：{LocalConfigs.wfc_conv_exe_path()}")
            zip_file_path = os.path.join(LocalConfigs.repository_folder_path(),
                                         "pc-tool\\WFC_conv_0-1.zip")
            print(f"安装文件在 {zip_file_path}")
            return

        # wiiflow\\cache
        foler_path = os.path.join(self.console.root_folder_path(),
                                  "wii\\wiiflow\\cache")
        if not verify_folder_exist_ex(foler_path):
            print(f"无效文件夹：{foler_path}")
            return

        foler_path = os.path.join(self.console.root_folder_path(),
                                  "wii\\wiiflow")
        cmd_line = f"\"{LocalConfigs.wfc_conv_exe_path()}\" \"{foler_path}\""
        print(cmd_line)
        subprocess.call(cmd_line)

    def export_all_fake_roms(self):
        # 本函数用于把 WiiFlowPluginsData 里所有的 ROM 文件导出到 Wii 的 SD 卡
        dst_folder_path = self.roms_export_to_folder_path()
        if not verify_folder_exist_ex(dst_folder_path):
            return
        self._plugins_data.export_all_fake_roms_to(dst_folder_path)

    def export_fake_roms(self):
        # 本函数用于把 roms_export.xml 中所有的 ROM 文件导出到 Wii 的 SD 卡
        dst_folder_path = self.roms_export_to_folder_path()
        if not verify_folder_exist_ex(dst_folder_path):
            return

        self.init_rom_dst_name_to_src_path()
        for dst_name in self.rom_dst_name_to_src_path.keys():
            dst_path = os.path.join(dst_folder_path, dst_name)
            if not os.path.exists(dst_path):
                open(dst_path, "w").close()

    def export_roms(self):
        # 本函数用于把 roms_export.xml 中所有的 ROM 文件导出到 Wii 的 SD 卡
        dst_folder_path = self.roms_export_to_folder_path()
        if not verify_folder_exist_ex(dst_folder_path):
            return

        self.init_rom_dst_name_to_src_path()
        for dst_name, src_path in self.rom_dst_name_to_src_path.items():
            dst_path = os.path.join(dst_folder_path, dst_name)
            copy_file_if_not_exist(src_path, dst_path)

    def export_png_boxcovers(self):
        # 本函数会根据 SD 卡里的 ROM 文件，把对应的封面文件（.png 格式）导出到 Wii 的 SD 卡
        #
        # 注意：WiiFlow 中展示的游戏封面对应于 cache 文件夹里的 .wfc 文件，如果已经导出过 .wfc 格式的封面文件，可以不导出 .png 格式的
        if not folder_exist(LocalConfigs.sd_path()):
            return

        # SD:\\wiiflow\\boxcovers\\<plugin_name>
        dst_folder_path = os.path.join(LocalConfigs.sd_path(),
                                       f"wii\\wiiflow\\boxcovers\\{self.plugin_name()}")
        if not verify_folder_exist_ex(dst_folder_path):
            return
        src_folder_path = os.path.join(self.console.root_folder_path(),
                                       f"wii\\wiiflow\\boxcovers\\{self.plugin_name()}")

        # 根据 SD 卡里的 ROM 文件来拷贝对应的封面文件
        roms_folder_path = os.path.join(LocalConfigs.sd_path(),
                                        f"roms\\{self.plugin_name()}")
        for rom_name in os.listdir(roms_folder_path):
            if not self.console.rom_extension_match(rom_name):
                continue
            src_png_path = os.path.join(src_folder_path, f"{rom_name}.png")
            dst_png_path = os.path.join(dst_folder_path, f"{rom_name}.png")
            copy_file_if_not_exist(src_png_path, dst_png_path)

    def export_cache(self):
        # 本函数执行的操作如下：
        # 1. 把 wiiflow\\boxcovers\\blank_covers 里的默认封面文件（.png 格式）导出到 Wii 的 SD 卡
        # 2. 把 wiiflow\\cache\\blank_covers 里的默认封面文件（.wfc 格式）导出到 Wii 的 SD 卡
        # 3. 根据 SD 卡里的 ROM 文件，把对应的封面文件（.wfc 格式）导出到 Wii 的 SD 卡
        # 4. 删除 SD:\\wiiflow\\cache 里可能失效的缓存文件
        #
        # 注意：WiiFlow 中展示的游戏封面对应于 cache 文件夹里的 .wfc 文件，如果导出了 .wfc 格式的封面文件，可以不导出 .png 格式的
        if not folder_exist(LocalConfigs.sd_path()):
            return

        # SD:\\wiiflow\\boxcovers\\blank_covers
        folder_path = os.path.join(LocalConfigs.sd_path(),
                                   "wiiflow\\boxcovers\\blank_covers")
        if not verify_folder_exist_ex(folder_path):
            return
        src_png_path = os.path.join(self.console.root_folder_path(),
                                    f"wii\\wiiflow\\boxcovers\\blank_covers\\{self.plugin_name()}.png")
        dst_png_path = os.path.join(LocalConfigs.sd_path(),
                                    f"wiiflow\\boxcovers\\blank_covers\\{self.plugin_name()}.png")
        copy_file_if_not_exist(src_png_path, dst_png_path)

        # SD:\\wiiflow\\cache\\blank_covers
        folder_path = os.path.join(LocalConfigs.sd_path(),
                                   "wiiflow\\cache\\blank_covers")
        if not verify_folder_exist_ex(folder_path):
            return
        src_wfc_path = os.path.join(self.console.root_folder_path(),
                                    f"wii\\wiiflow\\cache\\blank_covers\\{self.plugin_name()}.wfc")
        dst_wfc_path = os.path.join(LocalConfigs.sd_path(),
                                    f"wiiflow\\cache\\blank_covers\\{self.plugin_name()}.wfc")
        copy_file_if_not_exist(src_wfc_path, dst_wfc_path)

        # SD:\\wiiflow\\cache\\<plugin_name>
        dst_folder_path = os.path.join(LocalConfigs.sd_path(),
                                       f"wiiflow\\cache\\{self.plugin_name()}")
        if not verify_folder_exist_ex(dst_folder_path):
            return
        src_folder_path = os.path.join(self.console.root_folder_path(),
                                       f"wii\\wiiflow\\cache\\{self.plugin_name()}")

        # 根据 SD 卡里的 ROM 文件来拷贝对应的封面文件
        roms_folder_path = os.path.join(LocalConfigs.sd_path(),
                                        f"roms\\{self.plugin_name()}")
        for rom_name in os.listdir(roms_folder_path):
            if not self.console.rom_extension_match(rom_name):
                continue
            src_file_path = os.path.join(src_folder_path, f"{rom_name}.wfc")
            dst_file_path = os.path.join(dst_folder_path, f"{rom_name}.wfc")
            copy_file_if_not_exist(src_file_path, dst_file_path)

        # SD:\\wiiflow\\cache\\lists
        # lists 文件夹里都是 WiiFlow 生成的缓存文件，删掉才会重新生成
        folder_path = os.path.join(LocalConfigs.sd_path(),
                                   "wiiflow\\cache\\lists")
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

    def export_plugin(self):
        # 本函数用于把 wiiflow\\plugins 里的文件导出到 Wii 的 SD 卡
        if not folder_exist(LocalConfigs.sd_path()):
            return

        # SD:\\wiiflow\\plugins\\R-Sam\\<plugin_name>
        dst_folder_path = os.path.join(LocalConfigs.sd_path(),
                                       f"wiiflow\\plugins\\R-Sam\\{self.plugin_name()}")
        if not verify_folder_exist_ex(dst_folder_path):
            return
        src_folder_path = os.path.join(self.console.root_folder_path(),
                                       f"wii\\wiiflow\\plugins\\R-Sam\\{self.plugin_name()}")

        file_tuple = ("config.ini", "sound.ogg")
        for file in file_tuple:
            src_file_path = os.path.join(src_folder_path, file)
            dst_file_path = os.path.join(dst_folder_path, file)
            if os.path.exists(dst_file_path):
                os.remove(dst_file_path)
            copy_file_if_not_exist(src_file_path, dst_file_path)

    def export_plugins_data(self):
        # # 本函数执行的操作如下：
        # 1. 把 wiiflow\\plugins_data 里的文件导出到 Wii 的 SD 卡
        # 2. 删除可能失效的缓存文件：gametdb_offsets.bin
        if not folder_exist(LocalConfigs.sd_path()):
            return

        # SD:\\wiiflow\\plugins_data\\<plugin_name>
        dst_folder_path = os.path.join(LocalConfigs.sd_path(),
                                       f"wiiflow\\plugins_data\\{self.plugin_name()}")
        if not verify_folder_exist_ex(dst_folder_path):
            return
        src_folder_path = os.path.join(self.console.root_folder_path(),
                                       f"wii\\wiiflow\\plugins_data\\{self.plugin_name()}")

        file_tuple = (f"{self.plugin_name()}.ini", f"{self.plugin_name()}.xml")
        for file in file_tuple:
            src_file_path = os.path.join(src_folder_path, file)
            dst_file_path = os.path.join(dst_folder_path, file)
            if os.path.exists(dst_file_path):
                os.remove(dst_file_path)
            copy_file_if_not_exist(src_file_path, dst_file_path)

        # gametdb_offsets.bin 是 WiiFlow 生成的缓存文件，删掉才会重新生成
        gametdb_offsets_bin_path = os.path.join(dst_folder_path, "gametdb_offsets.bin")
        if os.path.exists(gametdb_offsets_bin_path):
            os.remove(gametdb_offsets_bin_path)

    def export_snapshots(self):
        # 本函数用于把 wiiflow\\snapshots 里的游戏截图（.png格式）导出到 Wii 的 SD 卡
        if not folder_exist(LocalConfigs.sd_path()):
            return

        # SD:\\wiiflow\\snapshots\\<plugin_name>
        dst_folder_path = os.path.join(LocalConfigs.sd_path(),
                                       f"wiiflow\\snapshots\\{self.plugin_name()}")
        if not verify_folder_exist_ex(dst_folder_path):
            return
        src_folder_path = os.path.join(self.console.root_folder_path(),
                                       f"wii\\wiiflow\\snapshots\\{self.plugin_name()}")

        roms_folder_path = os.path.join(LocalConfigs.sd_path(),
                                        f"roms\\{self.plugin_name()}")
        for rom_name in os.listdir(roms_folder_path):
            if not self.console.rom_extension_match(rom_name):
                continue
            png_title = os.path.splitext(rom_name)[0]
            src_png_path = os.path.join(src_folder_path, f"{png_title}.png")
            dst_png_path = os.path.join(dst_folder_path, f"{png_title}.png")
            copy_file_if_not_exist(src_png_path, dst_png_path)

    def export_source_menu(self):
        # 本函数用于把 wiiflow\\source_menu 里的源菜单图标（.png格式）导出到 Wii 的 SD 卡
        if not folder_exist(LocalConfigs.sd_path()):
            return

         # SD:\\wiiflow\\source_menu
        folder_path = os.path.join(LocalConfigs.sd_path(),
                                   "wiiflow\\source_menu")
        if not verify_folder_exist_ex(folder_path):
            return
        src_png_path = os.path.join(self.console.root_folder_path(),
                                    f"wii\\wiiflow\\source_menu\\{self.plugin_name()}.png")
        dst_png_path = os.path.join(LocalConfigs.sd_path(),
                                    f"wiiflow\\source_menu\\{self.plugin_name()}.png")
        copy_file_if_not_exist(src_png_path, dst_png_path)

    def convert_game_synopsis(self):
        # wiiflow\\plugins_data 里的 <self.plugin_name()>.xml 可以配置游戏的中文摘要
        # 但 WiiFlow 在显示中文句子的时候不会自动换行，需要在每个汉字之间加上空格才能有较好的显示效果，
        # 本函数用于生成 WiiFlow 专用排版格式的游戏摘要文本，原始的摘要文本存于 game_synopsis.md，
        # 转换后的摘要文本存于 game_synopsis.wiiflow.md，需要手动合入 <self.plugin_name()>.xml
        src_file_path = os.path.join(self.console.root_folder_path(), "doc\\game_synopsis.md")
        if not os.path.exists(src_file_path):
            return

        dst_lines = []
        with open(src_file_path, "r", encoding="utf-8") as src_file:
            for line in src_file.readlines():
                src_line = line.rstrip("\n")
                if src_line.startswith("#"):
                    dst_lines.append(src_line)
                    continue
                elif len(src_line) == 0:
                    dst_lines.append("")
                    continue
                else:
                    dst_line = ""
                    for char in src_line:
                        if len(dst_line) == 0:
                            dst_line = char
                        elif dst_line[-1] in " 、：，。《》（）【】“”":
                            dst_line += char
                        elif char in " 、：，。《》（）【】“”1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                            dst_line += char
                        else:
                            dst_line += f" {char}"

                    dst_lines.append(dst_line)

        dst_file_path = os.path.join(self.console.root_folder_path(), "doc\\game_synopsis.wiiflow.md")
        with open(dst_file_path, "w", encoding="utf-8") as dst_file:
            for line in dst_lines:
                dst_file.write(f"{line}\n")
