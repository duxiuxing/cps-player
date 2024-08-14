# -- coding: UTF-8 --

from cps import CPS
from export_wii_apps import ExportWiiApps
from main_menu import MainMenu


wii_app_files_tuple = (
    "apps\\ra-cps3\\overlays",
    "apps\\ra-cps3\\boot.dol",
    "apps\\ra-cps3\\icon.png",
    "apps\\ra-cps3\\meta.xml",
    "retroarch",
    "wad\\ra-cps3\\R-Sam-CPS3-White [C3LR].zhtw.wad",
    "wad\\ra-cps3\\R-Sam-CPS3-Yellow [C3LR].zhtw.wad"
)


MainMenu.console = CPS(3)
MainMenu.init_default_cmd_handlers()
MainMenu.add_cmd_handler(ExportWiiApps(wii_app_files_tuple))
MainMenu.show()
