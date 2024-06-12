#Librerias
import random
import sys
import pygame
import os
from pygame.locals import (K_UP,K_DOWN,K_LEFT,K_RIGHT,K_SPACE,K_RETURN,K_1,K_KP1,K_2,K_KP2,K_3,K_KP3,K_F1,K_ESCAPE,KEYDOWN)


#Iniciacion
medidax=1300
mediday=650
pygame.init()
screen=pygame.display.set_mode((medidax,mediday))#,pygame.FULLSCREEN)
pygame.display.set_caption("Coronavirus the game")
clock=pygame.time.Clock()
fps=60

#Imagenes
path = os.path.realpath(os.path.dirname(__file__))

def load_image(name, res):
    image = pygame.image.load(path+"/images"+name)
    return pygame.transform.scale(image,res)

virus=load_image("/virus.png",(100,100))

mutante=load_image("/mutante.png",(95,95))

leucocito=load_image("/leucocito.png",(90,90))

leucocitoalpha=load_image("/leucocitoalpha.png",(90,90))

fondo=pygame.image.load(path+"/images/fondo.png").convert()
fondo=pygame.transform.scale(fondo,(1350,1000))

pantallainicio=load_image("/pantallainicio.png", (1350,800))

controles=load_image("/controles.png",(1350,800))

dificultades=load_image("/dificultades.png", (900,550))

gameover=load_image("/gameover.png",(1000,600))

#Musica
pygame.mixer.music.load(path+"/sounds/temaprincipal.ogg")
pygame.mixer.music.play(-1)

#Caracteristicas enemigo
class enemigo:
    def __init__(self):
        self.tipoenemigo="verde"
        self.posx=random.randint(500,medidax-88)
        self.posy=random.randint(16,mediday-95)
        self.actualizar()
        self.deltax=random.choice([-3,-2.5,-2,2,2.5,3])
        self.deltay=random.choice([-3,-2.5,-2,2,2.5,3])
    def actualizar(self):
        self.xmin=self.posx+25
        self.xmax=self.posx+75
        self.ymin=self.posy+25
        self.ymax=self.posy+80
    def avanzar(self):
        if self.posx+self.deltax+88>medidax or self.posx+self.deltax+10<0:
            if self.deltax<0:
                self.deltax=random.choice([2,2.5,3])
                if self.tipoenemigo=="rojo":
                    self.deltax*=2
            else:
                self.deltax=random.choice([-2,-2.5,-3])
                if self.tipoenemigo=="rojo":
                    self.deltax*=2
        if self.posy+self.deltay+95>mediday or self.posy+self.deltay+12<0:
            if self.deltay<0:
                self.deltay=random.choice([2,2.5,3])
                if self.tipoenemigo=="rojo":
                    self.deltay*=2
            else:
                self.deltay=random.choice([-2,-2.5,-3])
                if self.tipoenemigo=="rojo":
                    self.deltay*=2
        self.posx+=self.deltax
        self.posy+=self.deltay
        self.actualizar()
        self.pintar()
    def pintar(self):
        if self.tipoenemigo=="verde":
            screen.blit(virus,(self.posx,self.posy))
        else:
            screen.blit(mutante,(self.posx,self.posy))

#Caracteristicas jugador
class jugador:
    def __init__(self):
        self.posx=0
        self.posy=550
        self.delta=5
        self.poderinmune=1
        self.inmune=False
        self.actualizar()
    def actualizar(self):
        self.xmin=self.posx+18
        self.xmax=self.posx+75
        self.ymin=self.posy+18
        self.ymax=self.posy+70
    def hacerinmune(self):
        if self.poderinmune>0:
            self.inmune=True
    def noinmune(self):
        self.inmune=False
    def derecha(self):
        if self.posx+self.delta+86<medidax:
            self.posx+=self.delta
            self.actualizar()
    def izquierda(self):
        if self.posx-self.delta+2>0:
            self.posx-=self.delta
            self.actualizar()
    def arriba(self):
        if self.posy-self.delta+4>0:
            self.posy-=self.delta
            self.actualizar()
    def abajo(self):
        if self.posy+self.delta+86<mediday:
            self.posy+=self.delta
            self.actualizar()
    def pintar(self):
        screen.blit(leucocito,(self.posx,self.posy))
    def pintarinmune(self):
        screen.blit(leucocitoalpha,(self.posx,self.posy))

