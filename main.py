import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 5
CELL_SIZE = WIDTH // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Икосиан")

font = pygame.font.SysFont('comicsans', 36)

GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()



class Vertice:
    def __init__(self, xy, radius, color, image):
        self.xy = xy
        self.x = xy[0]
        self.y = xy[1]
        self.radius = radius
        self.color = color
        self.image = image
    def draw(self):
        pygame.draw.circle(screen, self.color, self.xy,self.radius)
    def draw_city(self):
        screen.blit( self.image, (self.x-25, self.y-25))
    def draw_text(self, button_text):
        text_surface = font.render(button_text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.xy)
        screen.blit(text_surface, text_rect)
    def cord_x(self):
        return self.xy[0]
    def cord_y(self):
        return self.xy[1]
    def cords(self):
        return self.xy
    def clicked(self):
        print(self.xy, " i was clicked")


city_list = [pygame.image.load(f'cities/city{i}.png') for i in range(20)]

verts_0 = [(300.0,50.0), (78.0, 190.0),(150.0, 400.0),(450.0, 400.0),(512.0, 190.0)]
verts_1 = [(300.0,150.0), (235.0,185.0), (188.0, 220.0), (215.0,285.0), (250.0, 350.0), (300.0, 350.0), (350.0, 350.0),  (385.0, 285.0),(412.0, 220.0), (365.0,185.0)]
verts_2 = [(300.0, 300.0), (260.0, 275.0), (270.0, 225.0), (330.0, 225.0),  (340.0, 275.0)]

indx_0 = [i for i in range(0,5)]
indx_1 = [i for i in range(5,15)]
indx_2 = [i for i in range(15,20)]

bridges_indx = [(0,5), (1, 7),  (2,9),(3, 11), (4, 13), (6, 17), (8, 16), (10, 15), (12, 19), (14, 18)]


verts__ = verts_0 + verts_1 + verts_2
#print((verts__))

all_verts = dict(enumerate([Vertice(verts__[x], 10, BLUE, city_list[x]) for x in range(len(verts__))]))
#test_subject = Vertice((500.0, 500.0), 10, BLUE, city_1)
#
# def draw_button(x, y, width, height, text):
#     """Функция для рисования кнопки с текстом на экран."""
#     # Рисуем кнопку
#     button_rect = pygame.Rect(x, y, width, height)
#     pygame.draw.rect(screen, BLUE, button_rect)


def draw_bridge(player_bridges):
    if len(player_bridges) >= 2:
        for i in range(0, len(player_bridges), 2):
            pygame.draw.line(screen, GREEN, all_verts[player_bridges[i]].cords(), all_verts[player_bridges[i+1]].cords(), 5)

def draw_verts():
    for i in all_verts:
        all_verts[i].draw()
        all_verts[i].draw_city()
        #all_verts[i].draw_text(str(i))

def draw_indx(indx):
    for i in range(indx[0], indx[len(indx)-1]):
        pygame.draw.line(screen, GREY, all_verts[i].cords(), all_verts[i + 1].cords(),3)
    pygame.draw.line(screen, GREY, all_verts[indx[0]].cords(), all_verts[indx[len(indx)-1]].cords(), 3)

def draw_board():
    draw_indx(indx_0)
    draw_indx(indx_1)
    draw_indx(indx_2)
    for i in range(0, len(bridges_indx)-1):
        pygame.draw.line(screen, GREY, all_verts[bridges_indx[i][0]].cords(), all_verts[bridges_indx[i][1]].cords(),3)


# def draw_board():
#     for x in verts_0:
#         Vertice(x, 10 , BLUE).draw()
#     for x in verts_1:
#         Vertice(x, 10, BLUE).draw()
#     for x in verts_2:
#         Vertice(x, 10, BLUE).draw()
#     for x in verts_3:
#         Vertice(x, 10, BLUE).draw()

def check_vert(mouse_x, mouse_y):
    #print('Clicked!')
    for i in all_verts:
        #(mouse_x, mouse_y) == all_verts[i].cords()
        if (all_verts[i].cord_x() + all_verts[i].radius >= mouse_x >= all_verts[i].cord_x() - all_verts[i].radius) and (
                all_verts[i].cord_y() + all_verts[i].radius >= mouse_y >= all_verts[i].cord_y() - all_verts[i].radius):
            all_verts[i].clicked()
            return True, i
    return False, None

def is_citizens(buffer, indx_0, indx_1, indx_2):
    if buffer[0] in indx_0 and buffer[1] in indx_0:
        return True, indx_0
    elif buffer[0] in indx_1 and buffer[1] in indx_1:
        return True, indx_1
    elif buffer[0] in indx_2 and buffer[1] in indx_2:
        return True, indx_2
    else:
        return False, None

def is_neighbors(ix, iy, country):
    if ((min(ix, iy) == country[0]) and (max(ix, iy) == country[len(country)-1])) or min(ix, iy) + 1 == max(ix, iy):
        return True
    return False

def check_winner():
    return None

def main():
    board_bridges = []
    player_bridges = []
    buffer = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                try:
                    hit, index = check_vert(mouse_x, mouse_y)
                except TypeError:
                    print("Click again")
                if hit:
                    buffer.append(index)
                    if len(buffer) == 2:
                        if not (min(buffer[0], buffer[1]),max(buffer[0], buffer[1])) in bridges_indx:
                            check_same_country, country = is_citizens(buffer, indx_0, indx_1, indx_2)
                            if check_same_country:
                                if player_bridges.count(buffer[0]) >= 2 or player_bridges.count(buffer[1]) >= 2 or buffer[0] == buffer[1] or not is_neighbors(buffer[0], buffer[1], country):
                                    #print(is_neighbors(buffer[0], buffer[1], country))
                                    buffer.clear()
                                else:
                                    player_bridges += buffer
                                    #print(is_neighbors(buffer[0], buffer[1], country))
                                    buffer.clear()
                            else:
                                #print(buffer[0], buffer[1], indx_0)
                                buffer.clear()
                        else:
                            player_bridges += buffer
                            buffer.clear()



        screen.fill(WHITE)
#        test_subject.draw_city()
        draw_board()
        draw_bridge(player_bridges)
        draw_verts()
        pygame.display.update()
        clock.tick(15)


if __name__ == "__main__":
    main()
