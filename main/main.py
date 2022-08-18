import math
import writer
import pygame
import random
import plotter
from CONF import *
import Working_Scraper

display_note = False
displaying_graph = False

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

current_title = 0
GRAPH_TITLES = ["Mod Choices","Play Details","Level Details","Mod Preformances"]

def next_title(inc):
    global current_title

    current_title += inc
    if current_title < 0:
        current_title = len(GRAPH_TITLES) - 1
        return None

    if current_title > len(GRAPH_TITLES) - 1:
        current_title = 0

def get_background_tile(x,y,s) -> None:
    img = pygame.Surface((s,s))
    c = random.randint(50,75)

    img.fill((c,c,c))
    rect = img.get_rect(topleft = (x * s, y * s))
    BACKGROUND_SURF.blit(img,rect)

def get_background():
    global BACKGROUND_SURF
    BACKGROUND_SURF = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
    BACKGROUND_SURF.fill((0,0,0))

    n = 25
    while min(SCREEN_HEIGHT,SCREEN_WIDTH) % n != 0:
        n -= 1

    s = min(SCREEN_HEIGHT,SCREEN_WIDTH) // n

    #n is used because the proformance diffrance with
    #only useing n for the larger value and some outher number is negligable
    for y in range(n + 1):
        for x in range(n + 1):
            get_background_tile(x,y,s)

get_background()

