import math
import pygame
import writer
import os
import numpy as np
from CONF import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)

GRAPH_SIZE_UPSCALED = math.floor(GRAPH_SIZE * SUPER_SAMPLE_DEPTH)
s = GRAPH_SIZE_UPSCALED * 2.5

exec_list = []
Graph_cols = [(0,50,100),(50,0,100),(100,50,0),(100,150,100)]

def get_advrege(item:list) -> float:
    return round(np.mean(item),2)

def get_point_on_vector(start:tuple,deg:float,distance:float):
    deg -= 90

    m = math.tan(deg * math.pi / 180)
    initial_pt = start
    terminal_pt = (start[0] + 1,start[1] + m) if not deg > 90 else (start[0] - 1, start[1] - m)

    v = np.array(initial_pt, dtype=float)
    u = np.array(terminal_pt, dtype=float)
    n = v - u
    n /= np.linalg.norm(n, 2)
    point = v - distance * n

    pt = list(point)
    return (int(pt[0]),int(pt[1]))

#--------------------Sprites--------------------#

class Graph_sector():
    def __init__(self,sides:int,sector:int,min_max:tuple,center:tuple,steps:int) -> None:
        self.sides = sides
        self.sector = sector
        self.steps = steps

        if min_max == []: self.min_max = [i for i in range(self.steps)]
        else: self.min_max = [(round(i,2)) for i in np.arange(min_max[0],min_max[1],min_max[2])]

        self.center = center

        self.font = pygame.font.Font(None,GRAPH_SIZE_UPSCALED // 20)

        #11 becauce i = 0 is gust (center,center),(center,center),(center,center)
        self.segments = [self.get_segment(i) for i in range(1,self.steps + 1)]
        self.text = [self.get_text(i) for i in range(self.steps)]
        

    def get_segment(self,segment):
        sector_size = 360 / self.sides
        segment_size = GRAPH_SIZE_UPSCALED / self.steps
        
        deg1 = sector_size * self.sector
        deg2 = sector_size * (self.sector + 1)
        size = segment_size * segment

        pts = []
        pts.append(get_point_on_vector(self.center,deg1,size))
        pts.append(get_point_on_vector(self.center,deg2,size))
        pts.append(self.center)

        return tuple(pts)
    
    def get_text(self,segment):
        text = str(self.min_max[segment])
        text_surf = self.font.render(text,True,(255,255,255))

        deg = (360 / self.sides) * (self.sector + 0.5)

        full_dist = (360/self.sides/2) * math.pi / 180
        full_dist = math.cos(full_dist) * GRAPH_SIZE_UPSCALED
    
        dist = (full_dist / self.steps) * (segment + 0.5)
        pt = get_point_on_vector(self.center,deg,dist)

        text_surf = pygame.transform.rotate(text_surf,-deg)
        text_rect = text_surf.get_rect(center = pt)

        return (text_surf,text_rect)
    
    def draw(self):
        for segment in range(len(self.segments)-1,-1,-1):
            max = 230
            c = math.floor((max / self.steps) * segment)
            col = (c,c,c)

            pygame.draw.polygon(graph_surf,col,self.segments[segment])
        
        #if self.sector != 0 : return None
        for text in range(len(self.text)-1,-1,-1):
            graph_surf.blit(self.text[text][0],self.text[text][1])

class Graph_title:
    def __init__(self,sides,sect,text,center) -> None:
        dist = (360/sides/2) * math.pi / 180
        dist = (math.cos(dist) * GRAPH_SIZE_UPSCALED) * 1.1

        deg = (360 / sides) * (sect + 0.5)
        pt = get_point_on_vector(center,deg,dist)

        font = pygame.font.Font(None,GRAPH_SIZE_UPSCALED // 10)
        self.text_surf = pygame.transform.rotate(font.render(text,True,(255,255,255)),-deg)
        self.text_rect = self.text_surf.get_rect(center = pt)
    
    def draw(self):
        graph_surf.blit(self.text_surf,self.text_rect)

class Graph_line():
    def __init__(self,ranges,values,sides,center,steps,col) -> None:
        self.points = [self.get_point(sect,values[sect],ranges[sect],center,sides,steps) for sect in range(sides)]
        self.col = col

    
    def get_point(self,sector,value,min_max,center,sides,steps):
        dist = (360/sides/2) * math.pi / 180
        dist = math.cos(dist) * GRAPH_SIZE_UPSCALED

        offset = min_max[0]
        val = value - offset
        diff = min_max[1] - min_max[0]

        dist = (val / diff * dist) + ((dist / steps) / 2)
        deg = (360 / sides) * (sector + 0.5)

        pt = get_point_on_vector(center,deg,dist)
        return pt
    
    def draw(self):
        pygame.draw.polygon(graph_surf,self.col,self.points,GRAPH_LINE_WIDTH)

class Graph_divider:
    def __init__(self,sides,center) -> None:
        self.center = center
        self.lines = [self.get_line(sect,sides) for sect in range(sides)]
    
    def get_line(self,sect,sides):
        deg = (360 / sides) * sect
        pt1 = self.center
        return get_point_on_vector(pt1,deg,GRAPH_SIZE_UPSCALED)
    
    def draw(self):
        [pygame.draw.aaline(graph_surf,(0,0,0),self.center,pt) for pt in self.lines]

class Graph():
    def __init__(self,sides:int,ranges:list,center:tuple,values:list,titles:list,steps:int) -> None:
        global graph_surf
        graph_surf = pygame.Surface((s,s),pygame.SRCALPHA)
        self.sectors = [Graph_sector(sides,sect,ranges[sect],center,steps) for sect in range(sides)]
        self.titles = [Graph_title(sides,sect,titles[sect],center) for sect in range(sides)]

        self.line = []
  
        [self.line.append(Graph_line(ranges,values[i],sides,center,steps,Graph_cols[i])) for i in range(len(values))]

        self.dividers = Graph_divider(sides,center)

    def draw(self):
        [sector.draw() for sector in self.sectors]
        [title.draw() for title in self.titles]
        self.dividers.draw()
        [i.draw() for i in self.line]

        obj = pygame.transform.smoothscale(graph_surf,(GRAPH_SIZE,GRAPH_SIZE))
        return obj

#------------------ Loadings ------------------#

def exec_save(item):
    global exec_list
    exec_list.append(item)
    
def load_graph(sides,ranges,vals,titles,steps) -> None:
    global graph

    graph = Graph(sides,ranges,(s // 2, s // 2),vals,titles,steps)
    return graph.draw()

def load_diff_vals() -> None:
    global exec_list
    headdings = ["ars","css","ods","lengths","bpms","stars"]

    vals = []

    for i in range(len(os.listdir("Locals"))):
        data = writer.read(f"Locals/p{i + 1}.json")
        vals.append([get_advrege(data[head]) for head in headdings])

    ranges = [(0,11,1),(0,11,1),(0,11,1),(0,198,18),(80,388,28),(5,10.5,0.5)]
    titles = ["AR","CS","OD","Length","BPM","Stars"]
    
    return load_graph(6,ranges,vals,titles,11)

def load_mod_vals() -> None:
    global exec_list
    headdings = ["fls","hts","ezs","hrs","dts","hds","nms"]

    vals = []
    for i in range(len(os.listdir("Locals"))):
        data = writer.read(f"Locals/p{i + 1}.json")
        vals.append([get_advrege(data[head]) * 100 for head in headdings])

    ranges = [(0,110,10) for i in range(7)]
    titles = ["Flashlight","Half Time","Easy","Hard Rock","Double Time","Hidden","No Mod"]
    
    return load_graph(7,ranges,vals,titles,11)



def load_mod_pps() -> None:
    global exec_list
    headdings = ["fl_pp","ht_pp","ts_pp","sd_pp","pf_pp","hd_pp","hr_pp","nm_pp","ez_pp","no_choke_pp","dt_pp"]

    vals = []
    for i in range(len(os.listdir("Locals"))):
        data = writer.read(f"Locals/p{i + 1}.json")
        vals.append([get_advrege(data[head]) for head in headdings])

    ranges = [(0,7513,683) for i in range(11)]

    titles = ["Flashlight","Half Time","Touch Screen","Sudden Death","Perfect","Hidden","Hard Rock","No Mod","Easy","No Choke","Doubble Time"]

    return load_graph(11,ranges,vals,titles,11)

def load_play_details() -> None:
    global exec_list
    
    titles = ["Accuracey","Combo","Misses","chokes","Preformance","Note Densatey","PP Densatey","Missed Combo"]

    vals = []

    for i in range(len(os.listdir("Locals"))):
        data = writer.read(f"Locals/p{i + 1}.json")
        va = []

        headings = ["accs","combos","misses","chokes","pps"]
        for head in headings: va.append(get_advrege(data[head]))

        #vals.append(get_advrege([int(i[i.find(" / ") + 3:-1]) - int(i[:i.find("x")]) for i in data["combos_full"]]))
        va.append(get_advrege( [ (data['acc1s'][i] + data["acc2s"][i] + data["acc3s"][i]) / data["lengths"][i] for i in range(len(data["lengths"]))] ) )
        va.append(get_advrege( [ data["pps"][i] / data["lengths"][i] for i in range(len(data["lengths"]))] ))
        va.append(get_advrege( [int(i[i.find(" / ") + 3:-1]) - int(i[:i.find("x")]) for i in data["combos_full"]] ))

        vals.append(va)
    
    ranges = [(90,101,1),(100,2190,190),(5,-0.5,-0.5),(5,-0.5,-0.5),(100,320,20),(0,5.5,0.5),(0,6.6,0.6),(51,0,-5)]

    return load_graph(8,ranges,vals,titles,11)