#Chequea eventos
def chequeareventos():
    for event in pygame.event.get():
        if event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key==K_SPACE:
                player.hacerinmune()
    tecla=pygame.key.get_pressed()
    if tecla[K_RIGHT]:
        player.derecha()
    if tecla[K_LEFT]:
        player.izquierda()
    if tecla[K_UP]:
        player.arriba()
    if tecla[K_DOWN]:
        player.abajo()

#Chequea colision
def colision(i):
    if player.xmin>listavirus[i].xmax:
        return False
    if listavirus[i].xmin>player.xmax:
        return False
    if player.ymin>listavirus[i].ymax:
        return False
    if listavirus[i].ymin>player.ymax:
        return False
    return True

#Comienza cada bucle
def actualizarpantalla():
    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)
    screen.blit(fondo,(0,0))

#Cuenta bucles
def cuentabucles(contador):
    if contador%200==0:
        for i in range(numvirus):
            if listavirus[len(listavirus)-i-1].tipoenemigo=="verde":
                listavirus[len(listavirus)-i-1].tipoenemigo="rojo"
                return

#Bucle inicio
esperar=True
ensenarcontroles=False
while esperar:
    actualizarpantalla()
    screen.blit(pantallainicio,(-25,-100))
    for event in pygame.event.get():
        if event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key==K_F1:
                ensenarcontroles=True
                esperar=False
            if event.key==K_RETURN:
                esperar=False

#Bucle para ensenar controles
while ensenarcontroles:
    actualizarpantalla()
    screen.blit(controles,(-25,-100))
    for event in pygame.event.get():
        if event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                pygame.quit()
                sys.exit()
            else:
                ensenarcontroles=False

#Bucle que se repite siempre
while True:
    #Bucle dificultad
    escojerdificultad=True
    while escojerdificultad:
        actualizarpantalla()
        numvirus=0
        screen.blit(dificultades,(160,70))
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in [K_1,K_KP1]:
                    numvirus=8
                    escojerdificultad=False
                if event.key in [K_2,K_KP2]:
                    numvirus=14
                    escojerdificultad=False
                if event.key in [K_3,K_KP3]:
                    numvirus=20
                    escojerdificultad=False

    #Genera virus y jugador
    listavirus=[]
    for i in range(numvirus):
        listavirus.append(enemigo())
    player=jugador()

    #Bucle principal
    contador=0
    tiempoinmune=0
    vidas=1
    while vidas>0:
        contador+=1
        actualizarpantalla()
        chequeareventos()
        if player.inmune==False:
            player.pintar()
        if player.inmune==True:            
            tiempoinmune+=1
            if tiempoinmune<100:
                player.pintarinmune()
            elif tiempoinmune<110:
                player.pintar()
            elif tiempoinmune<120:
                player.pintarinmune()
            elif tiempoinmune<130:
                player.pintar()
            elif tiempoinmune<140:
                player.pintarinmune()
            elif tiempoinmune<145:
                player.pintar()
            elif tiempoinmune<150:
                player.pintarinmune()
            if tiempoinmune>150:
                player.noinmune()
        cuentabucles(contador)
        for i in range(numvirus):
            listavirus[i].avanzar()
            if player.inmune==False:
                if colision(i)==True:
                    vidas-=1

    #Bucle final
    endscreen=True
    while endscreen:
        actualizarpantalla()
        for i in range(numvirus):
            listavirus[i].avanzar()
        screen.blit(gameover,(150,40))
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key==K_RETURN:
                    endscreen=False