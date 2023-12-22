import pyautogui
import pyscreenshot as ImageGrab
from time import sleep
import pytesseract
from PIL import Image
import difflib
import winsound


from coordinates import *

def sound():
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)

def get_cord_color(cords:Cords):
    im=ImageGrab.grab(bbox=(cords.x,cords.y,cords.x+1,cords.y+1)).load()
    return im[0, 0]

def click(cords:Cords|Button|NPC, double=False):
    if type(cords) == Cords:
        pyautogui.moveTo((cords.x, cords.y))
        if double:
            pyautogui.mouseDown(cords.x, cords.y)
            pyautogui.mouseUp(cords.x, cords.y)
        pyautogui.mouseDown(cords.x, cords.y)
        pyautogui.mouseUp(cords.x, cords.y)
    elif type(cords) == NPC:
        color = get_cord_color(cords.check_cords)
        while color != cords.check_color:
            click(cords.screen_cords)
            sleep(1)
            color = get_cord_color(cords.check_cords)
    elif type(cords) == Button:
        if cords.reverse:
            color = get_cord_color(cords.cords_check)
            while color == cords.check_color:
                click(cords.cords)
                color = get_cord_color(cords.cords_check)
        else:
            color = get_cord_color(cords.cords_check)
            while color != cords.check_color:
                click(cords.cords)
                sleep(0.1)
                color = get_cord_color(cords.cords_check)

def print_pos():
    while 1:
        print(pyautogui.position())
        sleep(1)

def write_cords(cords:Cords):
    click(radar_input_x)
    pyautogui.write(str(cords.x))
    sleep(0.1)
    click(radar_input_y)
    click(radar_input_y)
    pyautogui.write(str(cords.y))
    sleep(0.1)
    click(radar_confirm_btn)

def get_cords_im(pos1:Cords, pos2:Cords, file_name:str="test.png", mode:str="binary", thresh=200, add_pixel:[(int, int)]=None):
    im=ImageGrab.grab(bbox=(pos1.x, pos1.y, pos2.x, pos2.y))
    if mode == "binary":
        im=im.convert('L')
        width, height = im.size
        for x in range(width):
            for y in range(height):
                if im.getpixel((x, y)) < thresh:
                    im.putpixel((x, y), 0)
                else:
                    im.putpixel((x, y), 255)
    if add_pixel:
        if im.getpixel((11, 3)) == 255:
            for cords in add_pixel:
                im.putpixel((cords[0], cords[1]), 255)
    # im.show()
    # input()
    im.save(file_name)

def get_text(file_name:str, mode:str="number") -> str:
    if mode == "number":
        config = f'--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'
    elif mode == "text":
        config = None
    ocr_result = pytesseract.image_to_string(Image.open(file_name), config=config)
    return ocr_result

def get_cords_from_scroll(open_count):
    pixels = [(11, 1), (11, 8), (7, 1), (7, 8), (11, 4), (7, 4), (10, 3)]
    cords_to_check = []
    pixel_list = pixels.copy()
    result = []
    for pixel_cord in pixels:
        # двигаем мышку на позицию скрола
        click(scroll_position)
        # вырезаем скрин координат
        get_cords_im(scroll_cords_pos1, scroll_cords_pos2)
        # запускаем распознование
        cords_string = get_text("test.png")
        x_cord = cords_string[:3].strip()
        y_cord = cords_string[3:].strip()

        # cords_to_check.append((x_cord, y_cord))
        if (x_cord, y_cord) not in cords_to_check:
            # print(f"Проверка координаты Y обнаружила несоответствие. Переопределение координаты на {y2_cord}")
            cords_to_check.append((x_cord, y_cord))
            if int(y_cord) == 957:
                cords_to_check.append((x_cord, 987))
            elif int(y_cord) == 967:
                cords_to_check.append((x_cord, 987))
        get_cords_im(scroll_cords_pos1_only_y, scroll_cords_pos2_only_y, add_pixel=pixel_list)
        # print(f"Получены координаты сокровищ: {x_cord}, {y_cord} ({open_count})")
        y2_cord = get_text("test.png").strip()
        if (x_cord, y2_cord) not in cords_to_check:
            # print(f"Проверка координаты Y обнаружила несоответствие. Переопределение координаты на {y2_cord}")
            cords_to_check.append((x_cord, y2_cord))
        else:
            break
        pixel_list.remove(pixel_cord)
        
    for cords in cords_to_check:
        try:
            x_cord = int(cords[0])
            y_cord = int(cords[1])
        except:
            continue
        if 400 <= x_cord <= 500 and 900 <= y_cord <= 1100:
            result.append(Cords(x_cord, y_cord))
    return result[::-1]
    


def wait_running():
    while 1:
        cords1 = get_char_cord(150)
        sleep(0.5)
        cords2 = get_char_cord(150)
        # print(cords1, cords2)
        if cords1 == cords2:
            return True

