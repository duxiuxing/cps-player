# -- coding: UTF-8 --

from cps import CPS

wii_app_file_tuple = (
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

cps2 = CPS(2)
cps2.main_menu("D:\\sdcard", wii_app_file_tuple)
