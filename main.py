import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('SpaceInvader//space-background.png')

#background sound
mixer.music.load('SpaceInvader//background-sound.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('SpaceInvader//ufo.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('SpaceInvader//player.png')
playerX = 370
playerY = 480
playerX_change = 0

#Ememy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6 

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('SpaceInvader//enimies.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


#Bullet
# Ready - you can't see bullet on fiew
# Fire - The bullet is currently moving 
bulletImg = pygame.image.load('SpaceInvader//bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"
score = 0

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)

def showScore(x,y):
    score = font.render("Score:"+ str(score_value),True,(0,255,255))
    screen.blit(score,(x, y))

def player(x,y):
    screen.blit(playerImg,(x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(0,255,255))
    screen.blit(over_text,(200, 250))

#Create gmae loop
running = True
while running:

    #screen.fill((155,89,182))
    #screen.fill((0,0,0))
    #playerX += 0.2
    #background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
        # if krystroke is pressed check right or left for players
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                #print("left arrow pressed.!")
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                #print("right arrow pressed.!")
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('SpaceInvader//laser.wav')
                    bullet_sound.play()
                    # get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)            
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #print("pressed keys released!")
                playerX_change = 0

    # checking for boundries of spaceship.
    playerX += playerX_change
    
    # This on keep our ship inside the box for player
   
    if playerX <=0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

    #Bullet Movement
    
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    #Enimies Movements
    # checking for boundries of enemy.
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i] > 400:
            for j in  range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        # This on keep our ship inside the box for Enemy
        if enemyX[i] <=0:
            enemyX_change[i]  = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i]  = -0.3
            enemyY[i] += enemyY_change[i]
        
        #Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('SpaceInvader//explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1            
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i],i)


    player(playerX,playerY)
    showScore(textX,textY)
    pygame.display.update()
