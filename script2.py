from coordinates import Cords
import pyautogui
from time import sleep


start = Cords(371, 250)
offset_x = 39
offset_y = 39


def rclick(cords:Cords):
    pyautogui.moveTo((cords.x, cords.y))
    pyautogui.mouseDown(cords.x, cords.y, button="secondary")
    pyautogui.mouseUp(cords.x, cords.y, button="secondary")

def click(cords:Cords, double=False):
    if type(cords) == Cords:
        pyautogui.moveTo((cords.x, cords.y))
        if double:
            pyautogui.mouseDown(cords.x, cords.y)
            pyautogui.mouseUp(cords.x, cords.y)
        pyautogui.mouseDown(cords.x, cords.y)
        pyautogui.mouseUp(cords.x, cords.y)

x = int(input("До какой ячейки в последней строке продавать? (5, 7)"))
for row in range(1, 6):
    for column in range(8):
        if row == 5 and column == x:
            exit()
        cords = Cords(start.x + offset_x * column, start.y + offset_y * row)
        # pyautogui.moveTo((cords.x, cords.y))
        rclick(cords)
        click(Cords(cords.x+10, cords.y+10))
        sleep(0.1)
        click(Cords(1221, 766))
        # input()
        