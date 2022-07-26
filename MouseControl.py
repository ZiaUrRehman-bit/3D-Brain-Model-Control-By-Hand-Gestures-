import pyautogui
import time

print(pyautogui.position())

pyautogui.moveTo(311, 427, duration=0.25)
for i in range(10):
    pyautogui.scroll(i)
    print(i)

time.sleep(1)
for i in range(0, -10, -1):
    pyautogui.scroll(i)
x, y = pyautogui.position()
# pyautogui.click(button="left", clicks=2)
# pyautogui.mouseDown(button="right")
# for i in range(x, x+200,30):
#     pyautogui.dragTo(i, y)
# pyautogui.mouseUp(button="right")
# x, y = pyautogui.position()
# pyautogui.mouseDown(button="right")
# for i in range(x, x-200,-30):
#     pyautogui.dragTo(i, y)
# pyautogui.mouseUp(button="right")
# pyautogui.mouseDown(button="right")
# for i in range(427, 600,30):
#     pyautogui.dragTo(311, i)
# pyautogui.mouseUp(button="right")
# pyautogui.mouseDown(button="right")
# for i in range(600, 427,-30):
#     pyautogui.dragTo(311, i)
# pyautogui.mouseUp(button="right")
    # pyautogui.moveTo(311, 427, duration=0.25)
    # pyautogui.dragTo(511,427, button="left", duration=0.25)

pyautogui.mouseDown(button="left")
for i in range(x, x+200,30):
    pyautogui.dragTo(i, y)
pyautogui.mouseUp(button="left")
x, y = pyautogui.position()
pyautogui.mouseDown(button="left")
for i in range(x, x-200,-30):
    pyautogui.dragTo(i, y)
pyautogui.mouseUp(button="left")