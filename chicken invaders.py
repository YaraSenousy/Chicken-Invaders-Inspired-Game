import pygame
import random
from time import sleep

pygame.init()

display_width = 1100
display_height = 650

gameDisplay= pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Chicken Invaders")


clock= pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)
grey = (100,100,100)
red = (200,0,0)
green = (0,200,0)
background = (23,30,40)
blue = (63,72,204)
lightblue = (112,146,190)
yellow = (255,242,0)
orange = (255,127,39)

firesound = pygame.mixer.Sound("fire_sound.wav")
explosionsound = pygame.mixer.Sound("explosion_sound.wav")
chickensound = pygame.mixer.Sound("chicken_sound.wav")
losesound = pygame.mixer.Sound("life_sound.wav")
pygame.mixer.music.load("space.mp3")

chicken = pygame.image.load("chicken.xcf")
ship = pygame.image.load("spaceship.png")
fire = pygame.image.load("fire.png")
introchicken = pygame.image.load("introchicken.xcf")
explode = pygame.image.load("explode.xcf")
life = pygame.image.load("life.xcf")
egg = pygame.image.load("egg.xcf")
icon=pygame.image.load('chickenicon.xcf')

pygame.display.set_icon(icon)


ship_width = 122
ship_height = 295
ship_heightwithoutlight = 120

introchicken_width = 178
introchicken_height = 150
chicken_width = 100
chicken_height = 84
fire_width = 30
fire_height = 94
egg_width = 30
egg_height = 30

life_width = 35
life_height = 39

def button(text,font,startx,width,starty,height,color,ac,ic,action):
    
    mouse= pygame.mouse.get_pos()
    click= pygame.mouse.get_pressed()
    
    if startx < mouse[0] < (startx + width)   and starty < mouse[1] < (starty + height):
        pygame.draw.rect(gameDisplay, ac, (startx,starty,width,height))
        if click[0] == 1 :
            pygame.mixer.Sound.play(firesound)
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (startx,starty,width,height))

    message_display(text,font,startx,width,starty,height,color)
    
    
def intro():
    pygame.mixer.music.play(-1)
    
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitgame()

        gameDisplay.fill(background)
        message_display("CHICKEN INVADERS",80,(display_width/2 - 200),400,100,150,orange)
        img(introchicken,0,0)
        img(introchicken,(display_width-introchicken_width),0) 
        
        button("Play",40,(display_width/2 - 150),300,300,50,yellow,lightblue,blue,gameloop)
        button("How to play",40,(display_width/2 - 150),300,400,50,yellow,lightblue,blue,controls)
        button("Quit",40,(display_width/2 - 150),300,500,50,yellow,lightblue,blue,exitgame)
        
        pygame.display.update()
        clock.tick(20)

def controls():
    pygame.mixer.music.play(-1)
    
    control = True

    while control:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitgame()

        gameDisplay.fill(background)
        
        message_display("Welcome aboard of your spaceship, You are now on a mission in space!",28,50,1000,30,30,yellow)
        message_display("You can move your ship using UP,Down,Right,or Left arrows",19,55,650,100,30,white)
        message_display("Fire using SPACE to kill all the chicken",19,5,500,180,30,white)
        img(chicken,505,180)
        message_display("Dodge the eggs and dont touch the chicken or you will lose lives",19,5,800,280,30,white)
        img(egg,800,280)
        message_display("Kill the chicken batch to move to the next round",19,5,500,350,30,white)
        message_display("The game is over once you lose your three lives",19,5,500,410,30,white)
        img(life,505,410)
        img(life,540,410)
        img(life,575,410)
        message_display("Good Luck!",30,50,600,500,30,yellow)

        button("Play",25,900,100,580,30,white,lightblue,blue,gameloop)
        button("Menu",25,70,100,580,30,white,lightblue,blue,intro)
        
        pygame.display.update()
        clock.tick(20)
        
def unpause():
    pygame.mixer.music.unpause()
    global pause
    pause = False
 
def paused():
    pygame.mixer.music.pause()
    global pause
    pause = True
    
    while pause == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitgame()
                
        gameDisplay.fill(background)
        message_display("score:"+str(score),20,0,90,0,20,white)        
        message_display("Pause",100,0,display_width,0,display_height,orange)
        
        button("Continue",40,150,200,500,50,yellow,lightblue,blue,unpause)
        button("Menu",40,750,200,500,50,yellow,lightblue,blue,intro)
        button("Quit",40,450,200,500,50,yellow,lightblue,blue,exitgame)
        
        pygame.display.update()
        clock.tick(10)

