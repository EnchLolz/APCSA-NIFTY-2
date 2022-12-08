#imports
import pygame
import random

#user settings
FPS = 60
horizontal = 4
vertical = 4
win_score = 11

#initializes pygame
pygame.init()

#game settings and constants
play = True
width = horizontal * 120+20
height = vertical * 120+70
score = 0
time_ticks = 0
spawn_percent = 0.8
bg_color = "wheat1"
grid_color = "wheat3"
light_colors = ["coral1","orange2","gold2","seagreen2","darkslategray2","royalblue1","palevioletred2","darkorchid1"]
medium_colors = ["brown2","chocolate2","goldenrod2","springgreen3","cyan3","dodgerblue3","deeppink","mediumorchid4"]
dark_colors = ["red2","darkorange3","darkgoldenrod3","forestgreen","cyan4","navy","#E0115F","purple4"]
tile_colors = light_colors+medium_colors+dark_colors
grid = [[None for i in range(horizontal)] for j in range(vertical)]
free_tiles = {(i%horizontal,i//horizontal)for i in range(horizontal*vertical)}

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(str(1<<win_score))
screen.fill(bg_color)

#moving tile class
class tile:
    #initializes tile
    def __init__(self,val,x,y):
        self.value = val
        self.xpos = x
        self.ypos = y
        self.color = tile_colors[(val-1)%len(tile_colors)]
    #processes tile-tile merging
    def merge(self,other):
        global score
        if other == None:
            return "empty"
        elif other.value == self.value:
            score += 2<<self.value
            other.value += 1
            other.color = tile_colors[(other.value-1)%len(tile_colors)]
            grid[self.ypos][self.xpos] = None
            free_tiles.add((self.xpos,self.ypos))
            del self
            return "merged"
        else:
            return "blocked"

#spawn new tile
def spawn():
    if len(free_tiles) > 0:
        x,y = random.sample(free_tiles,1)[0]
        free_tiles.remove((x,y))
        grid[y][x] = tile(1 if random.random() < spawn_percent else 2,x,y)

#moves tiles
def move(direction):
    global score
    moved = False
    #moving tile at position i j
    def replace(i,j):
        global score
        moved = False
        x,y=0,0
        #moving directions
        if direction == "left": y=0;x=-1
        if direction == "right": y=0;x=1
        if direction == "up": y=-1;x=0
        if direction == "down": y=1;x=0
        #moving tile
        if grid[i][j] != None:
            while(i+y>=0 and i+y<vertical and j+x>=0 and j+x<horizontal):
                merge = grid[i][j].merge(grid[i+y][j+x])
                if merge == "empty":
                    moved = True
                    grid[i+y][j+x] = grid[i][j]
                    grid[i+y][j+x].xpos = j+x
                    grid[i+y][j+x].ypos = i+y
                    grid[i][j] = None
                    free_tiles.add((j,i))
                    free_tiles.remove((j+x,i+y))
                    i+=y
                    j+=x
                elif merge == "merged":
                    moved = True
                    break
                else:
                    break
        return moved
    #move tiles based on direction
    if direction == "left":
        for i in range(vertical):
            for j in range(1,horizontal):
                moved |= replace(i,j)
    if direction == "right":
        for i in range(vertical):
            for j in range(horizontal-2,-1,-1):
                moved |= replace(i,j)
    if direction == "up":
        for i in range(horizontal):
            for j in range(1,vertical):
                moved |= replace(j,i)
    if direction == "down":
        for i in range(horizontal):
            for j in range(vertical-2,-1,-1):
                moved |= replace(j,i)
    #spawn new tile if tiles moved
    if moved:
        spawn()

#draws tiles on the grid
def drawtiles():
    for i in range(vertical):
        for j in range(horizontal):
            if grid[i][j] != None:
                pygame.draw.rect(screen, grid[i][j].color, (j*120+20, i*120+70, 100, 100))
                font = pygame.font.SysFont("comicsansms",36)
                if(1<<grid[i][j].value >= 10000):
                    font = pygame.font.SysFont("comicsansms",52-int(grid[i][j].value*0.3)*4)
                text = font.render(str(1<<grid[i][j].value), True, "white")
                screen.blit(text, (j*120+20+50 - text.get_width() / 2, i*120+70+50 - text.get_height() / 2))

#draws grid lines
def drawgrid():
    screen.fill(bg_color)
    for i in range(horizontal+1):
        pygame.draw.rect(screen, grid_color, (i*120, 0, 20, height))
    for i in range(vertical+1):
        pygame.draw.rect(screen, grid_color, (0, 50+i*120, width, 20))

#draws score and time
def drawheader():
    pygame.draw.rect(screen, "wheat4", (0, 0, width, 50))
    font = pygame.font.SysFont("comicsansms",36)
    text = font.render(str(1<<win_score), True, "white")
    screen.blit(text, (width / 2 - text.get_width() / 2, 0))
    font = pygame.font.SysFont("comicsansms",24)
    text = font.render("Score: " + str(score), True, "white")
    screen.blit(text, (10, 10))
    text = font.render("Time: " + str(time_ticks//FPS), True, "white")
    screen.blit(text, (width - text.get_width() - 10, 10))

#checks if game is over
def gameend():
    win = False
    lose = True
    for i in range(vertical):
        for j in range(horizontal):
            if grid[i][j] != None and grid[i][j].value >= win_score:
                win = True
            if grid[i][j] == None:
                lose = False
            elif j < horizontal-1 and (grid[i][j+1] == None or grid[i][j].value == grid[i][j+1].value):
                lose = False
            elif i < vertical-1 and (grid[i+1][j] == None or grid[i][j].value == grid[i+1][j].value):
                lose = False
    if win:
        return "win"
    elif lose:
        return "lose"
    return "continue"

#lose screen
def lose():
    while(True):
        drawgrid()
        drawheader()
        drawtiles()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        s = pygame.Surface((width,height-50))
        s.set_alpha(200)
        s.fill((0,0,0))
        screen.blit(s, (0,50))
        font = pygame.font.SysFont("comicsansms",72)
        text = font.render("You Lose", True, "white")
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        font = pygame.font.SysFont("comicsansms",24)
        text = font.render("(press space to continue)", True, "white")
        screen.blit(text, (width / 2 - text.get_width() / 2, height * 3 / 4 - text.get_height() / 2))
        pygame.display.flip()
        clock.tick(FPS)

#win screen
def win():
    while(True):
        drawgrid()
        drawheader()
        drawtiles()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        s = pygame.Surface((width,height-50))
        s.set_alpha(200)
        s.fill((0,0,0))
        screen.blit(s, (0,50))
        font = pygame.font.SysFont("comicsansms",72)
        text = font.render("You Win", True, "white")
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        font = pygame.font.SysFont("comicsansms",24)
        text = font.render("(press space to continue)", True, "white")
        screen.blit(text, (width / 2 - text.get_width() / 2, height * 3 / 4 - text.get_height() / 2))
        pygame.display.flip()
        clock.tick(FPS)

#main game loop
def game():
    global time_ticks, score, play
    spawn()
    spawn()
    #game loop
    while play:
        drawgrid()
        drawheader()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move("left")
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move("right")   
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move("up")
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move("down")
        drawtiles()
        time_ticks+=1
        pygame.display.flip()
        clock.tick(FPS)
        ended = gameend()
        if ended == "win":
            play = False
            win()
        elif ended == "lose":
            play = False
            lose()
    home()

#home screen
def home():
    global play, time_ticks, score, grid, free_tiles
    time_ticks = 0
    score = 0
    grid = [[None for i in range(horizontal)] for j in range(vertical)]
    free_tiles = {(i%horizontal,i//horizontal)for i in range(horizontal*vertical)}
    while(True):
        drawgrid()
        drawheader()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play = True
                    game()
        s = pygame.Surface((width,height-50))
        s.set_alpha(200)
        s.fill((0,0,0))
        screen.blit(s, (0,50))
        font = pygame.font.SysFont("comicsansms",72)
        text = font.render(str(1<<win_score), True, "white")
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        font = pygame.font.SysFont("comicsansms",24)
        text = font.render("(press space to continue)", True, "white")
        screen.blit(text, (width / 2 - text.get_width() / 2, height * 3 / 4 - text.get_height() / 2))
        pygame.display.flip()
        clock.tick(FPS)

#game starts here
home()    

#~Nathan Ye