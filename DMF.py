import time
import math
import win32api
import win32con
import win32gui
import os.path
import threading
import cv2
import numpy as np
from PIL import ImageGrab


# Возвращает статус таргета (Есть ли таргет, жив ли таргет,
# дистанция, здоровье цели)
def status_target():
    rgb = win32gui.GetPixel(hdc, 25, 0)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8
    b = (rgb & 0x00FF0000) >> 16

    rgb2 = win32gui.GetPixel(hdc, 63, 0)
    b2 = (rgb2 & 0x00FF0000) >> 16

    if r == 1:
        r = False
    else:
        r = True

    if g == 1:
        g = True
    else:
        g = False

    b = int(round(b / 255 * 100, 0))

    return [r, g, b, b2]


# Возвращает дистанцию до цели
def distance():
    rgb = win32gui.GetPixel(hdc, 25, 0)
    b = (rgb & 0x00FF0000) >> 16
    b = int(round(b / 255 * 100, 0))
    return b


# Возвращает дебафы цели (Иммолейт, корапт, курса, сифон, лайфдрейн, соулдрейн)
def debuff():
    rgb = win32gui.GetPixel(hdc, 38, 0)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8

    rgb2 = win32gui.GetPixel(hdc, 63, 0)
    r2 = (rgb2 & 0x000000FF) >> 0

    rgb3 = win32gui.GetPixel(hdc, 101, 0)
    b3 = (rgb3 & 0x00FF0000) >> 16

    rgb4 = win32gui.GetPixel(hdc, 114, 0)
    g4 = (rgb4 & 0x0000FF00) >> 8
    b4 = (rgb4 & 0x00FF0000) >> 16

    if r == 1:
        r = False
    else:
        r = True

    if g == 1:
        g = False
    else:
        g = True

    if r2 == 1:
        r2 = False
    else:
        r2 = True

    if b3 == 1:
        b3 = False
    else:
        b3 = True

    if g4 == 1:
        g4 = False
    else:
        g4 = True

    if b4 == 1:
        b4 = False
    else:
        b4 = True

    return [r, g, r2, b3, g4, b4]


# Возвращает есть ли курса агонии на цели
def curse():
    rgb = win32gui.GetPixel(hdc, 63, 0)
    r = (rgb & 0x000000FF) >> 0
    if r == 1:
        r = False
    else:
        r = True
    return r


# Возвращает есть ли дебафы из списка на игроке (Замедляющий яд)
def debuff_player():
    rgb = win32gui.GetPixel(hdc, 0, 0)
    r = (rgb & 0x000000FF) >> 0
    if r == 1:
        r = False
    else:
        r = True
    return r


# Возвращает бафы игрока (Демонскин, вызван ли пет, висит ли сс, прок найтфола,
# съеден ли суккуб, пища, питье, невидимость)
def buff():
    rgb = win32gui.GetPixel(hdc, 51, 0)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8

    rgb2 = win32gui.GetPixel(hdc, 76, 0)
    b2 = (rgb2 & 0x00FF0000) >> 16

    rgb3 = win32gui.GetPixel(hdc, 13, 0)
    g3 = (rgb3 & 0x0000FF00) >> 8
    r3 = (rgb3 & 0x000000FF) >> 0

    rgb4 = win32gui.GetPixel(hdc, 0, 0)
    g4 = (rgb4 & 0x0000FF00) >> 8
    b4 = (rgb4 & 0x00FF0000) >> 16

    rgb5 = win32gui.GetPixel(hdc, 101, 0)
    g5 = (rgb5 & 0x0000FF00) >> 8

    if r == 1:
        r = False
    else:
        r = True

    if g == 1:
        g = True
    else:
        g = False

    if b2 == 1:
        b2 = False
    else:
        b2 = True

    if g3 == 1:
        g3 = False
    else:
        g3 = True

    if g5 == 1:
        g5 = False
    else:
        g5 = True

    if b4 == 1:
        b4 = False
    else:
        b4 = True

    if g4 == 1:
        g4 = False
    else:
        g4 = True

    if r3 == 1:
        r3 = False
    else:
        r3 = True

    return [r, g, b2, g5, g3, g4, b4, r3]


# Возвращает прок найтфола и висит ли сифон
def nf_sifon():
    rgb = win32gui.GetPixel(hdc, 101, 0)
    g = (rgb & 0x0000FF00) >> 8
    b = (rgb & 0x00FF0000) >> 16
    if g == 1:
        g = False
    else:
        g = True
    if b == 1:
        b = False
    else:
        b = True
    return (g, b)


# Возвращает здоровье и ресурс игрока в процентах, состояние боя,
# состояние каста, здоровье пета
def resurs_player():
    rgb = win32gui.GetPixel(hdc, 13, 0)
    b = (rgb & 0x00FF0000) >> 16
    b = round(b, 0)

    rgb2 = win32gui.GetPixel(hdc, 38, 0)
    b2 = (rgb2 & 0x00FF0000) >> 16
    b2 = round(b2, 0)

    rgb3 = win32gui.GetPixel(hdc, 51, 0)
    b3 = (rgb3 & 0x00FF0000) >> 16

    rgb4 = win32gui.GetPixel(hdc, 63, 0)
    g4 = (rgb4 & 0x0000FF00) >> 8

    rgb5 = win32gui.GetPixel(hdc, 101, 0)
    r5 = (rgb5 & 0x000000FF) >> 0

    if g4 == 1:
        g4 = False
    else:
        g4 = True

    if b3 == 1:
        b3 = False
    else:
        b3 = True

    if r5 == 255:
        r5 = 0

    return [b, b2, b3, g4, r5]


# Возвращает хп и ресурс игрока, и есть ли коррапт на цели
def health_resurs_corrapt():
    rgb = win32gui.GetPixel(hdc, 13, 0)
    b = (rgb & 0x00FF0000) >> 16
    b = round(b, 0)
    rgb2 = win32gui.GetPixel(hdc, 38, 0)
    b2 = (rgb2 & 0x00FF0000) >> 16
    b2 = round(b2, 0)
    g2 = (rgb2 & 0x0000FF00) >> 8
    if g2 == 1:
        g2 = False
    else:
        g2 = True
    return (b, b2, g2)


# # Возвращает есть ли цель, жива ли цель, дистанция
def target():
    rgb = win32gui.GetPixel(hdc, 25, 0)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8
    b = (rgb & 0x00FF0000) >> 16

    if r == 1:
        r = False
    else:
        r = True

    if g == 1:
        g = True
    else:
        g = False

    b = int(round(b / 255 * 100, 0))

    return (r, g, b)


# Возвращает состояние боя
def combat():
    rgb = win32gui.GetPixel(hdc, 51, 0)
    b = (rgb & 0x00FF0000) >> 16
    if b == 1:
        b = False
    else:
        b = True

    return b


# Возвращает кулдауны игрока (хс, сс, коил)
def cooldown():
    rgb = win32gui.GetPixel(hdc, 76, 0)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8

    rgb2 = win32gui.GetPixel(hdc, 114, 0)
    r2 = (rgb2 & 0x000000FF) >> 0

    return [r, g, r2]


# Возвращает кд койла
def coil_cd():
    rgb = win32gui.GetPixel(hdc, 114, 0)
    r = (rgb & 0x000000FF) >> 0
    return r


# Возвращает наличие хс, сс, шардов
def saveitem():
    rgb = win32gui.GetPixel(hdc, 89, 0)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8
    b = (rgb & 0x00FF0000) >> 16

    if r == 1:
        r = False
    else:
        r = True
    if g == 1:
        g = False
    else:
        g = True
    b = b - 1

    return [r, g, b]


# Возвращает прочность предметов в %
def DurancyItem():
    rgb = win32gui.GetPixel(hdc, 127, 0)
    b = (rgb & 0x00FF0000) >> 16

    return b


# Возвращает состояние экрана загрузки
def loadscreen():
    global imdead_daemon
    global imdead_
    old_imdead_ = imdead_
    old_imdead_daemon = imdead_daemon
    imdead_daemon = False
    rgb = win32gui.GetPixel(hdc, 1919, 1079)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8
    b = (rgb & 0x00FF0000) >> 16

    if r == 0 and g == 0 and b == 0:
        return True
    else:
        return False
    imdead_ = old_imdead_
    imdead_daemon = old_imdead_daemon


