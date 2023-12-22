from typing import List


class Cords:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"{self.x}, {self.y}"
    
    def __eq__(self, __value: object) -> bool:
        return ((self.x, self.y) == (__value.x, __value.y))


class Button:
    def __init__(self, cords:Cords, cords_check:Cords=None, check_color:(int, int, int)=None, reverse:bool=False):
        self.cords = cords
        self.cords_check = cords_check
        self.check_color = check_color
        self.reverse=reverse

class NPC:
    def __init__(self, position:List[Cords], screen_cords:Cords, check_cords:Cords, check_color:(int, int, int)) -> None:
        self.position = position
        self.screen_cords = screen_cords
        self.check_cords = check_cords
        self.check_color = check_color

radar_btn = Button(cords=Cords(1182, 1339), cords_check=Cords(526, 222), check_color=(235, 235, 235))
radar_confirm_btn = Button(cords=Cords(480, 300), cords_check=Cords(526, 222), check_color=(235, 235, 235), reverse=True)
radar_input_x = Cords(420, 275)
radar_input_y = Cords(500, 275)

inventory_btn = Button(cords=Cords(2354, 1420), cords_check=Cords(662, 122), check_color=(235, 235, 235))

scroll_position = Cords(400, 244)
scroll_color = (107, 24, 41)
scroll_cords_pos1 = Cords(524, 285)
scroll_cords_pos2 = Cords(scroll_cords_pos1.x+48, scroll_cords_pos1.y+11)

scroll_cords_pos1_only_y = Cords(548, 285)
scroll_cords_pos2_only_y = Cords(scroll_cords_pos1.x+48, scroll_cords_pos1.y+11)

purple_pirate_scroll_position = Cords(379,244)
purple_pirate_scroll_color = (221, 170, 255)

location_name_pos1 = Cords(2408, 12)
location_name_pos2 = Cords(location_name_pos1.x + 130, location_name_pos1.y + 15)

old_ticket = Cords(1430, 1372)

death_indicator = Cords(803, 609)
revive_confirm_btn = Button(cords=Cords(721, 670), cords_check=death_indicator, check_color=(235, 235, 235), reverse=True)

sitdown_btn = Cords(2514, 1371)

health_pot = Cords(1056, 1372)

start_farm_cords = Cords(450, 1000)

char_cord1 = Cords(2440, 188)
char_cord2 = Cords(char_cord1.x + 70, char_cord1.y + 13)

center = Cords(1280, 704)



class NPCS:
    harbor_operator_mark = NPC([Cords(820, 3708), Cords(822, 3699)], Cords(1265, 581), Cords(1462, 1145), (235, 235, 235))
    elizabeth = NPC([Cords(623, 948), Cords(617, 963)], Cords(1265, 581), Cords(1462, 1145), (235, 235, 235))


class Navigation:
    from_shai_to_treasure_island_portal = [Cords(1718,620), Cords(1890,1323), Cords(2127,1087), Cords(1958,801), Cords(1702,758)]
    from_treasure_island_portal_to_treasure_island_harbor = [Cords(456,1200), Cords(818,430), Cords(778,220), Cords(1070,346), Cords(114,920), Cords(431,191), Cords(1044,449), Cords(417,1041), Cords(416,761)]