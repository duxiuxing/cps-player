# -- coding: UTF-8 --

from cps import CPS

wii_app_files_tuple = (
    "apps\\ra-cps1\\boot.dol",
    "apps\\ra-cps1\\icon.png",
    "apps\\ra-cps1\\meta.xml",
    "apps\\sf2",
    "apps\\sf2ce",
    "private",
    "wad\\ra-cps1\\Capcom-CPS-1-RunningSnakes-Gold [C1LR].wad",
    "wad\\ra-cps1\\Capcom-CPS-1-RunningSnakes-White [C1LR].wad",
    "wad\\ra-cps1\\Capcom-CPS-1-RunningSnakes-Yellow [C1LR].wad",
    "wad\\ra-cps1\\R-Sam-CPS1-White [C1LR].zhtw.wad",
    "wad\\ra-cps1\\R-Sam-CPS1-Yellow [C1LR].zhtw.wad",
    "wad\\Street Fighter II [SF21].zhtw.wad",
    "wad\\Street Fighter II CE [SF22].zhtw.wad"
)

cps1 = CPS(1)
cps1.main_menu(wii_app_files_tuple)
