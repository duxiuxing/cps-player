# -- coding: UTF-8 --

from cps import CPS
from wiiflow import WiiFlow

cps_version = 1
plugin_name = "CPS1"

while True:
    print("\n\n请输入数字序号，选择要执行的操作：")
    print("\t1. 导入新游戏 CPS.import_new_roms()")
    print("\t2. 检查游戏信息 CPS.check_game_infos()")
    print("\t3. 转换封面图片 WiiFlow.convert_wfc_files()")
    print("\t4. 导出所有游戏文件 WiiFlow.export_all()")
    print("\t5. 导出空白的.zip文件 WiiFlow.export_fake_roms()")
    print("\t6. 退出程序")

    input_value = str(input("Enter the version number: "))
    if input_value == "1":
        cps = CPS(cps_version)
        cps.import_new_roms()
    elif input_value == "2":
        cps = CPS(cps_version)
        cps.check_game_infos()
    elif input_value == "3":
        wiiflow = WiiFlow(plugin_name)
        wiiflow.convert_wfc_files()
    elif input_value == "4":
        wiiflow = WiiFlow(plugin_name)
        wiiflow.export_all("D:\\sdcard")
    elif input_value == "5":
        wiiflow = WiiFlow(plugin_name)
        wiiflow.export_fake_roms("D:\\sdcard")
    elif input_value == "6":
        break
