import pygame as pg
import random


WIDTH,HEIGHT=300,600

pg.init()
screen=pg.display.set_mode((WIDTH,HEIGHT),0,32)

background=pg.Surface((WIDTH,HEIGHT))
background.fill((100,150,255))

def write(msg,size):
    font=pg.font.SysFont("none",size)
    text=font.render(msg,False,(1,1,1))
    text.set_colorkey((255,255,255))
    text.convert_alpha()
    return text


allgroups=pg.sprite.LayeredUpdates()
floorgroup=pg.sprite.Group()
herogroup=pg.sprite.Group()


class Terrain(pg.sprite.Sprite):
    speed=50
    width,height=10,10
    def __init__(self,pos=[0,0]):
        self.groups=allgroups,floorgroup
        self._layer=1
        pg.sprite.Sprite.__init__(self,self.groups)
        
        self.image=pg.Surface((self.width,self.height))
        self.image.fill((200,150,40))
        self.image.convert()

        self.rect=self.image.get_rect()
        self.radius=self.rect.width/2
        self.rect.center=pos
        
        self.area=screen.get_rect()

    def update(self,time):
        self.rect.centery-=time*self.speed
        if not self.area.contains(self.rect):
            self.kill()


class Hero(pg.sprite.Sprite):
    speed=100
    width,height=10,10
    dx,dy=0,0
    def __init__(self,pos=[]):
        self.groups=allgroups,herogroup
        self._layer=2
        pg.sprite.Sprite.__init__(self,self.groups)
        
        self.image=pg.Surface((self.width,self.height))
        self.image.fill((40,150,200))
        self.image.convert()

        self.rect=self.image.get_rect()
        self.radius=self.rect.width/2
        self.rect.center=pos
        
        self.area=screen.get_rect()

        self.alive=True

    def update(self,time):
        key=pg.key.get_pressed()
        if key[pg.K_RIGHT]:
            self.rect.centerx+=self.speed*time
        if key[pg.K_LEFT]:
            self.rect.centerx-=self.speed*time

        for enemy in floorgroup.sprites(): 
            if self.rect.colliderect(enemy.rect):
                self.rect.bottom=enemy.rect.top
                self.dy=0
                break

        else:
            self.dy=self.speed*time


        self.rect.centery+=self.dy

        if not self.area.contains(self.rect):
            self.kill()
            print("YOU DIED")
            self.alive=False


running=True
FPS=60
clock=pg.time.Clock()



screen.blit(background,(0,0))
x,y=int(WIDTH/Terrain.width),int(HEIGHT/Terrain.height)

spawnfrequency=2
tpals=0
score=0
first=True
hero=Hero((WIDTH/2,HEIGHT-10*Hero.height))


while running:
    time=clock.tick(FPS)/1000.0
    tpals+=time

    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE:
                running=False

                

    if tpals>spawnfrequency or first:
        gap=random.randint(2,x)
        for i in range(1,x+1):
            if gap is not i and gap !=i+1:
                Terrain([i*WIDTH/x-Terrain.width/2,HEIGHT-Terrain.height/2])
        
        if Terrain.speed<Hero.speed*0.7:
            Terrain.speed+=1

        tpals=0
        first=False
      

    allgroups.update(time)
    allgroups.clear(screen,background)  
    allgroups.draw(screen)


    if hero.alive:
        text=write("SCORE:"+str(int(score)),20)
        screen.blit(background.subsurface(text.get_rect()),(0,0))
        screen.blit(text,(0,0))
        pg.display.update(text.get_rect())
        score+=time

    else:
        text=write("YOU DIED",50)
        screen.blit(text,(60,HEIGHT/2-2*text.get_rect()[1]))
        pg.display.update(text.get_rect())

        text=write(" SCORE:"+str(int(score)),50)
        screen.blit(text,(50,HEIGHT/2-2*text.get_rect()[1]+50))
        pg.display.update(text.get_rect())


    pg.display.flip()
