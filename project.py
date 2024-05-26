import pygame
from pygame.locals import *
import sys
from pygame.math import Vector2
import time


pygame.init()
#Screen
width = 700
height = 700
tile_size=35
screen = pygame.display.set_mode((width, height))

#Images
background=pygame.image.load("images/grass1.jpg")
snake = pygame.image.load("images/snakeIcon.png")
snakebg=pygame.image.load("images/snake2.png")
startImg = pygame.image.load("images/start_btn.png")
exitImg = pygame.image.load("images/exit_btn.png")
pauseImg=pygame.image.load("images/pause.png")
nextImg=pygame.image.load("images/next.png")
#treeImg= pygame.image.load("images/tree.png")
#hole=pygame.image.load("images/hole.png")
snakeHeadRight = pygame.image.load("images/RightHead.png")
snakeHeadLeft = pygame.image.load("images/LeftHead.png")
snakeHeadUp = pygame.image.load("images/UpHead.png")
snakeHeadDown = pygame.image.load("images/DownHead.png")
snakeHead = snakeHeadDown  # Initial head image
snakeheadMask=pygame.mask.from_surface(snakeHead)
headRect = snakeHead.get_rect()
headRect.topleft = (38, 38)
heart1=pygame.image.load("images/heart.png")
heart2 = pygame.image.load("images/heart.png")
heart3 = pygame.image.load("images/heart.png")
#img = pygame.image.load('images/apple.png')
# Set positions for all hearts
heartRect=heart1.get_rect()
heartRect.topright=(690,5)
heartRect2 = heart2.get_rect()
heartRect2.topright = (650, 5)  # Adjust position for the second heart
heartRect3 = heart3.get_rect()
heartRect3.topright = (610, 5)  # Adjust position for the third heart
soldier=pygame.image.load("images/soldier.png")
deadApple=pygame.image.load("images/deadApple2.png")
deadAppleRect=deadApple.get_rect()
deadAppleRect.topleft=(200,300)
deadAppleMask=pygame.mask.from_surface(deadApple)
bulletImg = pygame.image.load("images/fire.png")  # Add bullet image
bulletRect = bulletImg.get_rect()
bulletRect.center = soldier.get_rect().center  # Initially position bullet with soldier
bulletMask=pygame.mask.from_surface(bulletImg)

#Sounds
mainMusic=pygame.mixer.Sound("sounds/main.mp3")
mainMusic.set_volume(0.2)
mainMusic.play(-1)
gameOverMusic=pygame.mixer.Sound("sounds/gameOver.mp3")
gameOverMusic.set_volume(1)
winMusic=pygame.mixer.Sound("sounds/win.mp3")
winMusic.set_volume(1)
click=pygame.mixer.Sound("sounds/click.wav")
click.set_volume(1)
lostLife=pygame.mixer.Sound("sounds/lostLife.mp3")
lostLife.set_volume(1)

#Colors
fontColor=(240,240,240)

#Upper bar
pygame.display.set_caption("Snake Game")
pygame.display.set_icon(snake)

clock = pygame.time.Clock()
pause=False
hitCount=0
appleCount=0
daimondCount=0
bullet_speed = 20
bullet_active = False  


def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, height))

