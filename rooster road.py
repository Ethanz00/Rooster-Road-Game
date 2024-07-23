import sys, pygame,random

# Starting the mixer
pygame.mixer.init()
# Loading the song
pygame.mixer.music.load("song.wav")
# Start playing the song
pygame.mixer.music.play()
#begin pygame
pygame.init()

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

#define dimensions and colour
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BLACK = (0, 0, 0)

#enable keypresses
key=True
#game is not in lost state
lost=False
#game is not in level end state
levelend=False
#initial speed 5
speed=5
#turn sound on
sound=True
#set dimensions and application name into pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Crossy Road')

#class for potions
class Buffs:
    def __init__(self,name):
        self.buff=pygame.image.load("potion.png")
        self.buff=pygame.transform.rotozoom(self.buff,0,0.1)
        self.buffrect=self.buff.get_rect()
        self.name=name
        

    #method for displaying potion
    def draw(self):
        screen.blit(self.buff,self.buffrect)

    #method for changing position of potion
    def setPosition(self,x,y):
        self.buffrect.x = x
        self.buffrect.y = y

class Chicken:
    def __init__(self):
        self.chicken=pygame.image.load("chicken.png")
        self.chicken=pygame.transform.rotozoom(self.chicken,0,0.1)
        self.rect=self.chicken.get_rect()
        self.setPosition(400,800)
        self.speed=15
        #list for acquired potions
        self.bufflist=[]
        #turn advance buff off
        self.advance=False
        self.setVelocity(0,0)
        #level begins at 1
        self.level=1
        
    def setVelocity(self,vx,vy):
        self.setVelocity=[vx,vy]

    def setPosition(self,x,y):
        self.rect.x = x
        self.rect.y = y
    
    def move(self):
        self.rect=self.rect.move(self.setVelocity)
        #ensure player says within window
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>SCREEN_WIDTH:
            self.rect.right=SCREEN_WIDTH
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>SCREEN_HEIGHT:
            self.rect.bottom=SCREEN_HEIGHT
        
    def draw(self):
        screen.blit(self.chicken,self.rect)

#class for car
class Car:
    def __init__(self):
        self.car=pygame.image.load("car.png")
        self.car=pygame.transform.rotozoom(self.car,0,0.075)
        self.rect=self.car.get_rect()
        
        
    def setPosition(self,x,y):
        self.rect.x = x
        self.rect.y = y
    
    #method for changing the velocity of car
    def setVelocity(self,vx,vy):
        self.setVelocity=[vx,vy]
    
    #method for drawing
    def draw(self):
        screen.blit(self.car,self.rect)

    #method for moving car betweeen every frame
    def move(self):
        self.rect=self.rect.move(self.setVelocity)

        for car in carlist:
            #if player hits car with no invincibility, game ends
            if car.rect.colliderect(chicken.rect) and invincibility==False:
                global lost
                lost=True

            #remove cars that exit screen
            if car.rect.x>SCREEN_WIDTH:
                carlist.remove(car)
            #remove speed buff, disregarding invincibility upon collision
            if car.rect.colliderect(chicken.rect):
                #remove speed buff upon collision 
                chicken.advance=False
                
                for buff in chicken.bufflist:
                    if buff=="Speed":
                        chicken.bufflist.remove("Speed")
                    

#2 potion objects
vincrease=Buffs("Speed")
invincible=Buffs("invincible")

#timer for potion spawning
recur=0
#timer for car spawning
spawn=0
spawn_rate=650
#time when speed potion is consumed
speed_start_timer=0
#time when invincibility potion is consumed
invincibility_start_timer=0

#list for different buff's in game
unattained_buff_list=[]

#create chicken object
chicken=Chicken()

#create list for cars
carlist=[]

#no keys being pressed
pressed=False

#list for possible spawn coordinates
carspawn=[]

#turn off buff's/effects at start of game
invincibility=False

#assign possible y coordinates for car spawning
for x in range(0,SCREEN_HEIGHT,int(SCREEN_HEIGHT/5)):
    carspawn.append(x)