def get_location():
    get_cords_im(location_name_pos1, location_name_pos2, "location.png", thresh=160)
    return get_text("location.png", mode="text").strip().strip(".‘")

def check_location():
    location = get_location()
    if difflib.SequenceMatcher(None, "Treasure Gulf", location).ratio() < 0.9 and difflib.SequenceMatcher(None, "Pirate Hideout", location).ratio() < 0.9:
        return False
    return True

def open_scroll():
    location = True
    color = get_cord_color(scroll_position)
    open_count = 0
    while get_cord_color(scroll_position) == color and location == True and open_count < 30:
        # location = False
        click(scroll_position, double=True)
        location = check_location()
        open_count += 1
    if open_count == 30:
        print("!!! Не удалось открыть НП !!!")
        return False
    if check_location() == False:
        print(f"Локация не Treasure Gulf")
        move_to_treasure_gulf()
        return False
    return True
    
def move_to_treasure_gulf():
    print("Отправляемся в Treasure Gulf")
    if check_location() == True:
        print("Уже там! Ложное срабатывание!")
        return 1
    click(center)
    click(center)
    click(sitdown_btn)
    while not dead() and get_location() not in ("Magical Ocean", "Shaitan City"):
        # print(get_location())
        # click(health_pot)
        use_old_ticket()
        sleep(1)
    if dead():
        click(revive_confirm_btn)
        sleep(1)
    print("Прибыли в порт Шайтана")
    go_to_npc(NPCS.harbor_operator_mark)
    print("Подошли к Марку")
    talk_with_npc(NPCS.harbor_operator_mark)
    repair_ship()
    talk_with_npc(NPCS.harbor_operator_mark)
    refuel_ship()
    talk_with_npc(NPCS.harbor_operator_mark)
    choose_ship()
    print("Вышли в море")
    sea_move_to(Navigation.from_shai_to_treasure_island_portal)
    print("Прыгнули в портал")
    sea_move_to(Navigation.from_treasure_island_portal_to_treasure_island_harbor)
    print("Высадились на остров сокровищ")
    click(inventory_btn)
    # sound()
    
def repair_ship():
    click(Cords(1147, 1256))
    sleep(1)
    click(Cords(1249, 155))
    sleep(1)

def refuel_ship():
    click(Cords(1147, 1278))
    sleep(1)
    click(Cords(1249, 155))
    sleep(1)

def sea_move_to(clicks):
    for cords in clicks:
        click(cords)
        wait_running()

def choose_ship():
    click(Cords(1147, 1233))
    sleep(1)
    click(Cords(1249, 155))
    sleep(1)

def go_to_npc(npc:NPC):
    for cords in npc.position:
        click(radar_btn)
        write_cords(cords)
        wait_running()

def talk_with_npc(npc:NPC):
    click(npc)
    sleep(1)


def dead():
    if get_cord_color(death_indicator) == (235, 235, 235):
        return True
    return False

def use_old_ticket():
    click(old_ticket)

def get_scroll():
    i = 5
    while get_cord_color(scroll_position) != scroll_color and i > 0:
        # нажать на первую ячейку
        click(purple_pirate_scroll_position, double=True)
        i -= 1
    if i <= 0:
        print("Закончились НП")
        input()

def get_char_cord(x):
    get_cords_im(char_cord1, char_cord2, file_name="char_cords.png", thresh=x)
    cords_string = get_text("char_cords.png")
    x = cords_string[:3].strip()
    y = cords_string[3:].strip()
    try:
        return Cords(int(x), int(y))
    except ValueError:
        return Cords(0, 0)

def move_to_farm_spot():
    char_cord = get_char_cord()
    # print(char_cord.x, char_cord.y)
    state = "STAY"
    while not 400 <= int(char_cord.x) <= 500 or not 900 <= int(char_cord.y) <= 1100:
        if state == "STAY":
            click(radar_btn)
            write_cords(start_farm_cords)
            state = "RUN"
        try:
            char_cord = get_char_cord()
            int(char_cord.x)
            int(char_cord.y)
        except ValueError:
            char_cord = Cords(1, 1)

def do_stuff():
    open_count = 1
    error_count = 0
    while 1:
        if not check_location():
            print(f"Мы не на Treasure Gulf! {get_location()}")
            move_to_treasure_gulf()
        get_scroll()
        cords_to_move = get_cords_from_scroll(open_count)
        print([f"{x.x}, {x.y}" for x in cords_to_move], open_count, error_count)
        for x in cords_to_move:
            click(radar_btn)
            write_cords(x)
            # wait_running()
            result = open_scroll()
            if result == True:
                break
        if result:
            error_count = 0
            open_count += 1
        else:
            error_count += 1
        if error_count >= 4:
            print("Похоже нужно продаться")
            go_to_npc(NPCS.elizabeth)
            error_count = 0
            input()





pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
do_stuff()