class title_bar(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.set_text("Main Menu")

    def update_text(self) -> None:
        self.image = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT // 15), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))

        fnt = pygame.font.Font(None,SCREEN_WIDTH // 10)
        fnt_surf = fnt.render(self.text,True,(150,200,250))
        c = ((SCREEN_WIDTH // 2 - (fnt_surf.get_width() // 2),SCREEN_HEIGHT // 30 - (fnt_surf.get_height() // 2)))

        self.image.blit(fnt_surf,c)
        self.rect = self.image.get_rect(midbottom = (SCREEN_WIDTH // 2,SCREEN_HEIGHT // 10))
    
    def set_text(self,text):
        self.text = text
        self.update_text()

Title_bar = pygame.sprite.GroupSingle()
Title_bar.add(title_bar())

def Load_Player():
    global getting_input
    getting_input = True

def Exit():
    pygame.quit()
    exit()

def Compare_Players():
    global getting_input
    getting_input = True

class menu_item(pygame.sprite.Sprite):
    def __init__(self,text,inx) -> None:
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(None,SCREEN_WIDTH // 20)
        self.text_surf = self.font.render(text,True,(255,255,255))
        
        self.image = pygame.Surface((self.text_surf.get_width() + SCREEN_WIDTH // 30,(self.text_surf.get_height() + SCREEN_HEIGHT // 30)), pygame.SRCALPHA)
        self.c = (self.image.get_width() // 2 - (self.text_surf.get_width() // 2), self.image.get_height() // 2- (self.text_surf.get_height() // 2))
        self.image.blit(self.text_surf,self.c)
        self.rect = self.image.get_rect(midtop = (SCREEN_WIDTH // 2,(SCREEN_HEIGHT // 10) + self.image.get_height() * inx))
    
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill((0,0,0,255))
            self.image.blit(self.text_surf,self.c)
        else:
            self.image.fill((0,0,0,0))
            self.image.blit(self.text_surf,self.c)
    
    def click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            exec(self.text.replace(" ","_") + "()")

menu = [menu_item("Load Player",1),menu_item("Compare Players",2),menu_item("Exit",3)]
Menu_group = pygame.sprite.Group()
Menu_group.add(menu)

class Input_box(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.load_vals = []
        self.getting_play_count = False
        self.play_count = 0
        self.text = []
        self.image = pygame.surface.Surface((math.floor(SCREEN_WIDTH * 0.9),SCREEN_HEIGHT // 20))
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    def add_letter(self,char):
        if char == chr(pygame.K_RETURN):
            if self.getting_play_count:
                self.load_vals.append(int("".join(self.text)))
                self.load()
                self.getting_play_count = False
            else:
                self.load_vals.append("".join(self.text).split("/"))
                self.getting_play_count = True
                self.text = []
                self.update()
                return None

        if char == "\x08":
            if len(self.text) != 0:
                self.text.pop()
            else:
                return None
        else: self.text.append(char)

        self.update()
    
    def update(self):
        self.image = pygame.surface.Surface((math.floor(SCREEN_WIDTH * 0.9),SCREEN_HEIGHT // 20))
        self.fnt = pygame.font.Font(None,SCREEN_HEIGHT // 21)
        self.txt_surf = self.fnt.render("".join(self.text),True,(255,255,255))
        self.txt_rect = self.txt_surf.get_rect(center = self.rect.center)

        self.image.blit(self.txt_surf,(self.rect.width // 2 - self.txt_rect.width // 2, self.rect.height // 2 - self.txt_rect.height // 2))
    
    def load(self):
        global getting_input,displaying_graph
        writer.reset()

        i = 1
        for player in self.load_vals[0][::-1]:
            Working_Scraper.load(player,self.load_vals[1],i)
            i += 1
        
        getting_input = False
        self.update()
        gen_key(self.load_vals[0])
        displaying_graph = True
        load_graph()

input_box = Input_box()
user_input = pygame.sprite.GroupSingle(input_box)

class key_item():
    def __init__(self,text,col,pos) -> None:
        s = min(SCREEN_HEIGHT,SCREEN_WIDTH)
        self.colour_square = pygame.Surface((s // 40,s // 40),)
        self.colour_square.fill(col)

        self.fnt = pygame.font.Font(None,s // 40)
        self.txt_surf = self.fnt.render(text,True,col)
        self.txt_pos = (s // 40,s // 40 - math.floor(self.txt_surf.get_height() * 1.25))

        self.txt_pos = (self.txt_pos[0] + pos[0] + s // 80,self.txt_pos[1] + pos[1])
        self.pos = pos

    def draw(self):
        screen.blit(self.colour_square,self.pos)
        screen.blit(self.txt_surf,self.txt_pos)

def gen_key(names):
    global key
    out = []
    loop_count = (len(names) // 3) + 1
    step_size = 255 // loop_count
    
    for itt in range(loop_count):
        for i in range(3):
            col = [step_size * itt + 1 for i in range(3)]
            col[i] = 255
            out.append(col)
    
    plotter.Graph_cols = out
    key = [key_item(names[i],out[i],(100,100 + (i * min(SCREEN_HEIGHT,SCREEN_WIDTH) // 35))) for i in range(len(names))]

def load_graph():
    global obj_rect
    Title_bar.sprites()[0].set_text(GRAPH_TITLES[current_title])     

    exec("global obj\nobj = " + graphs_loaders[current_title] + ")")   
    obj_rect = obj.get_rect(center = (SCREEN_WIDTH // 2,SCREEN_HEIGHT // 2))

graphs_loaders = [
"plotter.load_mod_vals(",
"plotter.load_play_details(",
"plotter.load_diff_vals(",
"plotter.load_mod_pps("
]

obj = None
getting_input = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            
            if event.key == pygame.K_RIGHT:
                next_title(1)
                load_graph()
            
            if event.key == pygame.K_LEFT:
                next_title(-1)
                load_graph()

        
            if getting_input:
                input_box.add_letter(chr(event.key))

        if event.type == pygame.MOUSEBUTTONUP:
            for i in menu:
                i.click()

    #update
    for i in menu:
        i.update()

    #Render
    screen.blit(BACKGROUND_SURF,(0,0))
    Title_bar.draw(screen)
    if not displaying_graph:
        Menu_group.draw(screen)
    if getting_input:
        user_input.draw(screen)
    if obj != None:
        screen.blit(obj,obj_rect)
    if displaying_graph:
        [i.draw() for i in key]


    #Update
    pygame.display.update()
    clock.tick(FPS)