def gameover():
    
    over = True
    
    while over == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitgame()
                
        gameDisplay.fill(background)
        message_display("score:"+str(score),20,0,90,0,20,white)        
        message_display("GAME OVER",100,0,display_width,0,display_height,red)
        
        button("Play again",40,150,200,500,50,yellow,lightblue,blue,gameloop)
        button("Menu",40,750,200,500,50,yellow,lightblue,blue,intro)
        button("Quit",40,450,200,500,50,yellow,lightblue,blue,exitgame)
        
        pygame.display.update()
        clock.tick(10)


def message_display(text,FONT,startx,width,starty,height,color):
    font =pygame.font.Font("freesansbold.ttf",FONT)
    TextSurf= font.render(text, True, color)
    TextRect = TextSurf.get_rect()
    TextRect.center = (startx+width/2),(starty+height/2)
    gameDisplay.blit(TextSurf,TextRect)

def exitgame():
    pygame.quit()
    quit()

def img(img,x,y):
    gameDisplay.blit(img, (x,y))

    
def gameloop():
    
    ship_x =  (display_width * 0.35)
    ship_y = (display_height * 0.7)
    ship_x_change = 0
    ship_y_change = 0
    chicken_y = [0]
    chicken_x = [1100 - chicken_width]
    fire_y = []
    fire_x = []
    #done = []
    shoot = []
    killed =[0]
    lives_num = 3
    lives = [0]
    rounds = 1
    roundsDis = True

    egg_x = []
    egg_y = []
    eggyes = []
    egg_change = 4
    starttime = 0
    eggfreq = 4
    remainchicken = [0,1,2,3,4,5,6,7,8,9]

    firecount = []
    lastfire = 0
    
    global score
    score = 0
    
    game = True

    for i in range(1,lives_num) :
        lives.append(lives[i-1] + life_width)
        
    while game:
        if (ship_x+60)<=0 or (ship_x+ship_width)>=display_width:
            ship_x_change = 0
        if ship_y<=0 or (ship_y+30)>=display_height:   #(creating boarders)
               ship_y_change = 0
               
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitgame()
            if len(chicken_x)==10:
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_LEFT and (ship_x+60)>0:
                        ship_x_change = -5
                    if event.key == pygame.K_RIGHT and (ship_x + ship_width)<display_width:
                        ship_x_change = 5
                    if event.key == pygame.K_UP and ship_y>0:
                        ship_y_change = -5
                    if event.key == pygame.K_DOWN and (ship_y+30)<display_height:
                        ship_y_change = 5
                    if event.key == pygame.K_SPACE :#and len(fire_x)<4 :
                        shoot.append(True)
                        fire_y.append(ship_y - fire_height)
                        fire_x.append(ship_x+(ship_width*0.72))
                        pygame.mixer.Sound.play(firesound)
                        
                        firecount.append(pygame.time.get_ticks())
                        for i in range(len(firecount)):
                            if len(firecount)>6:
                                if firecount[i]-firecount[i-1] <5000 :         
                                    shoot[-1] = False
                                    lastfire = i
                                    if pygame.time.get_ticks() - firecount[i] >2500:
                                        firecount.clear()
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ship_x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ship_y_change = 0    
                    

        ship_x += ship_x_change
        ship_y += ship_y_change
        fire_change = 5
        gameDisplay.fill(background)
        img(ship,ship_x,ship_y)
        if roundsDis == True:
            message_display("Round "+str(rounds),100,0,display_width,0,display_height,white)

        if len(chicken_x) == 10:
            roundsDis = False
        
        for i in range(len(fire_x)):
            if (fire_y[i]+fire_height) <0 :
                shoot[i] = False
                gameDisplay.fill(background,(fire_x[i],fire_y[i],fire_width,fire_height))

            for j in range(len(chicken_x)):
                if roundsDis == False:
                    if (fire_x[i]>chicken_x[j] and fire_x[i]<(chicken_x[j]+chicken_width) or (fire_x[i]+fire_width)>chicken_x[j] and (fire_x[i]+fire_width)<(chicken_x[j]+chicken_width)) and fire_y[i] < (chicken_y[j]+chicken_height):
                        shoot[i] = False
                        score += 1
                        gameDisplay.fill(background,(fire_x[i],fire_y[i],fire_width,fire_height))
                        chicken_y[j] = -1000
                        chicken_x[j] = -1000
                        remainchicken.remove(j)
                        pygame.mixer.Sound.play(chickensound)
        

            
            if shoot[i] == True:
                img(fire,fire_x[i],fire_y[i])
                fire_y[i] -= fire_change
