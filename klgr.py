import time
import win32api
import win32con
import os.path


name = 'Inpt'
check = os.path.exists(name + '.txt')
starttime = time.perf_counter()
back = ''
t2 = 0
text = []

while win32api.GetAsyncKeyState(48) == 0:
    win32api.ClipCursor((520, 1, 1400, 1919))

    t = time.perf_counter() - starttime

    mousepos = win32api.GetCursorPos()

    mousekeys = [win32api.GetAsyncKeyState(win32con.VK_LBUTTON),
                 win32api.GetAsyncKeyState(win32con.VK_RBUTTON),
                 win32api.GetAsyncKeyState(win32con.VK_MBUTTON)]

    keybd = []
    for i in range(127):
        keybd.append(win32api.GetAsyncKeyState(i))

    if (mousepos, keybd, mousekeys) != back and (t - t2) > 0:

        text.append(str(t) + '\n')
        text.append(str(mousepos) + '\n')
        text.append(str(keybd) + '\n')
        text.append(str(mousekeys) + '\n')

        back = mousepos, keybd, mousekeys

        t2 = t

if not check:
    file = open(name + '.txt', 'w')
    file.writelines(text)
    file.close()
else:
    n = 1
    check = os.path.exists(name + str(n) + '.txt')
    while check:
        n = n + 1
        check = os.path.exists(name + str(n) + '.txt')
    file = open(name + str(n) + '.txt', 'w')
    file.writelines(text)
    file.close()

win32api.ClipCursor((0, 0, 0, 0))