# Возвращает мертв ли персонаж
def dead():
    rgb = win32gui.GetPixel(hdc, 127, 0)
    r = (rgb & 0x000000FF) >> 0

    if r == 1:
        return True
    else:
        return False


# Возвращает, есть ли предметы для распыления
def disenchant():
    rgb = win32gui.GetPixel(hdc, 127, 0)
    g = (rgb & 0x0000FF00) >> 8
    if g == 1:
        return False
    else:
        return True


# Нажать клавишу X и отпустить через Y секунд
def key(x, y):
    win32api.keybd_event(x, 0, 0, 0)
    if y != 0:
        starttime = time.perf_counter()
        while time.perf_counter() - starttime <= y:
            pass
    win32api.keybd_event(x, 0, win32con.KEYEVENTF_KEYUP, 0)


# Нажать комбинацию 2 клавиш X1, X2 и отпустить через Y секунд
def key2(x1, x2, y):
    win32api.keybd_event(x1, 0, 0, 0)
    win32api.keybd_event(x2, 0, 0, 0)
    if y != 0:
        starttime = time.perf_counter()
        while time.perf_counter() - starttime < y:
            pass
    win32api.keybd_event(x1, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(x2, 0, win32con.KEYEVENTF_KEYUP, 0)


# Ротация по цели
def rotation():
    while status_target()[0] and status_target()[1]:

        if resurs_player()[0] < 20 and cooldown()[0] == 1 and saveitem()[0]:
            key2(18, 57, 0.1)

        elif (debuff()[4] and (status_target()[3] > 10)) or debuff()[5]:
            continue

        elif resurs_player()[1] < 10 and resurs_player()[0] > 30:
            key(57, 0.1)

        elif buff()[3] and not(status_target()[3] <= 10 and saveitem()[2] < 5):
            key(54, 0.1)

        elif not debuff()[3]:
            key(51, 0.1)

        elif not debuff()[2]:
            key(50, 0.1)

        elif not debuff()[1]:
            key(49, 0.1)

        elif resurs_player()[0] > 95 and resurs_player()[1] < 80:
            key(57, 0.1)

        elif (not debuff()[5] and status_target()[3] <= 10 and
              saveitem()[2] < 5):
            key(56, 0.1)

        elif not debuff()[4]:
            key(53, 0.1)

        else:
            pass

    time.sleep(0.1)


# Ротация бафов
def rotation_buff():

    while (resurs_player()[0] < 70 or resurs_player()[1] < 70 or
           not buff()[0] or (not saveitem()[0] and saveitem()[2] > 0) or
           (not buff()[4] and (saveitem()[2] > 0 or resurs_player()[4] != 0))):

        if imdead_:
            break

        if resurs_player()[3]:
            continue

        elif (resurs_player()[0] - resurs_player()[1] > 10 and
              resurs_player()[0] > 20):
            key(57, 0)

        elif resurs_player()[0] < 70:
            key2(18, 51, 0)
            if resurs_player()[1] < 70:
                key2(18, 52, 0)
            while resurs_player()[0] < 100 and buff()[5] and not imdead_:
                pass
            while resurs_player()[1] < 100 and buff()[6] and not imdead_:
                pass
            key(88, 0)

        elif not buff()[0]:
            key2(18, 54, 0)

        elif resurs_player()[4] == 0 and saveitem()[2] > 0 and not buff()[4]:
            key2(18, 55, 0)

        elif not buff()[4]:
            key2(18, 53, 0)

        elif not saveitem()[0] and saveitem()[2] > 0:
            key2(18, 56, 0)

        else:
            pass
    time.sleep(0.1)


# Вторая ротация бафов
def rotation_buff2():

    while ((resurs_player()[0] > resurs_player()[1] and
           resurs_player()[0] > 40) or
           not buff()[0] or (not saveitem()[0] and saveitem()[2] > 0) or
           (not buff()[4] and (saveitem()[2] > 0 or resurs_player()[4] != 0))):

        if imdead_:
            break

        if resurs_player()[3]:
            continue

        elif (resurs_player()[0] > resurs_player()[1] and
              resurs_player()[0] > 40):
            key(57, 0)

        elif not buff()[0]:
            key2(18, 54, 0)

        elif resurs_player()[4] == 0 and saveitem()[2] > 0 and not buff()[4]:
            key2(18, 55, 0)

        elif not buff()[4]:
            key2(18, 53, 0)

        elif not saveitem()[0] and saveitem()[2] > 0:
            key2(18, 56, 0)

        else:
            pass
    time.sleep(0.1)


# принять получение лута
def confirm_loot():
    mousexy = win32api.GetCursorPos()
    rgb = win32gui.GetPixel(hdc, mousexy[0], mousexy[1] - 80)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8
    b = (rgb & 0x00FF0000) >> 16
    timer = time.perf_counter()
    while ((r > 10 or g > 10 or b > 10) and not dead() and not combat()
           and time.perf_counter() - timer < 5):
        time.sleep(0.01)
        rgb = win32gui.GetPixel(hdc, mousexy[0], mousexy[1] - 80)
        r = (rgb & 0x000000FF) >> 0
        g = (rgb & 0x0000FF00) >> 8
        b = (rgb & 0x00FF0000) >> 16
    for i in range(2):
        time.sleep(1)
        rgb = win32gui.GetPixel(hdc, 875, 242)
        r = (rgb & 0x000000FF) >> 0
        g = (rgb & 0x0000FF00) >> 8
        b = (rgb & 0x00FF0000) >> 16
        if r > 250 and (g > 204 and g < 214) and b < 5:
            time.sleep(1)
            win32api.SetCursorPos((880, 250))
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.SetCursorPos((mousexy[0], mousexy[1]))
            time.sleep(0.1)
        time.sleep(1)
        rgb = win32gui.GetPixel(hdc, mousexy[0], mousexy[1] - 80)
        r = (rgb & 0x000000FF) >> 0
        g = (rgb & 0x0000FF00) >> 8
        b = (rgb & 0x00FF0000) >> 16
        if r < 10 and g < 10 and b < 10:
            key(32, 0.1)
            time.sleep(1.5)
            if i == 0:
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                time.sleep(1)


# Возвращает координаты метки на экране (синий квадрат)
def search_mark():

    try:

        screen = ImageGrab.grab(bbox=(0, 120, 1920, 830))
        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        screen = cv2.inRange(screen, (180, 105, 0), (255, 205, 60))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(screen, cv2.MORPH_CLOSE, kernel)
        closed = cv2.erode(closed, kernel, iterations=1)
        closed = cv2.dilate(closed, kernel, iterations=4)

        # Вычесляет центр прямоугольников
        (centers, hierarchy) = cv2.findContours(
            closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        l2 = len(centers)
        tgt = []
        tgt2 = {}

        for i2 in range(l2):
            L = len(centers[i2])
            x = []
            y = []

            for i in range(L):
                x.append(centers[i2][i][0][0])
                y.append(centers[i2][i][0][1])

            x = int(abs((min(x) + max(x))/2))
            y = int(abs((min(y) + max(y))/2))
            tgt.append([x, y])

        # Находит ближайший центр прямоугольника
        for i3 in range(l2):
            tgtx = tgt[i3][0]
            tgtx = int(round(tgtx - (tgtx - 960)*0.5625, 0))
            tgt2[int(round(math.sqrt(abs(960 - tgtx)**2 + abs(
                355 - tgt[i3][1])**2), 0))] = tgt[i3][0], tgt[i3][1]

        tgt_keys = list(tgt2.keys())
        tgt_keys.sort()

        return [(tgt2[tgt_keys[0]][0]), (tgt2[tgt_keys[0]][1]) + 120]

    except IndexError:

        return None


# Возвращает координаты мертвого зеврима на экране от вида сверху
def search_loot_zevrim_top():
    screen = ImageGrab.grab(bbox=(600, 50, 1390, 830))
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    screen = cv2.inRange(screen, (0, 0, 10), (10, 10, 60))
    screen = cv2.rectangle(screen, (340, 480), (380, 520), (0, 0, 0), -1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 10))
    closed = cv2.morphologyEx(screen, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, kernel, iterations=1)
    closed = cv2.dilate(closed, kernel, iterations=4)

    # Вычесляет центр прямоугольников
    (centers, hierarchy) = cv2.findContours(
        closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    l2 = len(centers)
    tgt = []
    tgt2 = {}

    for i2 in range(l2):
        L = len(centers[i2])
        x = []
        y = []

        for i in range(L):
            x.append(centers[i2][i][0][0])
            y.append(centers[i2][i][0][1])

        x = int(abs((min(x) + max(x))/2))
        y = int(abs((min(y) + max(y))/2))
        tgt.append([x, y])

    # Находит ближайший центр прямоугольника
    for i3 in range(l2):
        tgtx = tgt[i3][0]
        tgtx = int(round(tgtx - (tgtx - 960)*0.5625, 0))
        tgt2[int(round(math.sqrt(abs(960 - tgtx)**2 + abs(
            355 - tgt[i3][1])**2), 0))] = tgt[i3][0], tgt[i3][1]

    tgt_keys = list(tgt2.keys())
    tgt_keys.sort()

    return [(tgt2[tgt_keys[0]][0]) + 600, (tgt2[tgt_keys[0]][1]) + 120]


# Возвращает координаты жилы с торием на миникарте
def search_toriy():
    try:
        screen = ImageGrab.grab(bbox=(1750, 100, 1866, 174))
        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        screen = cv2.inRange(screen, (7, 121, 155), (43, 193, 234))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(screen, cv2.MORPH_CLOSE, kernel)
        closed = cv2.erode(closed, kernel, iterations=1)
        closed = cv2.dilate(closed, kernel, iterations=1)

        # Вычесляет центр прямоугольников
        (centers, hierarchy) = cv2.findContours(
            closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        l2 = len(centers)
        tgt = []
        tgt2 = {}

        for i2 in range(l2):
            L = len(centers[i2])
            x = []
            y = []

            for i in range(L):
                x.append(centers[i2][i][0][0])
                y.append(centers[i2][i][0][1])

            x = int(abs((min(x) + max(x))/2))
            y = int(abs((min(y) + max(y))/2))
            tgt.append([x, y])

        # Находит ближайший центр прямоугольника
        for i3 in range(l2):
            tgtx = tgt[i3][0]
            tgtx = int(round(tgtx - (tgtx - 58), 0))
            tgt2[int(round(math.sqrt(abs(58 - tgtx)**2 + abs(
                100 - tgt[i3][1])**2), 0))] = tgt[i3][0], tgt[i3][1]

        tgt_keys = list(tgt2.keys())
        tgt_keys.sort()

        return [(tgt2[tgt_keys[0]][0]), (tgt2[tgt_keys[0]][1]) + 42]
    except IndexError:
        return False


# Лут трупа
def search_loot():
    try:
        screen = ImageGrab.grab(bbox=(660, 0, 1260, 740))
        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        screen = cv2.inRange(screen, (120, 120, 120), (155, 165, 170))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 2))
        screen = cv2.morphologyEx(screen, cv2.MORPH_CLOSE, kernel)
        screen = cv2.erode(screen, kernel, iterations=1)
        screen = cv2.dilate(screen, kernel, iterations=4)

        # Вычесляет центр прямоугольников
        (centers, hierarchy) = cv2.findContours(
            screen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        l2 = len(centers)
        tgt = []

        for i2 in range(l2):
            L = len(centers[i2])
            x = []
            y = []

            for i in range(L):

                x.append(centers[i2][i][0][0])
                y.append(centers[i2][i][0][1])

            x = int(abs((min(x) + max(x))/2))
            y = int(abs((min(y) + max(y))/2))
            tgt.append([x, y])

        # Сортирует мобов в порядке дальности
        tgt2 = {}

        for i3 in range(l2):

            tgtx = tgt[i3][0]
            tgtx = int(round(tgtx - (tgtx - 960)*0.5625, 0))
            tgt2[int(round(math.sqrt(abs(200 - tgtx)**2 +
                     abs(200 - tgt[i3][1])**2), 0))] = tgt[i3][0], tgt[i3][1]

        tgt_keys = list(tgt2.keys())
        tgt_keys.sort()

        # Кликает по ближайшему неполутанному мобу
        ii = False

        for i4 in range(l2):

            if ii or imdead_:
                break

            win32api.SetCursorPos((960, 0))
            time.sleep(0.1)
            c = win32gui.GetCursorInfo()[1]

            for i5 in range(40):

                if imdead_:
                    break

                win32api.SetCursorPos(((tgt2[tgt_keys[i4]][0] + 660),
                                      (tgt2[tgt_keys[i4]][1] + 50 + i5*5)))
                time.sleep(0.1)

                if c != win32gui.GetCursorInfo()[1]:

                    win32api.SetCursorPos((960, 0))
                    time.sleep(0.1)
                    c = win32gui.GetCursorInfo()[1]
                    (win32api.SetCursorPos(((tgt2[tgt_keys[i4]][0] + 660),
                     (tgt2[tgt_keys[i4]][1] + 50 + (i5+1)*5))))
                    time.sleep(0.1)

                    if c != win32gui.GetCursorInfo()[1]:

                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

                        confirm_loot()

                        ii = True
                        break

            if ((i4 + 1 == l2) and (i5 == 9) and
               (c == win32gui.GetCursorInfo()[1])):

                return None

        return l2

    except IndexError:
        return None


# Лут трупа зеврима
def search_loot_zevrim():
    try:
        screen = ImageGrab.grab(bbox=(860, 480, 1060, 670))
        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        screen = cv2.inRange(screen, (0, 0, 10), (10, 10, 60))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(screen, cv2.MORPH_CLOSE, kernel)
        closed = cv2.erode(closed, kernel, iterations=1)
        closed = cv2.dilate(closed, kernel, iterations=4)

        # Вычесляет центр прямоугольников
        (centers, hierarchy) = cv2.findContours(
            closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        l2 = len(centers)
        tgt = []

        for i2 in range(l2):
            L = len(centers[i2])
            x = []
            y = []

            for i in range(L):

                x.append(centers[i2][i][0][0])
                y.append(centers[i2][i][0][1])

            x = int(abs((min(x) + max(x))/2))
            y = int(abs((min(y) + max(y))/2))
            tgt.append([x, y])

        # Сортирует мобов в порядке дальности
        tgt2 = {}

        for i3 in range(l2):

            tgtx = tgt[i3][0]
            tgtx = int(round(tgtx - (tgtx - 960)*0.5625, 0))
            tgt2[int(round(math.sqrt(abs(200 - tgtx)**2 +
                     abs(200 - tgt[i3][1])**2), 0))] = tgt[i3][0], tgt[i3][1]

        tgt_keys = list(tgt2.keys())
        tgt_keys.sort()

        # Кликает по ближайшему неполутанному мобу
        ii = False

        for i4 in range(l2):

            if ii or imdead_:
                break

            win32api.SetCursorPos((960, 0))
            time.sleep(0.1)
            c = win32gui.GetCursorInfo()[1]

            for i5 in range(40):

                if imdead_:
                    break

                win32api.SetCursorPos(((tgt2[tgt_keys[i4]][0] + 860),
                                      (tgt2[tgt_keys[i4]][1] + 480 + i5*5)))
                time.sleep(0.1)

                if c != win32gui.GetCursorInfo()[1]:

                    win32api.SetCursorPos((960, 0))
                    time.sleep(0.1)
                    c = win32gui.GetCursorInfo()[1]
                    (win32api.SetCursorPos(((tgt2[tgt_keys[i4]][0] + 860),
                     (tgt2[tgt_keys[i4]][1] + 480 + (i5+1)*5))))
                    time.sleep(0.1)

                    if c != win32gui.GetCursorInfo()[1]:

                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

                        confirm_loot()

                        ii = True
                        break

            if ((i4 + 1 == l2) and (i5 == 9) and
               (c == win32gui.GetCursorInfo()[1])):

                return None

        return l2

    except IndexError:
        return None


# Разворот на aro градусов (3204 = 360)
# (если положительно - направо, если отрицательно - налево)
def will(c):
    time.sleep(0.1)
    win32api.SetCursorPos((960, 540))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    r = 1
    c = int(round(c, 0))

    for i in range(abs(c)):
        r += 1
        if r % 440 == 0:
            r -= 439
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.SetCursorPos((960, 540))
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)

        win32api.SetCursorPos((960 + (r * int((c / abs(c)))), 540))
        timer = time.perf_counter()
        while time.perf_counter() - timer < 0.005:
            pass

    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    time.sleep(0.1)


# Разворот на 180 градусов
def will_back():
    time.sleep(0.05)
    win32api.SetCursorPos((960, 540))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)

    for i in range(3):
        win32api.SetCursorPos((1400, 540))
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        time.sleep(0.05)

    win32api.SetCursorPos((1240, 540))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    time.sleep(0.1)


# разворачивает персонажа на гидротвари у колонны
def will_Inpt4():
    rgb = win32gui.GetPixel(hdc, 1799, 5)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8
    b = (rgb & 0x00FF0000) >> 16
    if not ((r > 193 and r < 203) and (g > 162 and g < 172) and
       (b > 11 and b < 21)):
        win32api.SetCursorPos((960, 540))
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        time.sleep(0.1)
        win32api.SetCursorPos((990, 540))
        time.sleep(0.1)
        i = 1
        while not ((r > 193 and r < 203) and (g > 162 and g < 172) and
                   (b > 11 and b < 21)) and not dead():
            if i >= 470:
                i = 1
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                time.sleep(0.1)
                win32api.SetCursorPos((990, 540))
                time.sleep(0.1)
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                time.sleep(0.1)
            win32api.SetCursorPos((990 - i, 540))
            time.sleep(0.02)
            rgb = win32gui.GetPixel(hdc, 1799, 5)
            r = (rgb & 0x000000FF) >> 0
            g = (rgb & 0x0000FF00) >> 8
            b = (rgb & 0x00FF0000) >> 16
            rgb = (r, g, b)
            i += 1
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


# разворачивает персонажа ровно на север (медленно)
def will_360():
    rgb = win32gui.GetPixel(hdc, 1809, 222)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8
    b = (rgb & 0x00FF0000) >> 16
    if not ((r > 185 and r < 190) and (g > 159 and g < 164) and b == 14):
        win32api.SetCursorPos((960, 540))
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        time.sleep(0.1)
        i = 1
        while not ((r > 185 and r < 190) and (g > 159 and g < 164) and
                   b == 14) and not dead():
            if i >= 440:
                i = 1
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                time.sleep(0.1)
                win32api.SetCursorPos((960, 540))
                time.sleep(0.1)
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                time.sleep(0.1)
            win32api.SetCursorPos((960 - i, 540))
            time.sleep(0.02)
            rgb = win32gui.GetPixel(hdc, 1809, 222)
            r = (rgb & 0x000000FF) >> 0
            g = (rgb & 0x0000FF00) >> 8
            b = (rgb & 0x00FF0000) >> 16
            rgb = (r, g, b)
            i += 1
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        time.sleep(0.1)


# разворачивает персонажа ровно на восток (медленно)
def will_270():
    rgb = win32gui.GetPixel(hdc, 1912, 109)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8
    b = (rgb & 0x00FF0000) >> 16
    if not ((r > 185 and r < 195) and (g > 155 and g < 165) and b == 14):
        win32api.SetCursorPos((960, 540))
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        time.sleep(0.1)
        i = 1
        while not ((r > 185 and r < 195) and (g > 155 and g < 165) and
                   b == 14) and not dead():
            if i >= 440:
                i = 1
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                time.sleep(0.1)
                win32api.SetCursorPos((960, 540))
                time.sleep(0.1)
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                time.sleep(0.1)
            win32api.SetCursorPos((960 - i, 540))
            time.sleep(0.03)
            rgb = win32gui.GetPixel(hdc, 1912, 109)
            r = (rgb & 0x000000FF) >> 0
            g = (rgb & 0x0000FF00) >> 8
            b = (rgb & 0x00FF0000) >> 16
            rgb = (r, g, b)
            i += 1
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        time.sleep(0.1)


# Разворот к заданному на экране пикселю (x2, y2)
def will_in_pixel(x2, y2):
    x1 = 960
    if x2 < x1:
        x2 += int(round(abs(x2 - x1)*0.5625, 0))
    elif x2 > x1:
        x2 -= int(round(abs(x2 - x1)*0.5625, 0))
    y1 = 540
    a = x1 - x2
    a2 = y1 - y2
    x = abs(a)
    y = abs(a2)

    if a != 0 and a2 != 0:

        b = (math.atan(x / y)*180/math.pi)/180
        if a > 0 and a2 > 0:
            ang2 = b
        elif a > 0 and a2 < 0:
            ang2 = 1 - b
        elif a < 0 and a2 < 0:
            ang2 = 1 + b
        else:
            ang2 = 2 - b

        if ang2 < 0.1 or ang2 > 1.9:
            return

        if ang2 > 1:
            will((2 - ang2)*1600)
        else:
            will(ang2*-1600)

    if a == 0 and a2 == 0:
        pass
    elif a == 0 and a2 > 0:
        pass
    elif a == 0 and a2 < 0:
        will(1600)
    elif a > 0 and a2 == 0:
        will(-800)
    elif a < 0 and a2 == 0:
        will(800)


# Разворот к заданному на миникарте пикселю пикселю (x2, y2)
def will_pixel_in_map(x2, y2):
    x1 = 58
    y1 = 58
    a = x1 - x2
    a2 = y1 - y2
    x = abs(a)
    y = abs(a2)

    if a != 0 and a2 != 0:

        b = (math.atan(x / y)*180/math.pi)/180
        if a > 0 and a2 > 0:
            ang2 = b
        elif a > 0 and a2 < 0:
            ang2 = 1 - b
        elif a < 0 and a2 < 0:
            ang2 = 1 + b
        else:
            ang2 = 2 - b

        if ang2 > 1:
            will((2 - ang2)*1600)
        else:
            will(ang2*-1600)

    if a == 0 and a2 == 0:
        pass
    elif a == 0 and a2 > 0:
        pass
    elif a == 0 and a2 < 0:
        will(1600)
    elif a > 0 and a2 == 0:
        will(-800)
    elif a < 0 and a2 == 0:
        will(800)


# Определяет форму алззина (True - гумманойдная, False - звериная)
def form_alzin():
    rgb = win32gui.GetPixel(hdc, 501, 68)
    r = (rgb & 0x000000FF) >> 0
    g = (rgb & 0x0000FF00) >> 8
    b = (rgb & 0x00FF0000) >> 16
    if ((r > 162 and r < 172) and (g > 208 and g < 218) and
       (b > 201 and b < 211)):
        return True
    else:
        return False


# поиск цели
def search_target(boxx, boxy, boxx2, boxy2, lenght, hight):
    imgscreen = ImageGrab.grab(bbox=(boxx, boxy, boxx2, boxy2))
    imgscreen = cv2.cvtColor(np.array(imgscreen), cv2.COLOR_RGB2BGR)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (lenght, hight))
    screen = cv2.inRange(imgscreen, (0, 0, 150), (75, 75, 255))
    screen = cv2.morphologyEx(screen, cv2.MORPH_CLOSE, kernel)
    screen = cv2.erode(screen, kernel, iterations=1)
    screen = cv2.dilate(screen, kernel, iterations=4)
    (centers, hierarchy) = cv2.findContours(
        screen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    l2 = len(centers)

    return l2


# поиск цели перед 7м участком
def search_target7(boxx, boxy, boxx2, boxy2, lenght, hight):
    imgscreen = ImageGrab.grab(bbox=(boxx, boxy, boxx2, boxy2))
    imgscreen = cv2.cvtColor(np.array(imgscreen), cv2.COLOR_RGB2BGR)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (lenght, hight))
    screen = cv2.inRange(imgscreen, (0, 0, 245), (75, 75, 255))
    screen = cv2.morphologyEx(screen, cv2.MORPH_CLOSE, kernel)
    screen = cv2.erode(screen, kernel, iterations=1)
    screen = cv2.dilate(screen, kernel, iterations=4)
    (centers, hierarchy) = cv2.findContours(
        screen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    l2 = len(centers)

    return l2


# поиск цели перед 3м участком
def search_target3(boxx, boxy, boxx2, boxy2, lenght, hight):
    imgscreen = ImageGrab.grab(bbox=(boxx, boxy, boxx2, boxy2))
    imgscreen = cv2.cvtColor(np.array(imgscreen), cv2.COLOR_RGB2BGR)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (lenght, hight))
    screen = cv2.inRange(imgscreen, (0, 0, 150), (75, 75, 255))
    screen = cv2.rectangle(screen, (0, 0), (350, 75), (0, 0, 0), -1)
    screen = cv2.morphologyEx(screen, cv2.MORPH_CLOSE, kernel)
    screen = cv2.erode(screen, kernel, iterations=1)
    screen = cv2.dilate(screen, kernel, iterations=4)
    (centers, hierarchy) = cv2.findContours(
        screen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    l2 = len(centers)

    return l2


# поиск цели перед 8м участком
def search_target8(boxx, boxy, boxx2, boxy2, lenght, hight):
    imgscreen = ImageGrab.grab(bbox=(boxx, boxy, boxx2, boxy2))
    imgscreen = cv2.cvtColor(np.array(imgscreen), cv2.COLOR_RGB2BGR)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (lenght, hight))
    screen = cv2.inRange(imgscreen, (0, 0, 245), (75, 75, 255))
    screen = cv2.morphologyEx(screen, cv2.MORPH_CLOSE, kernel)
    screen = cv2.erode(screen, kernel, iterations=1)
    screen = cv2.dilate(screen, kernel, iterations=4)
    (centers, hierarchy) = cv2.findContours(
        screen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    l2 = len(centers)

    return l2


# Полутать Зеврима
def loot_zevrim():

    will(100)
    time.sleep(0.1)
    key(81, 0.5)
    time.sleep(0.1)
    key(87, 2.6)
    time.sleep(0.1)
    will(-800)
    time.sleep(0.1)
    key(87, 1.3)

    time.sleep(0.1)
    win32api.SetCursorPos((960, 540))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    for i in range(1, 50, 1):
        time.sleep(0.02)
        mousexy = win32api.GetCursorPos()
        win32api.SetCursorPos((mousexy[0], mousexy[1] + 20))

    try:
        lootxy = search_loot_zevrim_top()
        lenlootxy = ((math.sqrt(abs(lootxy[0] - 960)**2 +
                     abs(lootxy[1] - 540)**2))*0.0035)
    except Exception:
        pass
    finally:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(2)

    try:
        if lenlootxy < 0.4:
            search_loot_zevrim()
        else:
            lenlootxy -= 0.35
            will_in_pixel(lootxy[0], lootxy[1])
            key(87, lenlootxy)
            time.sleep(2)
            search_loot_zevrim()
            time.sleep(1)
            will_back()
            time.sleep(1)
            key(87, lenlootxy)
            will_back()
            will_in_pixel(abs(lootxy[0] - 1920), lootxy[1])
    except Exception:
        pass


# функция для убийства и лута босса Зеврима
def kill_zevrim():

    # Функция перемещения в одну из трех позиций (0, 1, 2)
    def position_number_go(pos_new, pos_now):
        debuff_per = debuff()
        buff_per = buff()[3]
        pos_go = pos_now - pos_new
        if pos_go == 0:
            return pos_now
        elif pos_go == 1:
            key(69, 0.46)
            pos_now -= 1
            return pos_now
        elif pos_go == 2:
            starttime = time.perf_counter()
            win32api.keybd_event(69, 0, 0, 0)
            while time.perf_counter() - starttime < 0.91:
                if time.perf_counter() - starttime < 0.7:
                    if buff_per:
                        key(54, 0.05)
                    elif not debuff_per[1]:
                        key(49, 0.05)
                    elif not debuff_per[2]:
                        key(50, 0.05)
                    elif not debuff_per[3]:
                        key(51, 0.05)
            win32api.keybd_event(69, 0, win32con.KEYEVENTF_KEYUP, 0)
            pos_now -= 2
            return pos_now
        elif pos_go == -1:
            key(81, 0.45)
            pos_now += 1
            return pos_now
        elif pos_go == -2:
            starttime = time.perf_counter()
            win32api.keybd_event(81, 0, 0, 0)
            while time.perf_counter() - starttime < 0.9:
                if time.perf_counter() - starttime < 0.7:
                    if buff_per:
                        key(54, 0.05)
                    elif not debuff_per[1]:
                        key(49, 0.05)
                    elif not debuff_per[2]:
                        key(50, 0.05)
                    elif not debuff_per[3]:
                        key(51, 0.05)
            win32api.keybd_event(81, 0, win32con.KEYEVENTF_KEYUP, 0)
            pos_now += 2
            return pos_now
        else:
            1/0

    pos_now = 0
    key(83, 0.5)
    key(81, 0.5)
    key2(18, 50, 0.1)
    time.sleep(0.1)
    will(700)
    time.sleep(0.1)
    pos_now = position_number_go(2, pos_now)
    key(50, 0.1)
    pos_now = position_number_go(0, pos_now)
    time.sleep(0.1)

    while status_target()[0 and 1] and not imdead_:
        status_target_per = status_target()
        debuff_per = debuff()
        resurs_player_per = resurs_player()
        nf = nf_sifon()[0]

        if ((debuff_per[1:4] != [True, True, True] or nf) and
           status_target_per[2] >= 30 and pos_now == 0):
            pos_now = position_number_go(2, pos_now)
            pos_now = position_number_go(0, pos_now)

        elif status_target_per[2] < 30:
            if (resurs_player_per[0] - resurs_player_per[1] > 20 and
               resurs_player_per[0] > 20):
                key(57, 0.1)
            pos_now = position_number_go(0, pos_now)

        elif status_target_per[2] >= 30:
            if (resurs_player_per[0] - resurs_player_per[1] > 20 and
               resurs_player_per[0] > 20):
                key(57, 0.1)
            pos_now = position_number_go(1, pos_now)

    pos_now = position_number_go(2, pos_now)

    loot_zevrim()


# Ротация в бою с Алззином
def rotation_alzin(stoptimer):
    starttimer = time.perf_counter()
    while time.perf_counter() - starttimer < stoptimer - 0.1:
        hrc_ = health_resurs_corrapt()
        distance_ = distance()
        healstone_ = saveitem()[0]
        nf_sifon_ = nf_sifon()
        coil_cd_ = coil_cd()
        curse_ = curse()
        if hrc_[0] < 45 and healstone_:
            key2(18, 57, 0)
        elif hrc_[0] < 80 and coil_cd_ == 1 and distance_ < 100:
            key(187, 0)
        elif nf_sifon_[0] and distance_ < 36:
            key(54, 0)
        elif not nf_sifon_[1] and distance_ < 100:
            key(51, 0)
        elif not curse_ and distance_ < 100:
            key(50, 0)
        elif not hrc_[2] and distance_ < 100:
            key(49, 0)
        elif ((hrc_[0] > 80 and hrc_[1] < 80) or
              (hrc_[1] < 20 and hrc_[0] > 40)):
            key(57, 0)


# Функция перемещения в двух позициях на Алззине
def position_number_go_allzin(pos_new, pos_now):
    if pos_new != pos_now:
        if pos_new == 1:
            win32api.keybd_event(69, 0, 0, 0)
            rotation_alzin(0.675)
            win32api.keybd_event(69, 0, win32con.KEYEVENTF_KEYUP, 0)
            return 1
        elif pos_new == 0:
            key2(81, 32, 0)
            rotation_alzin(1)
            return 0
    else:
        return pos_now


# Копает руду, обнаруженную на миникарте (максимальное приближение камеры)
def mine_toriy():
    lootxy = search_toriy()
    if not lootxy:
        return False
    will_pixel_in_map(lootxy[0], lootxy[1])
    lenlootxy = ((math.sqrt(abs(lootxy[0] - 58)**2 +
                 abs(lootxy[1] - 58)**2))*0.03)
    key(87, lenlootxy)
    while True:
        time.sleep(0.1)
        win32api.SetCursorPos((960, 0))
        time.sleep(0.1)
        cursorform = win32gui.GetCursorInfo()[1]
        time.sleep(0.1)
        win32api.SetCursorPos((960, 540))
        time.sleep(0.1)
        if win32gui.GetCursorInfo()[1] != cursorform:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            confirm_loot()
        else:
            break
    will_back()
    key(87, lenlootxy)
    will_back()
    will_pixel_in_map(abs(lootxy[0] - 116), lootxy[1])


# Обновить данж
def resetdange():
    global numberdange
    global excessnumberdange
    global numberdeath
    global durancyitem
    win32api.keybd_event(83, 0, 0, 0)
    win32api.keybd_event(69, 0, 0, 0)
    while not loadscreen():
        time.sleep(0.1)
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(69, 0, win32con.KEYEVENTF_KEYUP, 0)
    while loadscreen():
        time.sleep(0.1)
    time.sleep(1)
    win32api.SetCursorPos((70, 70))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    time.sleep(0.5)
    win32api.SetCursorPos((220, 290))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.SetCursorPos((875, 245))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)
    numberdange += 1
    win32api.keybd_event(83, 0, 0, 0)
    print("Дм восток обновлен " + str(numberdange) + " раз, успешно пройден "
          + str(excessnumberdange) + " раз, смертей " + str(numberdeath)
          + ", прочность предметов " + str(durancyitem) + "%. " +
          time.strftime("%H:%M:%S", time.localtime()))
    while not loadscreen():
        time.sleep(0.1)
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)
    while loadscreen():
        time.sleep(0.1)
    time.sleep(1)