while True:
    for event in pygame.event.get():
        #if pygame is exited, stop program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #clock
    time=pygame.time.get_ticks()

    #every 3 seconds given that no potions have been attained spawn new potion
    if time>recur+3000 and chicken.bufflist==[]:

        #randomise potion spawn
        item=random.choice([vincrease,invincible])

        #speed potion
        if item==vincrease:
            item=Buffs("Speed")
        #invincible potion
        else:
            item=Buffs("invincible")
        
        #randomise potion spawn coordinates
        item.setPosition(random.randint(55, SCREEN_WIDTH-55), random.randint(55, SCREEN_HEIGHT-55))

        #append potion to potion list to be drawn later
        unattained_buff_list.append(item)

        #time of potion being spawned
        recur=time

    #if potion has elapsed 5 seconds
    if time>speed_start_timer+5000:
        #revert speed
        chicken.advance=False
        #remove buff from displayed list
        for buff in chicken.bufflist:
            if buff=="Speed":
                chicken.bufflist.remove("Speed")
    
    #if invincibility potion has elapsed 3 seconds
    if time>invincibility_start_timer+3000  and invincibility ==True:

        #remove invinciibilty
        for buff in chicken.bufflist:
            if buff=="invincible":
                chicken.bufflist.remove("invincible")
        invincibility=False
    
    #spawn new car interval of time
    if time>spawn+spawn_rate:
        #set spawn time
        spawn=time
        #spawn cars in sets of 2
        for x in range(2): 
            car=Car()
            car.setPosition(-55,random.choice(carspawn))
            car.setVelocity(speed,0)
            #append object to list
            carlist.append(car)

    #if a key is released, there are no keys being pressed (allows for key tap movement)
    if event.type==pygame.KEYUP:
        pressed=False

    # key is being tapped
    if event.type==pygame.KEYDOWN and key==True:

        #clock for purposes such as endgame
        time2=time

        #if speed buff is on, move smoothly
        if chicken.advance==True:
            if event.key==pygame.K_LEFT:
                chicken.setVelocity[0]=-chicken.speed
            if event.key==pygame.K_RIGHT:
                chicken.setVelocity[0]=chicken.speed
            if event.key==pygame.K_UP:
                chicken.setVelocity[1]=-chicken.speed
            if event.key==pygame.K_DOWN:
                chicken.setVelocity[1]=chicken.speed
        
        #if speed buff is off, move with taps
        if pressed==False and chicken.advance==False:
            pressed=True
            if event.key==pygame.K_LEFT:
                chicken.setPosition(chicken.rect.x-54,chicken.rect.y)
                if sound==True:
                    #sound effect
                    pygame.mixer.Sound.play(pygame.mixer.Sound("tap.wav"))
            if event.key==pygame.K_RIGHT:
                chicken.setPosition(chicken.rect.x+54,chicken.rect.y)
                if sound==True:
                    pygame.mixer.Sound.play(pygame.mixer.Sound("tap.wav"))
            if event.key==pygame.K_UP:
                chicken.setPosition(chicken.rect.x,chicken.rect.y-54)
                if sound==True:
                    pygame.mixer.Sound.play(pygame.mixer.Sound("tap.wav"))
            if event.key==pygame.K_DOWN:
                chicken.setPosition(chicken.rect.x,chicken.rect.y+54)
                if sound==True:
                    pygame.mixer.Sound.play(pygame.mixer.Sound("tap.wav"))
    #when no key press, don't move
    else:
        chicken.setVelocity=[0,0]

    for power in unattained_buff_list:
        #collision between potion and player
        if power.buffrect.colliderect(chicken.rect):
            pygame.mixer.Sound.play(pygame.mixer.Sound("potionsound.wav"))
            #if potion is speed change speed
            if power.name=="Speed":
                speed_start_timer=time
                chicken.advance=True

            #if potion is invincibility turn on invincibility
            if power.name=="invincible":
                #clock for when potion is attained
                invincibility_start_timer=time
                invincibility=True

            #add potion to list display
            if power.name not in chicken.bufflist:
                chicken.bufflist.append(power.name)

            #remove potion from screen upon collision
            power.setPosition(-100,-100)
   
    #stat menu 
    buff_font=pygame.font.SysFont("Arial",20)

    #show buffs, time
    counter_text=buff_font.render(f'Buffs: {chicken.bufflist} Time:{time/1000} ' ,True,(255,255,255))
    #fill screen black
    screen.fill(BLACK)
    road=pygame.image.load("road.png")
    screen.blit(road,(0,0))
    #draw and move cars
    for car in carlist:
        car.move()
        car.draw()
    #draw potions
    for power in unattained_buff_list:
        power.draw()

    #draw and move chicken
    chicken.move()
    chicken.draw()
    #display stats
    screen.blit(counter_text,(20,20))

    #when chicken hits top of screen
    if chicken.rect.y==0 or levelend==True:
        #turn on invincibility
        invincibility=True
        invincibility_start_timer=time
        chicken.bufflist.append("invincible")

        #change state of game to levelend
        if chicken.rect.y==0:
            levelend=True
            #turn sound off
            sound=False
            #add level to counter
            chicken.level+=1
            #disable key presses
            key=False
            #play sparkle sound
            pygame.mixer.Sound.play(pygame.mixer.Sound("bell.wav"))
                       
        #remove cars from screen
        for car in carlist:
            carlist.remove(car)
        #move chicken to start
        chicken.setPosition(400,800)
        #time that game ended
        finaltime=time2

        #after 2 seconds has elapsed, exit out of loop
        if time-finaltime>2000:
            levelend=False
            #turn sound on
            sound=True
            #allow key presses
            key=True
            #remove potions from screen 
            for power in unattained_buff_list:
                unattained_buff_list.remove(power)
            #increase speed of cars
            speed+=5
            #min spawn rate of 0.05 seconds
            if spawn_rate>50:
                #decrease spawn rate
                spawn_rate+=-75

            #remove personal buffs   
            invincibility=False
            chicken.advance=False   
        for buff in chicken.bufflist:
            chicken.bufflist.clear()
        
        #during endlevel, make screen black
        screen.fill(BLACK)

        #display next level stats
        end_font=pygame.font.SysFont("Arial",30)
        end_game=end_font.render(f"Level {chicken.level}" ,True,(255,255,255))
        screen.blit(end_game,(10,400))
        
    # if game is in state of lost
    if  lost==True:
        Sound=False
        #disable key presses
        key=False
        #record time lost
        finaltime=time2
        
        #make screen black
        screen.fill(BLACK)

        #write game over with final level
        end_font=pygame.font.SysFont("Arial",30)
        end_game=end_font.render(f"Chicken Died at level {chicken.level} :(" ,True,(255,255,255))
        screen.blit(end_game,(10,400))

        #when 3 seconds has elapsed, end game
        if time-finaltime>3000:
            pygame.quit()
    pygame.display.flip()
    
    #game refresh rate
    fpsClock.tick(60)