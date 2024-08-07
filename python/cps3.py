# -- coding: UTF-8 --

from cps import CPS
from wiiflow import WiiFlow

# cps3 = CPS(3)
# cps3.list_new_roms()
# cps3.check_game_infos()

wiiflow = WiiFlow("CPS3")
# wiiflow.convert_wfc_files()
wiiflow.export_to("D:\\sdcard")
