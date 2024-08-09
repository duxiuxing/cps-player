# -- coding: UTF-8 --

from cps import CPS

wii_app_files_tuple = (
    "apps\\ra-cps3\\overlays",
    "apps\\ra-cps3\\boot.dol",
    "apps\\ra-cps3\\icon.png",
    "apps\\ra-cps3\\meta.xml",
    "retroarch",
    "wad\\ra-cps3\\R-Sam-CPS3-White [C3LR].zhtw.wad",
    "wad\\ra-cps3\\R-Sam-CPS3-Yellow [C3LR].zhtw.wad"
)

cps3 = CPS(3)
cps3.main_menu(wii_app_files_tuple)
