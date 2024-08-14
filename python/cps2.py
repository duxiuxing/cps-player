# -- coding: UTF-8 --

from cps import CPS
from export_wii_apps import ExportWiiApps
from main_menu import MainMenu


wii_app_files_tuple = (
    "apps\\ra-cps2\\boot.dol",
    "apps\\ra-cps2\\icon.png",
    "apps\\ra-cps2\\meta.xml",
    "private",
    "wad\\ra-cps2\\Capcom-CPS-2-RunningSnakes-Blue [C2LR].wad",
    "wad\\ra-cps2\\Capcom-CPS-2-RunningSnakes-Gold [C2LR].wad",
    "wad\\ra-cps2\\Capcom-CPS-2-RunningSnakes-White [C2LR].wad",
    "wad\\ra-cps2\\R-Sam-CPS2-White [C2LR].zhtw.wad",
    "wad\\ra-cps2\\R-Sam-CPS2-Yellow [C2LR].zhtw.wad"
)


MainMenu.console = CPS(2)
MainMenu.init_default_cmd_handlers()
MainMenu.add_cmd_handler(ExportWiiApps(wii_app_files_tuple))
MainMenu.show()
