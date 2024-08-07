# -- coding: UTF-8 --

from cps import CPS
from wiiflow import WiiFlow

# cps1 = CPS(1)
# cps1.list_new_roms()
# cps1.check_game_infos()

wiiflow = WiiFlow("CPS1")
# wiiflow.convert_wfc_files()
wiiflow.export_to("D:\\sdcard")
