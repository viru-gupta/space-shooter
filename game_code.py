import pygame
import os
import time
import random

pygame.init()

WIDTH=1000
HEIGHT=670
score=0
#enemy ship
red_ship=pygame.image.load('pixel_ship_red_small.png')
green_ship=pygame.image.load('pixel_ship_green_small.png')
blue_ship=pygame.image.load('pixel_ship_blue_small.png')
#figther ship
yellow_ship=pygame.image.load('pixel_ship_yellow.png')
#bullets
red_bullet=pygame.image.load('pixel_laser_red.png')
green_bullet=pygame.image.load('pixel_laser_green.png')
blue_bullet=pygame.image.load('pixel_laser_blue.png')
#ship bullets
yellow_bullet=pygame.image.load('pixel_laser_yellow.png')
#background
bg=pygame.transform.scale(pygame.image.load('background.jpg'),(WIDTH,HEIGHT))

#screen
win=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('space wars by viru')

class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)
    
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
        
    def move(self,vel):
        self.y+=vel
        
    def off_screen(self,height):
        return not(self.y<=height and self.y>=0)
        
    def collisoin(self,obj):
        return collide(self,obj)

class Ship:
    COOLDOWN=30
    
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.ship_img=None
        self.laser_img=None
        self.lasers=[]
        self.cool_down_counter=0
        
     #for drawing ship
    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)
            
    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collisoin(obj):
                obj.health-=10
                self.lasers.remove(laser)
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter>0:
            self.cool_down_counter+=1
    
    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter=1
    
    
    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img=yellow_ship
        self.laser_img=yellow_bullet
        self.mask=pygame.mask.from_surface(self.ship_img)
        self.max_health=health
        
    def move_(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collisoin(obj):
                        objs.remove(obj)
                        abc()
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                          
        
    def draw(self,window):
        super().draw(window)
        self.healthbar(window)
    
    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width()*(self.health/self.max_health),10))

    
class Enemy(Ship):
    COLOUR_MAP={
                'red':(red_ship,red_bullet),
                'blue':(blue_ship,blue_bullet),
                'green':(green_ship,green_bullet)
                }
    def __init__(self,x,y,colour,health=100):
        super().__init__(x,y,health)
        self.ship_img,self.laser_img=self.COLOUR_MAP[colour]
        self.mask=pygame.mask.from_surface(self.ship_img)
        
    def move(self,vel):
        self.y += vel
        
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
        
def collide(obj1,obj2):
    offset_x = obj2.x-obj1.x
    offset_y = obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) !=None

def abc():
    global score
    score+=1

def main():
    fps=60
    global score
    clock=pygame.time.Clock()
    run=True
    level=0
    lives=5
    fonts=pygame.font.SysFont('comicsans',40)
    lost_font=pygame.font.SysFont('comicsans',60)
    player=Player(475,HEIGHT-100)
    player_velocity=5
    lost=False
    enemies=[]
    no_of_enimes=5
    enemy_vel=1
    laser_vel=5
    lost_count=0
    
    def screen():
        win.blit(bg,(0,0))
        #for text on screen -preparing
        lives_label=fonts.render(f'LIFE: {lives}',1,(255,255,255))
        level_label=fonts.render(f'LEVEL: {level}',1,(255,255,255))
        screen_label=fonts.render(f'YOUR SCORE: {score}',1,(255,255,255))
        
        #now lets display the preapared message on screen
        win.blit(lives_label,(10,10))
        win.blit(level_label,(WIDTH-level_label.get_width()-20,10))
        win.blit(screen_label,(250,10))
        
        #drwing enemy ships
        for enemy in enemies:
            enemy.draw(win)
        #drawing player ship
        player.draw(win)
        
        if lost:
            lost_label=lost_font.render(f'YOU LOST!!',1,(255,255,255)) #adding message to respective font
            win.blit(lost_label,(WIDTH/2-lost_label.get_width()/2,HEIGHT/2))   #displaying message in center
        
        
        pygame.display.update()
        
    while run:
        clock.tick(fps)
        screen()
                     
        if lives<=0 or player.health<=0:
            lost=True
            lost_count+=1
        
        if lost:
            if lost_count > fps * 3:
                run=False
            else:
                continue
        
        if len(enemies)==0:
            level+=1
            no_of_enimes+=5
            for i in range(no_of_enimes):
                enemy=Enemy(random.randrange(50,WIDTH-100),random.randrange(-1000,-150),random.choice(['red','blue','green']))
                enemies.append(enemy)
                
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
        #for multiple key inputing
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x-player_velocity>0:
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x+player_velocity+player.get_width()<WIDTH:
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y-player_velocity>0:
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y+player_velocity+player.get_height()+20<HEIGHT:
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()
            
        
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)
            if random.randrange(0,120)==1:
                enemy.shoot()
                
            if collide(enemy,player):
                player.health-=10
                enemies.remove(enemy)
                score+=1
            
            elif enemy.y+enemy.get_height()>HEIGHT:
                lives-=1
                enemies.remove(enemy)
        
        player.move_(-laser_vel,enemies)

def main_menu():
    run=True
    fontt=pygame.font.SysFont('comicsans',30)
    while run:
        win.blit(bg,(0,0))
        start=fontt.render(f'CLICK TO START!!!',1,(255,255,255))
        win.blit(start,(HEIGHT/2,WIDTH/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
    quit()
main_menu()
