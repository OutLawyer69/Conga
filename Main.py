import pygame
import random

pygame.init()

white=(255,255,255)
black=(0,0,0)
font = pygame.font.Font(None,36)

screen_width = 700
screen_height = 520
playable_width=580
playable_height=400
score=0
follower_flag=False
fps=30
counter=1
follower_space=7

screen= pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Conga Conga Conga")
clock = pygame.time.Clock()
running=True
sprite_sheet=pygame.image.load("assets/character_sheet.png").convert_alpha()
background_image = pygame.image.load("assets/background.png")
background_image = pygame.transform.scale(background_image,(playable_width,playable_height))

def get_image(sheet,row,column):
    image=pygame.Surface((16,24)).convert_alpha()
    image.blit(sheet,(0,0),(16*row,24*column,16*row+16,24*column+24))
    image=pygame.transform.scale(image,(32,48))
    image.set_colorkey(black)
    return image

class congo_line:
    def __init__(self,x,y):
        self.i=0
        self.j=4
        self.x=x
        self.y=y
        self.velx=0
        self.vely=0
        self.image=get_image(sprite_sheet,4,10)
        self.image_set=[]
        self.replay=False
        for n in range(8):
            for k in range(3):
                self.image_set.append(get_image(sprite_sheet,n,k+9))
    def draw(self):
        screen.blit(self.image,(self.x,self.y))
        if self.velx!=0 or self.vely!=0:
            self.image=self.image_set[int(self.j*3+int(self.i))]
        if self.i>2:
            self.i=0
        self.i+=0.14
    def move(self):
        keys=pygame.key.get_pressed()
        if (score==0 or self.j!=2) and keys[pygame.K_LEFT]:
            self.j=6
            self.velx=-5
            self.vely=0
        if (score==0 or self.j!=6) and keys[pygame.K_RIGHT]:
            self.j=2
            self.velx=5
            self.vely=0
        if (score==0 or self.j!=4) and keys[pygame.K_UP]:
            self.j=0
            self.vely=-5
            self.velx=0
        if (score==0 or self.j!=0) and keys[pygame.K_DOWN]:
            self.j=4
            self.vely=5
            self.velx=0
        if (score==0 or self.j!=5) and keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.j=1
            self.velx=3
            self.vely=-4
        if (score==0 or self.j!=3) and keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.j=7
            self.velx=-3
            self.vely=-4        
        if (score==0 or self.j!=7) and keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.j=3
            self.velx=3
            self.vely=4
        if (score==0 or self.j!=1) and keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.j=5
            self.velx=-3
            self.vely=4
    def exit(self):
        screen.fill(white)  
        screen.blit(background_image,((screen_width-playable_width)/2,(screen_height-playable_height)/2))
        screen.blit(Game_over_text,(screen_width/2-80,(screen_height-playable_height)/2-36))
        screen.blit(score_text,(screen_width/2-18*4,(screen_height-playable_height)/2+playable_height+15))
        screen.blit(replay_text,(screen_width/2-120,screen_height/2-20))
        pygame.display.update()
        self.replay=True
            
class follower:
    def __init__(self,x,y,i,j):
        self.x=x
        self.y=y
        self.velx=0
        self.vely=0
        self.image=get_image(sprite_sheet,4,6)
        self.image_set=[]
        self.i=i
        self.j=j
        for n in range(8):
            for k in range(3):
                self.image_set.append(get_image(sprite_sheet,n,k+5))
    def draw(self):
        screen.blit(self.image,(self.x,self.y))
        self.image=self.image_set[int(self.j*3+int(self.i))]

class friend:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.image=get_image(sprite_sheet,4,6)
    def draw(self):
        screen.blit(self.image,(self.x,self.y))
    def collision(self):
        if abs(player.x-self.x)<22 and abs(player.y-self.y)<32:
            self.x=random.randint((screen_width-playable_width)/2,playable_width+(screen_width-playable_width)/2-32)
            self.y=random.randint((screen_height-playable_height)/2,playable_height+(screen_height-playable_height)/2-48)
            global score
            global follower_flag
            follower_flag=True
            score+=1
       
player=congo_line(screen_width/2-16,screen_height/2-24) 
friend1=friend(random.randint((screen_width-playable_width)/2,playable_width+(screen_width-playable_width)/2-32),random.randint((screen_height-playable_height)/2,playable_height+(screen_height-playable_height)/2-48))
followers=[player]
title_text=font.render("Conga, Conga, Conga!",True,(black))
Game_over_text=font.render("GAME OVER!",True,(black))
replay_text=font.render("Press Enter to replay",True,(white))

while running:
    screen.fill(white)  
    screen.blit(background_image,((screen_width-playable_width)/2,(screen_height-playable_height)/2))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if player.replay==True:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            score=0
            player.__init__(screen_width/2-16,screen_height/2-24)
            followers=[player]
            follower_flag=False
            counter=1
    else:
        if follower_flag:
            followers.append(follower(followers[score-1].x,followers[score-1].y,followers[score-1].i,followers[score-1].j))
            counter+=1
            if counter>follower_space:
                follower_flag=False
                counter=1
          
        player.x+=player.velx
        player.y+=player.vely
    
        for x in range(len(followers)-1,0,-1):
            if x>0:
                followers[x].x=followers[x-1].x
                followers[x].y=followers[x-1].y
                followers[x].j=followers[x-1].j
                followers[x].i=followers[x-1].i
        
        for x in range(0,len(followers),follower_space):
            if x!=0:
                followers[x].draw()
        player.draw()
        player.move()
        friend1.draw()
        friend1.collision()
        score_text = font.render(f"Followers: {score}",True,(black))
        screen.blit(title_text,(screen_width/2-140,(screen_height-playable_height)/2-36))
        screen.blit(score_text,(screen_width/2-18*4,(screen_height-playable_height)/2+playable_height+15))
        pygame.display.update()
        
        for x in range(0,len(followers),follower_space):
            if x!=0 and x!=follower_space and abs(player.x-followers[x].x)<15 and abs(player.y-followers[x].y)<15:
                player.exit()
        if (player.y<(screen_height-playable_height)/2-4 or player.y>(screen_height-playable_height)/2+playable_height-46):
            player.exit()
        elif (player.x<(screen_width-playable_width)/2+4 or player.x>(screen_width-playable_width)/2+playable_width-36):
            player.exit()
            
        clock.tick(fps)
        
pygame.quit()