# Бафнутся и выйти в меню на 5 минут
def buff_quit():
    global excessnumberdange
    time.sleep(0.1)
    win32api.SetCursorPos((130, 995))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)
    while disenchant():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(1)
    key2(18, 48, 0)
    time.sleep(1)
    rotation_buff()
    key(27, 0)
    win32api.SetCursorPos((960, 615))
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    while not debuff_player():
        time.sleep(1)
    excessnumberdange += 1
    time.sleep(305)
    key(13, 0)
    time.sleep(1)
    while loadscreen():
        time.sleep(0.1)
    time.sleep(1)


# Возвращает из строки все цифры
def nextname(name):
    L = len(name)
    integ = []
    i = 0
    while i < L:
        s_int = ''
        a = name[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i < L:
                a = name[i]
            else:
                break
        i += 1
        if s_int != '':
            integ.append(int(s_int))
    return integ


# Демонический поток проверки событий
def daemon():
    global target_
    global target_patrool_daemon
    global mine_toriy_daemon
    global toriy_
    while True:
        time.sleep(0.3)
        if target_patrool_daemon:
            target_ = target()
            if not target_[0] or not target_[1] or target_[2] > 24:
                win32api.keybd_event(48, 0, 0, 0)
                win32api.keybd_event(48, 0, win32con.KEYEVENTF_KEYUP, 0)
        if mine_toriy_daemon:
            toriy_ = search_toriy()


# Демонический поток проверки событий
def daemon_imdead():
    global imdead_daemon
    global imdead_
    while True:
        time.sleep(1)
        if imdead_daemon:
            imdead_ = dead()


# Запуск тела скрипта
def go():
    global target_
    global target_patrool_daemon
    global mine_toriy_daemon
    global imdead_daemon
    global toriy_
    global imdead_
    global durancyitem
    global numberdeath
    global excessnumberdange
    imawake = False
    name = 'Inpt1.txt'

    while os.path.exists(name):
        imdead_ = dead()
        toriy_ = False
        flag_Inpt5 = True
        target_ = target()
        if imdead_ and not imawake:
            name = 'Inpt0.txt'
            imawake = True
        maini = 0
        file = open(name, 'r')
        text = file.readlines()
        file.close()
        text = [i.replace('\n', '') for i in text]
        time_ = []
        mousepos = []
        keys = []
        mousekeys = []

        for i in range(len(text)):
            if i % 4 == 0:
                time_.append(float(text[i]))
            elif i % 4 == 1:
                text[i] = text[i].replace('(', '')
                text[i] = text[i].replace(')', '')
                text[i] = text[i].split(', ')
                mousepos.append([int(i) for i in text[i]])
            elif i % 4 == 2:
                text[i] = text[i].replace('[', '')
                text[i] = text[i].replace(']', '')
                text[i] = text[i].split(', ')
                keys.append([int(i) for i in text[i]])
            elif i % 4 == 3:
                text[i] = text[i].replace('[', '')
                text[i] = text[i].replace(']', '')
                text[i] = text[i].split(', ')
                mousekeys.append([int(i) for i in text[i]])

        del(text)

        time_ = tuple(time_)
        mousepos = tuple([tuple(i) for i in mousepos])
        keys = tuple([tuple(i) for i in keys])
        mousekeys = tuple([tuple(i) for i in mousekeys])
        len_time_ = len(time_)

        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

        if win32api.GetAsyncKeyState(87) not in range(2):
            win32api.keybd_event(87, 0, win32con.KEYEVENTF_KEYUP, 0)

        for i in range(127):
            if win32api.GetAsyncKeyState(i) not in range(2) and i != 87:
                win32api.keybd_event(i, 0, win32con.KEYEVENTF_KEYUP, 0)

        if name != 'Inpt0.txt':
            imdead_daemon = True

        if name == 'Inpt0.txt':
            time.sleep(1)
            win32api.SetCursorPos((960, 245))
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            while not loadscreen():
                time.sleep(0.1)
            while loadscreen():
                time.sleep(0.1)
            time.sleep(1)
        elif name == 'Inpt1.txt' and imawake:
            if dead():
                win32api.keybd_event(87, 0, 0, 0)
                while not loadscreen():
                    time.sleep(0.1)
                win32api.keybd_event(48, 0, win32con.KEYEVENTF_KEYUP, 0)
                while loadscreen():
                    time.sleep(0.1)
                while dead() and imdead_:
                    time.sleep(0.1)
            time.sleep(1)
            imawake = False
            imdead_ = False
            key2(18, 187, 0)
            durancyitem == DurancyItem()
            rotation_buff()
            resetdange()

        elif name == 'Inpt2.txt':
            key(189, 0)
            starttimer_Inpt2 = time.perf_counter()
            while time.perf_counter() - starttimer_Inpt2 < 60:
                key(48, 0)
                time.sleep(0.1)
                target_Inpt2 = target()
                if (target_Inpt2[0] and target_Inpt2[1] and
                   target_Inpt2[2] in range(10, 37)):
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                    rotation()
                    mousepos2 = win32api.GetCursorPos()
                    time.sleep(0.1)
                    win32api.SetCursorPos(
                        (mousepos2[0], mousepos2[1] - 10))
                    time.sleep(0.1)
                    win32api.SetCursorPos((mousepos2[0], mousepos2[1]))
                    time.sleep(0.1)
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                    time.sleep(0.1)
                    rotation_buff()
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                    confirm_loot()
                    while debuff_player():
                        time.sleep(0.1)
                    break

        elif name == 'Inpt3.txt':
            while search_target(714, 295, 957, 493, 1, 1) == 0 and not imdead_:
                time.sleep(0.2)
            while search_target(714, 295, 957, 493, 1, 1) != 0 and not imdead_:
                time.sleep(0.2)
        elif name == 'Inpt4.txt':
            key2(87, 69, 0.5)
            time.sleep(0.1)
            will_Inpt4()
        elif name == 'Inpt5.txt':
            if target() == (True, True, 10):
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                rotation()
                mousepos2 = win32api.GetCursorPos()
                time.sleep(0.1)
                win32api.SetCursorPos(
                    (mousepos2[0], mousepos2[1] - 10))
                time.sleep(0.1)
                win32api.SetCursorPos((mousepos2[0], mousepos2[1]))
                time.sleep(0.1)
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                time.sleep(0.1)
                rotation_buff()
                while debuff_player():
                    time.sleep(0.1)

            win32api.SetCursorPos((960, 0))
            time.sleep(0.1)
            c = win32gui.GetCursorInfo()[1]
            win32api.SetCursorPos((960, 540))
            time.sleep(0.1)
            if c != win32gui.GetCursorInfo()[1]:
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                confirm_loot()
            key(48, 0)
            time.sleep(0.5)
            if target() == (True, True, 24) or target() == (True, True, 10):
                for i in range(20):
                    key(48, 0)
                    time.sleep(0.5)
                    if distance() == 10:
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                        rotation()
                        mousepos2 = win32api.GetCursorPos()
                        time.sleep(0.1)
                        win32api.SetCursorPos(
                            (mousepos2[0], mousepos2[1] - 10))
                        time.sleep(0.1)
                        win32api.SetCursorPos((mousepos2[0], mousepos2[1]))
                        time.sleep(0.1)
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                        time.sleep(0.1)
                        rotation_buff()
                        search_loot()
                        while debuff_player():
                            time.sleep(0.1)
                        break
                else:
                    if distance() == 24 and not combat():
                        key(51, 0)
                        will_back()
                        win32api.keybd_event(87, 0, 0, 0)
                        time.sleep(0.5)
                        win32api.keybd_event(69, 0, 0, 0)
                        time.sleep(0.5)
                        win32api.keybd_event(
                            69, 0, win32con.KEYEVENTF_KEYUP, 0)
                        time.sleep(0.5)
                        key(50, 0)
                        time.sleep(1.5)
                        key(49, 0)
                        time.sleep(0.5)
                        win32api.keybd_event(
                            87, 0, win32con.KEYEVENTF_KEYUP, 0)
                        will_back()
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                        rotation()
                        mousepos2 = win32api.GetCursorPos()
                        time.sleep(0.1)
                        win32api.SetCursorPos(
                            (mousepos2[0], mousepos2[1] - 10))
                        time.sleep(0.1)
                        win32api.SetCursorPos((mousepos2[0], mousepos2[1]))
                        time.sleep(0.1)
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                        time.sleep(0.1)
                        rotation_buff()
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                        time.sleep(0.1)
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                        confirm_loot()
                        while debuff_player():
                            time.sleep(0.1)
                        key69tumbler = 0
                        timer = 0.0
                        lesttime = time.perf_counter()
                        win32api.keybd_event(87, 0, 0, 0)
                        target_patrool_daemon = True
                        while timer < 3.5:
                            timertime = time.perf_counter()
                            deltatime = timertime - lesttime
                            lesttime = timertime
                            timer += deltatime
                            if target_ == (True, True, 10):
                                win32api.keybd_event(
                                    69, 0, win32con.KEYEVENTF_KEYUP, 0)
                                win32api.keybd_event(
                                    87, 0, win32con.KEYEVENTF_KEYUP, 0)
                                win32api.mouse_event(
                                    win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                                rotation()
                                mousepos2 = win32api.GetCursorPos()
                                time.sleep(0.1)
                                win32api.SetCursorPos(
                                    (mousepos2[0], mousepos2[1] - 10))
                                time.sleep(0.1)
                                win32api.SetCursorPos(
                                    (mousepos2[0], mousepos2[1]))
                                time.sleep(0.1)
                                win32api.mouse_event(
                                    win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                                time.sleep(0.1)
                                rotation_buff()
                                search_loot()
                                if timer > 2.5 and timer < 3:
                                    win32api.keybd_event(69, 0, 0, 0)
                                win32api.keybd_event(87, 0, 0, 0)
                                lesttime = time.perf_counter()
                            elif timer > 2.5 and key69tumbler == 0:
                                win32api.keybd_event(69, 0, 0, 0)
                                key69tumbler = 1
                            elif timer > 3 and key69tumbler == 1:
                                win32api.keybd_event(
                                    69, 0, win32con.KEYEVENTF_KEYUP, 0)
                                key69tumbler = 2
                        win32api.keybd_event(
                            87, 0, win32con.KEYEVENTF_KEYUP, 0)
                        time.sleep(0.1)
            will_Inpt4()
        elif name == 'Inpt6.txt':
            kill_zevrim()
        elif name == 'Inpt7.txt':
            will_360()
        elif name == 'Inpt8.txt':
            while (search_target(730, 220, 1190, 500, 40, 4) == 0
                   and not imdead_):
                time.sleep(0.2)
            time.sleep(4)
            key(87, 8)
            time.sleep(0.1)
            win32api.SetCursorPos((950, 300))
            time.sleep(1.5)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            time.sleep(1.5)
            win32api.SetCursorPos((170, 430))
            time.sleep(1.5)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(1.5)
            will_back()
            while (search_target7(830, 240, 1180, 340, 40, 4) == 0
                   and not imdead_):
                time.sleep(0.2)
            time.sleep(3)
            key(87, 8)
            time.sleep(0.1)
            will(-1400)
            while (search_target(0, 220, 1920, 500, 40, 4) != 0
                   and not imdead_):
                time.sleep(0.5)
        elif name == 'Inpt9.txt':
            time.sleep(0.1)
            key(69, 0.1)
            while (search_target8(810, 120, 1200, 530, 10, 3) == 0
                   and not imdead_):
                time.sleep(1)
            while (search_target8(810, 120, 1200, 530, 10, 3) != 0
                   and not imdead_):
                time.sleep(1)
        elif name == 'Inpt10.txt':
            while (search_target(740, 270, 900, 420, 10, 2) == 0
                   and not imdead_):
                time.sleep(0.2)
            while (search_target(1120, 315, 1285, 470, 10, 2) == 0
                   and not imdead_):
                time.sleep(0.2)
            time.sleep(2)
        elif name == 'Inpt11.txt':
            will_360()
            key(83, 1)
            time.sleep(0.1)
            will(-801)
            if search_target(750, 0, 1110, 620, 1, 1) != 0:
                while (search_target(750, 0, 1110, 620, 1, 1) != 0
                       and not imdead_):
                    time.sleep(0.2)
                time.sleep(5)
        elif name == 'Inpt12.txt':
            while combat():
                time.sleep(0.2)
            key(87, 1)
            will(600)
            key2(83, 81, 0.4)
            key(87, 0.3)

            key2(18, 49, 0)
            position_now = 0
            timeralzin = True
            starttimer = 0
            position_now = position_number_go_allzin(1, position_now)
            while not combat():
                key(50, 0.1)
            rotation_alzin(0.5)
            position_now = position_number_go_allzin(0, position_now)
            key2(83, 81, 0.7)
            while (time.perf_counter() - starttimer < 10 or
                   timeralzin and not imdead_):
                rotation_alzin(1)
                if timeralzin and status_target()[3] <= 50:
                    timeralzin = False
                    starttimer = time.perf_counter()
                if status_target()[2] < 100:
                    while status_target()[2] < 100 and not imdead_:
                        rotation_alzin(0.2)
                        if timeralzin and status_target()[3] <= 50:
                            timeralzin = False
                            starttimer = time.perf_counter()
                    rotation_alzin(1.4)
                    if status_target()[3] == 10:
                        position_now = position_number_go_allzin(
                            1, position_now)
                        rotation_alzin(5)
                        position_now = position_number_go_allzin(
                            0, position_now)
                    if timeralzin and status_target()[3] <= 50:
                        timeralzin = False
                        starttimer = time.perf_counter()

                if timeralzin and status_target()[3] <= 50:
                    timeralzin = False
                    starttimer = time.perf_counter()
                position_now = position_number_go_allzin(1, position_now)
                if timeralzin and status_target()[3] <= 50:
                    timeralzin = False
                    starttimer = time.perf_counter()
                if not form_alzin() and timeralzin:
                    rotation_alzin(0.5)
                    if timeralzin and status_target()[3] <= 50:
                        timeralzin = False
                        starttimer = time.perf_counter()
                rotation_alzin(0.3)
                if timeralzin and status_target()[3] <= 50:
                    timeralzin = False
                    starttimer = time.perf_counter()
                position_now = position_number_go_allzin(0, position_now)
                if timeralzin and status_target()[3] <= 50:
                    timeralzin = False
                    starttimer = time.perf_counter()
            time.sleep(1.25)
            key2(81, 83, 0.35)

        elif name == 'Inpt13.txt':
            time.sleep(0.1)
            win32api.SetCursorPos((960, 540))
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            win32api.SetCursorPos((480, 540))
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            time.sleep(0.1)
            will_270()
            starttime12 = time.perf_counter()
            while combat():
                if time.perf_counter() - starttime12 > 60:
                    key(81, 0.5)
                    key(69, 1)
                    starttime12 = time.perf_counter()
            time.sleep(5)
            starttime12 = time.perf_counter()
            while (not buff()[7] or combat()) and not imdead_:
                if time.perf_counter() - starttime12 > 60:
                    key(81, 0.5)
                    key(69, 1)
                    starttime12 = time.perf_counter()
                while combat():
                    if time.perf_counter() - starttime12 > 60:
                        key(81, 0.5)
                        key(69, 1)
                        starttime12 = time.perf_counter()
                key2(18, 189, 0)
                time.sleep(9)

        time.sleep(0.1)

        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

        if win32api.GetAsyncKeyState(87) not in range(2):
            win32api.keybd_event(87, 0, win32con.KEYEVENTF_KEYUP, 0)

        for i in range(127):
            if win32api.GetAsyncKeyState(i) not in range(2) and i != 87:
                win32api.keybd_event(i, 0, win32con.KEYEVENTF_KEYUP, 0)

        time.sleep(0.1)

        if name in ('Inpt2.txt', 'Inpt4.txt', 'Inpt5.txt', 'Inpt7.txt'):
            target_patrool_daemon = True
        if name == 'Inpt14.txt':
            mine_toriy_daemon = True

        lesttime = time.perf_counter()
        timer = 0.0
        while maini < len_time_:
            timertime = time.perf_counter()
            deltatime = timertime - lesttime
            lesttime = timertime
            timer += deltatime

            if timer > time_[maini]:

                if (win32api.GetAsyncKeyState(win32con.VK_RBUTTON)
                   in range(2) and mousekeys[maini][1] not in range(2)):
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)

                elif (win32api.GetAsyncKeyState(win32con.VK_RBUTTON)
                      not in range(2) and mousekeys[maini][1] in range(2)):
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

                if (win32api.GetAsyncKeyState(win32con.VK_LBUTTON)
                   in range(2) and mousekeys[maini][0] not in range(2)):
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

                elif (win32api.GetAsyncKeyState(win32con.VK_LBUTTON)
                      not in range(2) and mousekeys[maini][0] in range(2)):
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

                if (win32api.GetAsyncKeyState(win32con.VK_MBUTTON)
                   in range(2) and mousekeys[maini][2] not in range(2)):
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)

                elif (win32api.GetAsyncKeyState(win32con.VK_MBUTTON)
                      not in range(2) and mousekeys[maini][2] in range(2)):
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

                if win32api.GetCursorPos() != mousepos[maini]:
                    win32api.SetCursorPos(
                        (mousepos[maini][0], mousepos[maini][1]))

                for i in range(127):

                    if win32api.GetAsyncKeyState(i) != keys[maini][i]:

                        if (win32api.GetAsyncKeyState(i) not in range(2) and
                           keys[maini][i] == 0):
                            win32api.keybd_event(
                                i, 0, win32con.KEYEVENTF_KEYUP, 0)

                        elif (win32api.GetAsyncKeyState(i) in range(2) and
                              keys[maini][i] != 0):
                            win32api.keybd_event(i, 0, 0, 0)

                maini += 1

            elif imdead_ and name != 'Inpt0.txt':
                numberdeath += 1
                print("Смерть в " + name + " в моменте " + str(time_[maini]) +
                      ". " + time.strftime("%H:%M:%S", time.localtime()))
                break

            elif (name == 'Inpt5.txt' and maini == 5154 and target_[0] and
                  target_[1] and flag_Inpt5):
                target_patrool_daemon = False
                starttimer_Inpt5 = time.perf_counter()
                while time.perf_counter() - starttimer_Inpt5 < 30:
                    key(48, 0)
                    time.sleep(0.1)
                    target_Inpt5 = target()
                    if (target_Inpt5[0] and target_Inpt5[1] and
                       target_Inpt5[2] == 10):
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                        rotation()
                        mousepos2 = win32api.GetCursorPos()
                        time.sleep(0.1)
                        win32api.SetCursorPos(
                            (mousepos2[0], mousepos2[1] - 10))
                        time.sleep(0.1)
                        win32api.SetCursorPos((mousepos2[0], mousepos2[1]))
                        time.sleep(0.1)
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                        time.sleep(0.1)
                        rotation_buff2()
                        search_loot()
                        while debuff_player():
                            time.sleep(0.1)
                        win32api.SetCursorPos((mousepos2[0], mousepos2[1]))
                        time.sleep(0.1)
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                        time.sleep(0.1)

                flag_Inpt5 = False
                lesttime = time.perf_counter()
                target_patrool_daemon = True

            elif (target_ == (True, True, 10) and name != 'Inpt0.txt'
                  and maini > 0):
                target_patrool_daemon = False

                if win32api.GetAsyncKeyState(87) not in range(2):
                    win32api.keybd_event(
                        87, 0, win32con.KEYEVENTF_KEYUP, 0)
                for i in range(127):
                    if win32api.GetAsyncKeyState(i) not in range(2):
                        win32api.keybd_event(
                            i, 0, win32con.KEYEVENTF_KEYUP, 0)

                time.sleep(0.1)

                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

                time.sleep(0.1)
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                rotation()
                mousepos2 = win32api.GetCursorPos()
                time.sleep(0.1)
                win32api.SetCursorPos((mousepos2[0], mousepos2[1] - 10))
                time.sleep(0.1)
                win32api.SetCursorPos((mousepos2[0], mousepos2[1]))
                time.sleep(0.1)
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                time.sleep(0.1)

                if name == 'Inpt2.txt' or name == 'Inpt4.txt':
                    rotation_buff()
                    while debuff_player():
                        time.sleep(1)
                else:
                    while debuff_player():
                        rotation_buff2()

                search_loot()
                time.sleep(0.1)

                target_ = target()

                maini -= 1
                win32api.SetCursorPos((mousepos[maini][0], mousepos[maini][1]))
                time.sleep(0.1)
                lesttime = time.perf_counter()
                target_patrool_daemon = True

            elif toriy_ and name == 'Inpt14.txt' and maini > 0:
                mine_toriy_daemon = False
                if win32api.GetAsyncKeyState(87) not in range(2):
                    win32api.keybd_event(
                        87, 0, win32con.KEYEVENTF_KEYUP, 0)
                for i in range(127):
                    if win32api.GetAsyncKeyState(i) not in range(2):
                        win32api.keybd_event(
                            i, 0, win32con.KEYEVENTF_KEYUP, 0)

                time.sleep(0.1)

                win32api.mouse_event(
                    win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

                mine_toriy()
                toriy_ = False

                time.sleep(0.1)
                maini -= 1
                win32api.SetCursorPos((mousepos[maini][0], mousepos[maini][1]))
                time.sleep(0.1)
                lesttime = time.perf_counter()
                mine_toriy_daemon = True

        target_patrool_daemon = False
        mine_toriy_daemon = False
        imdead_daemon = False

        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

        if win32api.GetAsyncKeyState(87) not in range(2):
            win32api.keybd_event(87, 0, win32con.KEYEVENTF_KEYUP, 0)

        for i in range(127):
            if win32api.GetAsyncKeyState(i) not in range(2) and i != 87:
                win32api.keybd_event(i, 0, win32con.KEYEVENTF_KEYUP, 0)

        name = 'Inpt' + str(nextname(name)[0] + 1) + '.txt'


# Функция потока прохождения данжа
def daemon_go():
    global numberdange
    global durancyitem
    global excessnumberdange
    global numberdeath
    numberdange = 0
    numberdeath = 0
    excessnumberdange = 0
    durancyitem = DurancyItem()
    while numberdange < 30:
        go()
        durancyitem = DurancyItem()
        buff_quit()
        resetdange()


try:
    while win32api.GetAsyncKeyState(192) == 0:
        pass

    time.sleep(1)
    durancyitem = 100
    hwnd = win32gui.GetActiveWindow()
    hdc = win32gui.GetDC(hwnd)

    target_patrool_daemon = False
    mine_toriy_daemon = False
    imdead_daemon = False
    daemonthread = threading.Thread(target=daemon, daemon=True)
    daemonthread_imdead = threading.Thread(target=daemon_imdead, daemon=True)
    daemonthread_go = threading.Thread(target=daemon_go, daemon=True)
    daemonthread.start()
    daemonthread_imdead.start()
    daemonthread_go.start()
    threadlock = threading.RLock()

    while True:
        if (win32api.GetAsyncKeyState(46) != 0 or numberdange == 30
           or durancyitem < 15):
            raise SystemExit
finally:
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

    for i in range(127):
        if win32api.GetAsyncKeyState(i) != 0:
            win32api.keybd_event(i, 0, win32con.KEYEVENTF_KEYUP, 0)
