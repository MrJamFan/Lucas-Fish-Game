import pygame
import random 

#setup  the ai
class BadGuy():
    #bad guy constctor function 

    #bad guy vairbles
    def __init__(self, x, y, speed, size):
        self.x = x
        self.y = y
        self.pic = pygame.image.load("../assets/Fish03_B.png")
        self.speed = speed
        self.size = size
        self.hitbox = pygame.Rect(self.x, self.y, int(self.size*1.25), self.size)

        #shirnk bad guy pic
        self.pic = pygame.transform.scale(self.pic , ( int (self.size*1.25), self.size))

        #flip the badguy pic
        if self.speed < 0:
            self.pic = pygame.transform.flip(self.pic, True, False)

    #bad guy update function
    def update(self, screen):
        self.x += self.speed
        self.hitbox.x += self.speed
        screen.blit(self.pic, (self.x, self.y))
        
                
#ai code ends here

# Start the game
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True
#loading pics in top left   
background_pic = pygame.image.load("../assets/Scene_B.png")
#player
fishy_pic = pygame.image.load("../assets/Fish02_A.png")

#make some varibles for our player
fishy_starting_x = 480
fishy_starting_y = 310
fishy_starting_size = 30
fishy_x = fishy_starting_x
fishy_y = fishy_starting_y
fishy_speed = 3
fishy_size = 30
fishy_facing_left = False
fishy_hitbox = pygame.Rect(fishy_x, fishy_y,int(fishy_size*1.25), fishy_size)
fishy_alive = False


#cool varibles HUD
score = -1
score_font = pygame.font.SysFont("default", 30)
score_text = score_font.render("Score: "+str(score) , 1, (255, 255, 255))

Play_button_pic = pygame.image.load("../assets/BtnPlayIcon.png")
Play_button_x = game_width/2 - Play_button_pic.get_width()/2
Play_button_y = game_height/2 - Play_button_pic.get_height()/2

title_font = pygame.font.SysFont("default", 60)
title_text = "EAT OR GET EATEN"
title_render = title_font.render(title_text , 1, (255, 255, 255))
title_width, title_height = title_font.size(title_text)

BadGuys_timer_max = 45
BadGuys_timer = BadGuys_timer_max
# make the badguy array
BadGuys = []
BadGuys_to_remove = []




# ***************** Loop Land Below :D *****************
# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    screen.blit(background_pic, (0, 0))
    fishy_pic_small = pygame.transform.scale(fishy_pic, (int(fishy_size*1.25 ), fishy_size))

    # this should be further down.  Check the video @ 12:00
    for Badguy in BadGuys_to_remove:
        BadGuys.remove(Badguy)
    BadGuys_to_remove = []
    
#use cool code to update all bad guys



#   oopsy.  Let's not redefine BadGuy here
    for Badguy in BadGuys:
        Badguy.update(screen)

    BadGuys_timer -= 1
    if BadGuys_timer <=0:
        
        new_BadGuy_y = random.randint(0, game_height)
        new_BadGuy_speed = random.randint(1, 10)
        new_BadGuy_size = random.randint(int(fishy_size/2),int(fishy_size*2.5))
        if random.randint(0, 1) == 0:
            BadGuys.append(BadGuy(-new_BadGuy_size*2, new_BadGuy_y, new_BadGuy_speed, new_BadGuy_size))
        else: 
            BadGuys.append(BadGuy(game_width, new_BadGuy_y, -new_BadGuy_speed, new_BadGuy_size))            

        BadGuys_timer = BadGuys_timer_max

    
    if fishy_facing_left:
        fishy_pic_small = pygame.transform.flip(fishy_pic_small, True, False)

    if fishy_alive:
        #player hitbox
        fishy_hitbox.x = fishy_x
        fishy_hitbox.y = fishy_y
        fishy_hitbox.width = int(fishy_size * 1.25)
        fishy_hitbox.height = fishy_size
            
        

        #eat or die checker
        for Badguy in BadGuys:
            if fishy_hitbox.colliderect(Badguy.hitbox):
                if fishy_size >= Badguy.size:
                    fishy_size += 3 
                    score += round(Badguy.size / 2)
                    BadGuys.remove(Badguy)
                else: fishy_alive = False
        
        #checkes to see when and what keys are pressed to move
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            fishy_x += fishy_speed
            fishy_facing_left = False
             
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            fishy_x  -= fishy_speed
            fishy_facing_left = True

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            fishy_y -= fishy_speed

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            fishy_y  += fishy_speed

        if keys[pygame.K_SPACE]:
            fishy_size += 2
        screen.blit(fishy_pic_small, (fishy_x, fishy_y))

    #score update
    if fishy_alive == True:        

        score_text = score_font.render("Score: "+str(score) , 1, (255, 255, 255))

    else:
        score_text = score_font.render("Final Score: "+str(score) , 1, (255, 255, 255))

    if score >= 0:   
        screen.blit(score_text, (30, 30))
    
       
    


    #menu
    if not fishy_alive:
        screen.blit(Play_button_pic, (Play_button_x, Play_button_y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        title_text = title_font.render("EAT OR GET EATEN" , 1, (255, 255, 255))
        screen.blit(title_render, ((game_width/2)-(title_width/2),250))
        #check if mouse is clicked
        if pygame.mouse.get_pressed()[0]:
            if mouse_x > Play_button_x and mouse_x < Play_button_x + Play_button_pic.get_width():
                 if mouse_y > Play_button_y and mouse_y < Play_button_y + Play_button_pic.get_height():
                     #Restarts the game
                     fishy_alive = True
                     score = 0
                     fishy_size = fishy_starting_size
                     fishy_x = fishy_starting_x
                     fishy_y - fishy_starting_y
                     for Badguy in BadGuys:
                         BadGuys_to_remove.append(Badguy)
              

    
                
    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("MY GAME fps: " + str(clock.get_fps()))
