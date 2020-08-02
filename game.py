import usemodel
import neuralnetwork
import random
import pygame
import tkinter as tk
from tkinter import messagebox

#CHANGE ME
numOfSnakes = 40
train_network = False

class cube(object):
    rows = 10
    w = 600

    def __init__(self, start, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    def __init__(self, color, pos, id1):
        self.body = []
        self.turns = {}
        self.snack = None
        self.color = color
        self.head = cube(pos, color = self.color) #Individual color :)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        #Added some variables to help keep track of certain data
        self.first3 = 0
        self.alive = True
        self.id = id1
        self.length = 0
        self.hunger = 0
        self.direction = "UP"

    def isAlive(self):
        return self.alive
    def isFirst3(self):
        return self.first3<3
    def changeAlive(self):
        self.alive = False
    def addFirst3(self):
        self.first3+=1

    def randomSnack(self, rows):
        while True:
            x = random.randrange(1, rows - 1)
            y = random.randrange(1, rows - 1)
            if len(list(filter(lambda z: z.pos == (x, y), self.body))) > 0:
                continue
            else:
                break
        self.snack = cube((x,y), color=self.color)
    def insertSnack(self, snack):
        self.snack = snack
    def move(self, direction):
        if self.alive:
            if direction == "LEFT":
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.direction = "LEFT"

            elif direction == "RIGHT":
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.direction = "RIGHT"

            elif direction == "UP":
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.direction = "UP"

            elif direction == "DOWN":
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                self.direction = "DOWN"

            for i, c in enumerate(self.body):
                p = c.pos[:]
                if p in self.turns:
                    turn = self.turns[p]
                    c.move(turn[0], turn[1])
                    if i == len(self.body) - 1:
                        self.turns.pop(p)
                else:
                    if c.dirnx == -1 and c.pos[0] <= 0:
                        c.pos = (c.rows - 1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                        c.pos = (0, c.pos[1])
                    elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                        c.pos = (c.pos[0], 0)
                    elif c.dirny == -1 and c.pos[1] <= 0:
                        c.pos = (c.pos[0], c.rows - 1)
                    else:
                        c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos, color=self.color)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.alive = True
        self.length = 0
        self.hunger = 0
        self.first3 = 0
        self.snack = None
        self.direction = "UP"

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1]), self.color))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1]), self.color))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1), self.color))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1), self.color))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface, snakes):
    global rows, width
    surface.fill((0, 0, 0))
    for s in snakes:
        s.draw(surface)
        s.snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def globalRandomSnack(rows, snakes):  # snakes should just be the singular snake
    positions = []
    for s in snakes:
        positions.extend(s.body)
    while True:
        x = random.randrange(1, rows - 1)
        y = random.randrange(1, rows - 1)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

def generateSnake(num, loc):
    return snake((random.randint(0,255), random.randint(0,255), random.randint(0,255)), loc, num)

def main():
    global width, rows, snack
    width = 600
    rows = 10
    win = pygame.display.set_mode((width, width))
    randloc = (random.randint(2, rows - 2), random.randint(2, rows - 2)) #Generates a psuedo random spawn that isn't on the edge
    if train_network:
        snakes = [generateSnake(x, randloc) for x in range(numOfSnakes)] #Generates x snakes with the same spawn
    else:
        snakes = [generateSnake(0, randloc)]
    snack = cube(globalRandomSnack(rows, snakes), color=(0, 255, 0)) #Generates a globalized food location to start
    for s in snakes:
        s.insertSnack(snack) #injects the food location to each snake

    clock = pygame.time.Clock()

    while True:
        #pygame.time.delay(50)
        clock.tick(120)
        #Check to see if any snake is alive, if not, train network and restart game
        quit = True
        for s in snakes:
            if s.isAlive():
                quit = False
        if quit:
            if train_network:
                neuralnetwork.gameIsOver(snakes)
            randloc = (random.randint(2, rows - 2), random.randint(2, rows - 2))
            for s in snakes:
                s.reset(randloc)
                snack = cube(globalRandomSnack(rows, snakes), color=(0, 255, 0))
                for s in snakes:
                    s.insertSnack(snack)
        #Control each snake
        for s in snakes:
            if s.isAlive() == True:
                s.hunger+=1
                if train_network:
                    s.move(neuralnetwork.selectMove(s.head.pos, s.body, s.snack.pos, rows, s.id, s.direction))
                else:
                    s.move(usemodel.selectMove(s.head.pos, s.body, s.snack.pos, rows, s.id, s.direction))
                if s.isFirst3():
                    s.addCube()
                    s.addFirst3()
                if s.head.pos[0] == 0 or s.head.pos[0] == rows-1 or s.head.pos[1] == 0 or s.head.pos[1] == rows-1 or s.hunger>29:
                    s.changeAlive()
                    s.length = len(s.body)
                    s.body = [s.body[0]]
                if s.body[0].pos == s.snack.pos:
                    s.addCube()
                    s.randomSnack(rows)
                    s.hunger = 0
                for x in range(len(s.body)):
                    if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                        s.changeAlive()
                        s.length = len(s.body)
                        s.body = [s.body[0]]
                        break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        #message_box('', 'Next Turn') #Uncomment this if you want to control pace of turns
        redrawWindow(win, snakes)
main()