##            else:
##                done.append(i)
##
##        for i in done:
##            fire_y.pop(i)
##            fire_x.pop(i)
##            shoot.pop(i)
##            done.remove(i)
            
            
        for j in range(len(chicken_x)):  
            img(chicken,chicken_x[j],chicken_y[j])

            if chicken_x[j]>0 and len(chicken_x)<=10:
                if j == 0 or (chicken_x[j] > chicken_x[j-1]+chicken_width and chicken_x[j-1] != -1000):
                    chicken_y[j] = chicken_y[j] + 0.6
                    chicken_x[j] = (chicken_y[j]-200)/-0.2
                    
            if (ship_x>chicken_x[j] and ship_x<(chicken_x[j]+chicken_width) or (ship_x+ship_width)>chicken_x[j] and (ship_x+ship_width)<(chicken_x[j]+chicken_width)):
             if (ship_y < (chicken_y[j]+chicken_height)and ship_y > chicken_y[j])  or (ship_y+ship_heightwithoutlight>chicken_y[j] and ship_y+ship_heightwithoutlight<chicken_y[j]+chicken_height):
                 lives_num = lives_num - 1
                 lives.pop(-1)
                 if lives_num != 0:
                     pygame.mixer.Sound.play(losesound)
                     ship_x =  (display_width * 0.35)
                     ship_y = (display_height * 0.7)

        if len(chicken_x)==10:
            count = 0
            for i in range(0,10):
                if chicken_x[i] == -1000:
                    count = count + 1
                if count == 10:
                    chicken_x.clear()
                    chicken_y.clear()
                    egg_x.clear()            
                    egg_y.clear()                              
                    eggyes.clear()
                    fire_x.clear()
                    fire_y.clear()
                    shoot.clear()
                    chicken_y = [0]
                    chicken_x = [1100 - chicken_width]
                    rounds = rounds + 1
                    roundsDis = True
                    remainchicken = [0,1,2,3,4,5,6,7,8,9]
                    eggfreq += 0.7                                      #inc difficulty
                    egg_change += 0.5
                    
        now = pygame.time.get_ticks()/1000
        if (now - starttime) > eggfreq and roundsDis == False:
            thechicken = random.choice(remainchicken)
            starttime = now
            egg_x.append(chicken_x[thechicken]+chicken_width/2)            #timer
            egg_y.append(chicken_y[thechicken]+chicken_height)
            eggyes.append(True)
            
        for i in range(len(egg_x)):
            if egg_y[i] > display_height:
                eggyes[i] = False
                egg_x[i]= -1000
                egg_y[i] = 1000
                
            if ((egg_x[i]>ship_x and egg_x[i]<(ship_x+ship_width)) or ((egg_x[i]+egg_width)>ship_x and (egg_x[i]+egg_width)<(ship_x+ship_width))) and (egg_y[i] > ship_y and egg_y[i]<(ship_y+ship_heightwithoutlight)):
                eggyes[i] = False
                egg_x[i]= -1000
                egg_y[i] = 1000
                lives_num -= 1
                lives.pop(-1)
                if lives_num != 0:
                 pygame.mixer.Sound.play(losesound)
                 ship_x =  (display_width * 0.35)
                 ship_y = (display_height * 0.7)
    

            
            if eggyes[i] == True :
                img(egg,egg_x[i],egg_y[i])
                egg_y[i] += egg_change

            
        for i in range(lives_num):
            img(life,lives[i],22)
            
        if lives_num == 0 :
            gameDisplay.fill(background,(ship_x,ship_y,200,ship_height))
            img(explode,ship_x+ship_width/2,ship_y)
            pygame.mixer.Sound.play(explosionsound)
            pygame.display.update()
            pygame.time.delay(1000)
            gameover()
            
        if display_width-(chicken_x[-1]+chicken_width) > chicken_width and chicken_x[0] > 0:
            chicken_y.append(0)
            chicken_x.append(1100 - chicken_width)

        if lastfire != 0:
            if pygame.time.get_ticks() - firecount[lastfire] <2500:
                message_display("charging",20,180,90,0,20,red)
        message_display("score:"+str(score),20,0,90,0,20,white)
        message_display("round"+str(rounds),20,90,90,0,20,white)
        button("pause",20,1010,90,0,20,white,lightblue,background,paused)
        pygame.display.update()
        clock.tick(60)

intro()    



##chicken movement *
##chicken overlapping *
##eggs *
##timer for the eggs *
##explosion *
##hearts and game over *
##a time before the game start *
##sound effects(fire, explosion, losing a life,chicken dying), and music  *
##icon *
##how to play *
##inc difficulty *
##fire limit (using time) *
##charging message *
##check images height and width *


##dt = clock.tick(30) / 1000               #time handling 
##pygame.time.get_ticks()

##crashsound = pygame.mixer.Sound("Crash .mp3")
##    pygame.mixer.Sound.play(crashsound)
##pygame.mixer.music.load("Race Car - Rondo Brothers.mp3")
##pygame.mixer.music.play(-1)                                             #sound
##    pygame.mixer.music.stop()
##        pygame.mixer.music.pause()
##            pygame.mixer.music.unpause()



            
