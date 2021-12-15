import pygame, sys
from time import sleep

#GAME VARIABLES
box_size = 10
list_size = 100     # if changed: influences the number of squares in the Grid and the size of the screen
speed = 0.0125

# PYGAME VARIABLES
WIDTH, HEIGHT = list_size * 10, list_size * 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
rects = []
liste = []

pygame.display.set_caption("Game of Life")

# ------GAME ALGORITHM-------

#creates a 2d list with list_size number of rows and list_size number of columns filled with 0
def create_liste():
    liste = []
    for i in range(list_size):
        liste.append([0] * list_size)
    return liste

# takes a row and a column of liste as input and returns the number of living neighbours (1) this position has
def get_neighbours(i, j):
    n = 0
    if i > 0 and j > 0 and i < list_size - 1 and j < list_size - 1:
        if liste[i+1][j] == 1:
            n += 1
        if liste[i+1][j+1] == 1:
            n += 1
        if liste[i+1][j-1] == 1:
            n += 1
        if liste[i-1][j] == 1:
            n += 1
        if liste[i-1][j+1] == 1:
            n += 1
        if liste[i-1][j-1] == 1:
            n += 1
        if liste[i][j+1] == 1:
            n += 1
        if liste[i][j-1] == 1:
            n += 1
    return n

#applies the rules of game of life using the get_neighbours function (--> calling this funcitons once gives you only one round of the game)
def play():
    ne = []
    for i, row in enumerate(liste):
        for j, box in enumerate(row):
            ne.append(get_neighbours(i, j))

    for i, row in enumerate(liste):
        for j, num in enumerate(row):
            if num == 0 and ne[i * list_size + j] == 3:
                liste[i][j] = 1
            elif num == 1 and ne[i * list_size + j] < 2:
                liste[i][j] = 0
            elif num == 1 and ne[i * list_size + j] >= 4:
                liste[i][j] = 0



# ----- PYGAME METHODS ------

#checks if a certain rect (given as parameter) is already in rects
def clear(rect):
    for r in rects:
        if r.x == rect.x and r.y == rect.y:
            return False
    return True

#resets the rects list to an empty list
def clear_rects():
    for rect in rects:
        rects.remove(rect)

#sets every slot in liste to 1, if the associated rect exists in rects
def initialize():
    for rect in rects:
         liste[int(rect.y / box_size)][int(rect.x / box_size)] == 1

# updates rects if any changes happen in liste throughout the game
def show_game():
    for i, row in enumerate(liste):
        for j, num in enumerate(row):
            if liste[i][j] == 1:
                rect = pygame.Rect(j * box_size, i * box_size , box_size, box_size)
                if clear(rect):
                    rects.append(rect)
    for rect in rects:
        if liste[int(rect.y / box_size)][int(rect.x / box_size)] == 0:
            rects.remove(rect)

#draws the grid
def draw_lines():
    for i in range(0, list_size * 10, box_size):
        pygame.draw.line(screen, BLACK, (i, 0), (i, HEIGHT))
        pygame.draw.line(screen, BLACK, (0, i), (HEIGHT, i))

#draws the grid (->draw_lines) and displays the existing rects to the screen
def update_everything():
    screen.fill(WHITE)
    for rect in rects:
        pygame.draw.rect(screen, BLACK, rect)
    draw_lines()
    pygame.display.update()

pygame.init()


# -----MAIN GAME METHODS------

#in this state the player can click on any rect to convert it to a living cell, this information is stored in rects
#and if the player starts the game, pressing space, it is initialized to liste

def start():
    started = False
    global rects
    global liste
    rects = []
    liste = create_liste()
    while not started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    initialize()
                    started = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos1 = pos[0] - pos[0] % box_size
                pos2 = pos[1] - pos[1] % box_size
                rect = pygame.Rect(pos1, pos2, box_size, box_size)
                for i, row in enumerate(liste):
                    for j, box in enumerate(row):
                        if i == int(pos2 / box_size) and j == int(pos1 / box_size):
                            if clear(rect):
                                liste[i][j] = 1
                                rects.append(rect)
        update_everything()
    game()

#in this state the game is played until the player hits the s-key to stop and get back to the choosing-state
def game():
    game = True
    stopped = False
    while stopped == False:
        sleep(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    stopped = True
        play()
        show_game()
        update_everything()

    start()

#START
start()
