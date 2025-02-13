import launchpad_py
from pygame import time

#Launchpad S Setup
lp = launchpad_py.Launchpad()
lp.Open(0)
lp.Reset()

"""lp.LedCtrlXY(0, 1, 3, 0)
lp.LedCtrlXY(7, 1, 3, 0)
lp.LedCtrlXY(0, 8, 3, 0)
lp.LedCtrlXY(7, 8, 3, 0)"""

"""while True:
    if len(lp.ButtonStateXY()) > 0:
        print(*lp.ButtonStateXY(), sep= '\n')
    time.wait(1000)"""

lp.Close()