# Class for buttons
class Button():
    def __init__(self, x, y, image,scale):
        Bwidth = image.get_width()
        Bheight = image.get_height()
        self.image = pygame.transform.scale(image, (int(Bwidth * scale), int(Bheight * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked=False
   
    def draw(self):
        action=False
        pos=pygame.mouse.get_pos()
        

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                click.play()
                action = True
                

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action        


#Text
def TextThings(text,font):
    textSurface = font.render(text, True, fontColor)
    return textSurface, textSurface.get_rect()

class Apple(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('images/apple.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y) 

appleGroup = pygame.sprite.Group()

class world():
    def __init__(self,data):

        miniT1_img = pygame.image.load('images/miniTree1.png')
        miniT2_img = pygame.image.load('images/miniTree2.png')
        miniT3_img = pygame.image.load('images/miniTree3.png')
        rocks=pygame.image.load('images/rocks.jpg')
        daimond=pygame.image.load('images/diamond.png')
        #appleImg=pygame.image.load('images/apple.png')
        mushroom=pygame.image.load('images/mushroom.webp')

        self.tile_list = []
        self.mask_list = []  # List to hold masks for tiles
        row_count=0

        for row in data:
            col_count = 0
            for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(rocks, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                        self.mask_list.append(pygame.mask.from_surface(img))
                    if tile == 2:
                        img = pygame.transform.scale(miniT1_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                        self.mask_list.append(pygame.mask.from_surface(img))
                    if tile == 3:
                        img = pygame.transform.scale(miniT2_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                        self.mask_list.append(pygame.mask.from_surface(img))
                    if tile == 4:
                        img = pygame.transform.scale(miniT3_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                        self.mask_list.append(pygame.mask.from_surface(img))    
                    if tile == 5:
                        img = pygame.transform.scale(mushroom, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile) 
                        self.mask_list.append(pygame.mask.from_surface(img))
                    if tile == 6:
                        apple = Apple(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                        appleGroup.add(apple)
                    if tile == 7:
                        img = pygame.transform.scale(daimond, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile) 
                        self.mask_list.append(pygame.mask.from_surface(img))              
                    col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])      
            #pygame.draw.rect(screen,(255,255,255),tile[1],2)

    def check_collision(self, headRect, snakeheadMask):
        for tile, mask in zip(self.tile_list, self.mask_list):
            if mask:  # Only check tiles with masks
                offset = (headRect.x - tile[1].x, headRect.y - tile[1].y)
                if mask.overlap(snakeheadMask, offset):
                    return True
        return False
    
level1_data=[
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 6, 0, 0, 0, 6, 0, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 7, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

level2_data=[
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


level1=world(level1_data)
level2=world(level2_data)
start = Button(100, 450, startImg,0.8)
end = Button(500, 450, exitImg,0.8)
pausebtn=Button(5,5,pauseImg,0.8)
nextbtn=Button(500,450,nextImg,0.8)



def gameIntro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background,(0,0))
    
        screen.blit(snakebg,(145,150))
        
        if start.draw():
            gameLoop() 
        if end.draw():
            click.play()  
            time.sleep(0.2)
            gameQuit() 
            
        pygame.display.update()  
        clock.tick(15)  
        
def unpause():
    global pause
    pause = False

def paused():
    largeText = pygame.font.SysFont("Elephant",115)
    TextSurf, TextRect = TextThings("Paused", largeText)
    TextRect.center = ((width/2),(height/2))
    screen.blit(TextSurf, TextRect)


    while pause:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if start.draw():
            unpause() 
        if end.draw():
            gameQuit() 

        pygame.display.update()
        clock.tick(15)

def gameQuit():

    pygame.quit()
    quit()

def gameOver():
    mainMusic.stop()  # Stop the main music
    gameOverMusic.play()  # Play the game over music
    mainMusic.play()

    largeText = pygame.font.SysFont("Elephant", 100)
    TextSurf, TextRect = TextThings("Game Over", largeText)
    TextRect.center = ((width / 2), (height / 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.blit(background, (0, 0))
        screen.blit(TextSurf, TextRect)

        if start.draw():
            gameLoop()
        if end.draw():
            click.play()  
            time.sleep(0.2)
            gameQuit()

        pygame.display.update()
        clock.tick(15)

def winLevel2():
    mainMusic.stop()
    winMusic.play()


    largeText = pygame.font.SysFont("Elephant", 100)
    TextSurf, TextRect = TextThings("You won!", largeText)
    TextRect.center = ((width / 2), (height / 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.blit(background, (0, 0))
        screen.blit(TextSurf, TextRect)

        if nextbtn.draw():
            gameLoop2()
        if end.draw():
            click.play()  
            time.sleep(0.2)
            gameQuit()

        pygame.display.update()
        clock.tick(15)

def win():
    mainMusic.stop()
    winMusic.play()

    largeText = pygame.font.SysFont("Elephant", 100)
    TextSurf, TextRect = TextThings("You won!", largeText)
    TextRect.center = ((width / 2), (height / 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.blit(background, (0, 0))
        screen.blit(TextSurf, TextRect)

        if start.draw():
            gameLoop2()
        if end.draw():
            click.play()  
            time.sleep(0.2)
            gameQuit()

        pygame.display.update()
        clock.tick(15)

def gameLoop():
    global snakeHead, headRect, pause, snakeheadMask
    snakeHead = snakeHeadDown  # Reset snake head direction
    snakeheadMask = pygame.mask.from_surface(snakeHead)  # Reset snake head mask
    headRect.topleft = (38, 38)  # Reset snake head position
    direction = Vector2(0, 0)  # Initial direction is down
    hitCount=0
    heartRect.topright=(690,5)
    heartRect2.topright = (650, 5)  # Adjust position for the second heart
    heartRect3.topright = (610, 5)  # Adjust position for the third heart
   
   
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                previous_position = headRect.topleft  # Update the previous position before moving
                if event.key == K_UP:
                    direction = Vector2(0, -20)
                    snakeHead = snakeHeadUp
                if event.key == K_DOWN:
                    direction = Vector2(0, 20)
                    snakeHead = snakeHeadDown
                if event.key == K_LEFT:
                    direction = Vector2(-20, 0)
                    snakeHead = snakeHeadLeft
                if event.key == K_RIGHT:
                    direction = Vector2(20, 0)
                    snakeHead = snakeHeadRight
                snakeheadMask = pygame.mask.from_surface(snakeHead)
   
        headRect.topleft += direction  # Move the snake head
         
        screen.blit(background, (0, 0))
        level1.draw()
        draw_grid()
        pygame.draw.rect(screen, (255, 255, 255), headRect, 2)
        screen.blit(snakeHead, headRect)
        appleGroup.update()
        appleGroup.draw(screen)
        screen.blit(heart1, heartRect)
        screen.blit(heart2, heartRect2)
        screen.blit(heart3, heartRect3)
        

        if pausebtn.draw():
            pause = True
            paused()

        if level1.check_collision(headRect, snakeheadMask):
            lostLife.play()
            hitCount += 1
            headRect.topleft = previous_position  
            if hitCount >= 3:
                time.sleep(0.5)
                gameOver()

            if hitCount == 1:
                heartRect3.topleft = (-100, -100)
            elif hitCount == 2:    
                heartRect2.topleft = (-100, -100)
            elif hitCount == 3:
                heartRect.topleft = (-100, -100)
                
        
        pygame.display.update()
        clock.tick(10)

def gameLoop2():
    global snakeHead, headRect, pause, snakeheadMask, bullet_active, bulletRect, bulletMask, bullet_speed, width
    snakeHead = snakeHeadDown  # Reset snake head direction
    snakeheadMask = pygame.mask.from_surface(snakeHead)  # Reset snake head mask
    headRect.topleft = (38, 38)  # Reset snake head position
    direction = Vector2(0, 0)  # Initial direction is down
    hitCount=0
    heartRect.topright=(690,5)
    heartRect2.topright = (650, 5)  # Adjust position for the second heart
    heartRect3.topright = (610, 5)  # Adjust position for the third heart
    last_bullet_time = time.time()
    bullet_active = False
    bulletRect = pygame.Rect(soldier.get_rect().centerx, soldier.get_rect().centery, 10, 10)
    bulletMask = pygame.mask.from_surface(bulletImg)  # Create a mask for the bullet image


    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                previous_position = headRect.topleft  # Update the previous position before moving
                if event.key == K_UP:
                    direction = Vector2(0, -20)
                    snakeHead = snakeHeadUp
                if event.key == K_DOWN:
                    direction = Vector2(0, 20)
                    snakeHead = snakeHeadDown
                if event.key == K_LEFT:
                    direction = Vector2(-20, 0)
                    snakeHead = snakeHeadLeft
                if event.key == K_RIGHT:
                    direction = Vector2(20, 0)
                    snakeHead = snakeHeadRight
                snakeheadMask = pygame.mask.from_surface(snakeHead)
   
        headRect.topleft += direction  # Move the snake head
        
        if deadAppleMask.overlap(snakeheadMask,(headRect.x-deadAppleRect.x,headRect.y-deadAppleRect.y)):
            gameOver()
            

        screen.blit(background, (0, 0))
        level2.draw()
        draw_grid()
        pygame.draw.rect(screen, (255, 255, 255), headRect, 2)
        screen.blit(snakeHead, headRect)
        appleGroup.update()
        appleGroup.draw(screen)
        screen.blit(heart1, heartRect)
        screen.blit(heart2, heartRect2)
        screen.blit(heart3, heartRect3)
        screen.blit(soldier,(575,50))
        screen.blit(deadApple,deadAppleRect)

        if bullet_active:
            # Calculate bullet direction
            target_x, target_y = 0, height  # Bottom-left corner of the screen
            dx = target_x - bulletRect.centerx
            dy = target_y - bulletRect.centery
            bullet_speed = 20
            # Normalize the direction vector
            length = (dx**2 + dy**2)**0.5
            dx /= length
            dy /= length
            bulletRect.x += bullet_speed * dx
            bulletRect.y += bullet_speed * dy
            if bulletRect.right < 0 or bulletRect.left > width or bulletRect.bottom < 0 or bulletRect.top > height:
                bullet_active = False

        else:
            current_time = time.time()
            if current_time - last_bullet_time > 20:  # Fire a bullet every 2 seconds
                bullet_active = True
                bulletRect.center = (575,50)
                last_bullet_time = current_time

        if bullet_active:
            screen.blit(bulletImg, bulletRect)

        # Check collision with bullet
        if bullet_active and snakeheadMask.overlap(bulletMask, (headRect.x - bulletRect.x, headRect.y - bulletRect.y)):
            gameOver()

        if pausebtn.draw():
            pause = True
            paused()

        if level2.check_collision(headRect, snakeheadMask):
            lostLife.play()
            hitCount += 1
            headRect.topleft = previous_position  # Revert to the previous position on collision
            if hitCount >= 3:
                time.sleep(0.9)
                gameOver()

            if hitCount == 1:
                heartRect3.topleft = (-100, -100)
            elif hitCount == 2:    
                heartRect2.topleft = (-100, -100)
            elif hitCount == 3:
                heartRect.topleft = (-100, -100)

        pygame.display.update()
        clock.tick(10)

# Call things
gameIntro()
gameLoop()

