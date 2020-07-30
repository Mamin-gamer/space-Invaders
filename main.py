#import all things for creating path, pygame, time and random for all internal things
import textwrap
import os
import random
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
try:
    import pygame
except Exception as e:
    raise  e


#initialising pygame window so it will stay opened
pygame.font.init()


#set constants for window and FPS
FPS = 60
WIDTH, HEIGHT = 800, 600

MAIN_BUTTON_WIDTH = 150
MAIN_BUTTON_HEIGHT = 50
BACK_BUTTON_WIDTH = 50
BACK_BUTTON_HEIGHT = 50

#Load inages for ships, BG and laser
RED_SHIP = pygame.image.load(os.path.join("pics", "pixel_ship_red_small.png"))
GREEN_SHIP = pygame.image.load(os.path.join("pics", "pixel_ship_green_small.png"))
BLUE_SHIP = pygame.image.load(os.path.join("pics", "pixel_ship_blue_small.png"))

PLAYER_SHIP = pygame.image.load(os.path.join("pics", "pixel_ship_yellow.png"))
YELLOW_LASER = pygame.image.load(os.path.join("pics", "pixel_laser_yellow.png"))

RED_LASER = pygame.image.load(os.path.join("pics", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("pics", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("pics", "pixel_laser_blue.png"))

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("pics", "background-black.png")), (WIDTH, HEIGHT))

#Parent class SpaceShip for all ships(player and enemy)
class SpaceShip:
    def __init__(self, x, y, health = 100, damage = 50, delay = 0.5):

        #setting varisbles for class

        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.delay = delay

        self.lasers = []
        self.ship_pic = None
        self.lazer_pic = None

        self.pause = 1


        #draw method for drawing healthbar and lasers for all ships
    def draw(self, master):
        self.healthbar(master)
        master.blit(self.ship_pic, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(master)

    #method to move lasers on the screen
    def move_lasers(self, velocity, object, shooter):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)

            #if laser is on the screen, otherwise deletes it
            if laser.off() == True:
                self.lasers.remove(laser)
            # if laser collides with object it decreses it health by laser`s health damage
            elif laser.collision(object):
                object.health -= shooter.damage
                self.lasers.remove(laser)
                #removes obkect if it`s health below 0
                if object.health <= 0:
                    if laser in self.lasers:
                        self.lasers.remove(laser)

    #lets player`s ship shoot only once in FPS time
    def cooldown(self):
        if self.pause >= self.delay * FPS:
            self.pause = 0
        elif self.pause > 0:
            self.pause +=1

    #creates a laser object and starts the timer for player not to shoot
    def shoot(self):
        if self.pause == 0:
            laser = Laser(self.x - 15, self.y, self.laser_pic)
            self.lasers.append(laser)
            self.pause = 1

    #draws the healthbar for player
    def healthbar(self, master):
        pygame.draw.rect(master, (255,0,0), (self.x, self.y + self.ship_pic.get_height() +10, self.ship_pic.get_width(), 10) )
        if self.health > 0:
            pygame.draw.rect(master, (0,255,0), (self.x, self.y + self.ship_pic.get_height() + 10, int(self.ship_pic.get_width() * (self.health/self.max_health)), 10))


    #pygame method for getting width and height of an object(img)
    def get_width(self):
        return self.ship_pic.get_width()

    def get_height(self):
        return self.ship_pic.get_height()


# child class Player inherits __init__ from Parent with creating its own
class Player(SpaceShip):
    def __init__(self, x,y, health = 100, damage = 50):
        super().__init__(x,y)
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.damage = damage

        self.ship_pic = PLAYER_SHIP
        self.laser_pic = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_pic)

    #move player`s laser
    def move_lasers(self, velocity, objects):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off() == True:
                self.lasers.remove(laser)
            else:
                for obj in objects:
                    if laser.collision(obj):
                        obj.health -= self.damage
                        if obj.health <= 0:
                            if obj in objects:
                                objects.remove(obj)

                        #when laser hits object it removes from the screen
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def shoot(self):
        if self.pause == 0:
            laser = Laser(self.x, self.y, self.laser_pic)
            self.lasers.append(laser)
            self.pause = 1

# child class Enemy inherits __init__ from SpaceShip and gives it`s own colours and images
class Enemy(SpaceShip):
    colours = {
                "red": (RED_SHIP, RED_LASER),
                "green": (GREEN_SHIP, GREEN_LASER),
                "blue": (BLUE_SHIP, BLUE_LASER)
                }
    def __init__(self, x,y, colour, damage = 10, health = 50, delay = 1, speed = 1):

        super().__init__(x,y,health, damage, delay)
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.speed = speed
        self.ship_pic, self.laser_pic = self.colours[colour]
        self.mask = pygame.mask.from_surface(self.ship_pic)

    #method to move the ship itself by several pixels depending on its velocity(each ship has got it`s own velocity)
    def move(self, velocity):
        self.y += velocity


#class Laser for all lasers in the game
class Laser:
    def __init__(self, x, y, picture):
        self.x = x
        self.y = y
        self.pic = picture
        self.mask = pygame.mask.from_surface(self.pic)
    #draws laser on the screen
    def draw(self, master):
        master.blit(self.pic, (self.x, self.y))
    #moves laser
    def move(self, velocity):
        self.y += velocity

    #returns if the laser is off the screen
    #30 is the height of labels (level and lives)
    def off(self):
        return not(self.y >= -30 and self.y <= HEIGHT)

    #of object collide with anything
    def collision(self, object):
        return collide(self, object)


def collide(object1, object2):
    distance_x = object2.x - object1.x
    distance_y = object2.y - object1.y
    #return if mask of object 1 overlaps with the mask of object 2
    return object1.mask.overlap(object2.mask, (distance_x, distance_y)) !=None


#function that splits large text and displays it in Pygame window. (textwrapping)
def blit_text(surface, text, pos = (0,0), font = None, max_width = 0, padding_left = 0, padding_right = 0, colour=pygame.Color('white')):
    #function must take 2 arguments: window itself and text, optional are: position of the text`s top left corner, pygame font, width of the text e.g. width of block in css/html
            #padding from both sides to control positions better and colour of the font

    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.

    #if max_width wasn`t changet, it declares it as window`s width-padding
    if max_width == 0:
        max_width = surface.get_width() - padding_right - padding_right

    max_height = surface.get_height()

    #changes x-position of the pos tuple to add the paddinf up
    pos = list(pos)
    pos[0] += padding_left
    x, y = pos


    #iterates through each line in the 2D array
    for line in words:
        #iterates through each word in line
        for word in line:
            word_surface = font.render(word, 0, colour)
            word_width, word_height = word_surface.get_size()
            #checks if starting coordinate + width of the word is less than maximal width available
            # BUG: text can go off the edge because of max_width and starting position, however it won`t go off is starting positon is 0
            if x + word_width >= max_width + pos[0]:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space*2
        x = pos[0]  # Reset the x.
        y += word_height


class Button:
    #declares variables for buttons
    def __init__(self, x, y, width, height, text = None, colour = None, font = None):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text
        self.colour = colour
        if font:
            self.font = font
        else:
            self.font = pygame.font.SysFont('comsicsans', 40)

    #displays button on window
    def draw(self, win, outline = (255,255,255)):
        if self.text:
            writing = self.font.render(self.text, 1, (255,255,255))
        #if outline exists it will draw outline
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)
        win.blit(writing, (self.x + (self.width//2 - writing.get_width()//2), self.y + (self.height//2 - writing.get_height()//2)))
        pygame.display.update()

    #checks if cursor is over the button
    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

#creates help menu where people can find rules and movements
def option_help():
    run = True

    win.blit(BACKGROUND, (0,0))
    # constant check so window won`t close and check for button hover and press
    while run:
        #declares fonts
        welcome_font = pygame.font.SysFont('Papyrus', 60)
        font =  pygame.font.SysFont('Papyrus', 20)

        #displays "inscruction"
        welcome_text = welcome_font.render('Instructions', 1, (255,255,255))
        win.blit(welcome_text, (win.get_width()//2 -welcome_text.get_width()//2, 10))

        #displays chosen text coming through function
        player_text = 'Movement = "WASD" and arrows. You have got 100HP wich is shown under the yellow Spaceship\nTo shoot you should press "Spacebar", however, there is a delay between each bullet'
        blit_text(win, player_text, pos = (150, 100), font = font, max_width = 500)

        #displays chosen text coming through function

        enemy_text = 'There are different types of enemies. Greater Wave - harder opponents.\nThere are some ships which are extremely fast and some which kill you with the first shot'
        blit_text(win, enemy_text, pos = (150, 250), font = font, max_width = 500)

        #displays chosen text coming through function

        extra_text = 'If you collide with any enemy - you lose some HP.\nIf you survive the wave - you get HP.\n\nGood Luck!'
        blit_text(win, extra_text, pos = (150, 400), font = font, max_width = 500)

        #places the button
        exit_button = Button(x = 10, y = win.get_height() - 100, width = BACK_BUTTON_WIDTH, height = BACK_BUTTON_HEIGHT, text = '<--', colour = (0, 0, 0), font = (pygame.font.SysFont('comsicsans', 30)))

        #checks for position of cursor
        pos = pygame.mouse.get_pos()

        if exit_button.is_over(pos):
            exit_button.colour = (255,0,0)
        else:
            exit_button.colour = (0, 0, 0, 0)
        exit_button.draw(win)


        #if window closes - everything stops
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            #if button is pressed - function stops and main will be displayed again
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.is_over(pos):
                    return



#function for credits
def option_credits():
    run = True

    win.blit(BACKGROUND, (0,0))
    while run:
        welcome_font = pygame.font.SysFont('Papyrus', 60)
        font =  pygame.font.SysFont('Papyrus', 20)

        welcome_text = welcome_font.render('Credits', 1, (255,255,255))
        win.blit(welcome_text, (win.get_width()//2 -welcome_text.get_width()//2, 10))

        tim_credits_text = 'Idea came from YouTube "Tech With Tim". All assets reserved to TechWithTim.\n'
        blit_text(win, tim_credits_text, pos = (100, 200), font = font, max_width = 600)

        my_credits_text = 'Project`s GitHub: "https://github.com/Mamin-gamer/space-Invaders".\nMost of the code, algorithm and design are reserved to:\nDmitrii Ponomarev aka. @mamin_gamer.'
        blit_text(win, my_credits_text, pos = (100, 300), font = font, max_width = 500)

        exit_button = Button(x = 10, y = win.get_height() - 100, width = BACK_BUTTON_WIDTH, height = BACK_BUTTON_HEIGHT, text = '<--', colour = (0, 0, 0), font = (pygame.font.SysFont('comsicsans', 30)))

        pos = pygame.mouse.get_pos()

        if exit_button.is_over(pos):
            exit_button.colour = (255,0,0)
        else:
            exit_button.colour = (0, 0, 0, 0)
        exit_button.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.is_over(pos):
                    return





#main function to call everything
def main():

    font = pygame.font.SysFont('comsicsans', 60)

    #creates a lits of buttons to iterate throung
    buttons = []
    play_button = Button(x = win.get_width()//2 - MAIN_BUTTON_WIDTH//2, y = win.get_height() - 400, width = MAIN_BUTTON_WIDTH, height = MAIN_BUTTON_HEIGHT, text = 'Play', colour = (0, 0, 0))
    help_button = Button(x = win.get_width()//2 - MAIN_BUTTON_WIDTH//2, y = win.get_height() - 300, width = MAIN_BUTTON_WIDTH, height = MAIN_BUTTON_HEIGHT, text = 'Help', colour = (0, 0, 0))
    credits_button = Button(x = win.get_width()//2 - MAIN_BUTTON_WIDTH//2, y = win.get_height() - 200, width = MAIN_BUTTON_WIDTH, height = MAIN_BUTTON_HEIGHT, text = 'Credits', colour = (0, 0, 0))
    exit_button = Button(x = 10, y = win.get_height() - 100, width = BACK_BUTTON_WIDTH, height = BACK_BUTTON_HEIGHT, text = 'Quit', colour = (0, 0, 0), font = (pygame.font.SysFont('comsicsans', 30)))

    buttons.extend((play_button, help_button, credits_button, exit_button))

    welcome_text = font.render('Choose your option', 1, (255,255,255))
    win.blit(BACKGROUND, (0,0))
    win.blit(welcome_text, (win.get_width()//2 - welcome_text.get_width()//2, 100))

    show_up = False
    run = True
    while run:
        #constant retreive of cursor position
        pos = pygame.mouse.get_pos()

        #iterate through pygame events
        for event in pygame.event.get():
            #if window closes - app destroys
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            #iterates throung each button and checks hovers and presses
            for btn in buttons:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn.is_over(pos):
                        if btn.text == 'Play':
                            main_game()

                        if btn.text == 'Help':
                            option_help()

                        if btn.text == 'Credits':
                            option_credits()

                        if btn.text == 'Quit':
                            run = False
                            pygame.quit()
                            break

                        #resets backgroung and text
                        win.blit(BACKGROUND, (0,0))
                        win.blit(welcome_text, (win.get_width()//2 - welcome_text.get_width()//2, 100))

                if btn.is_over(pos):
                    btn.colour = (255,0,0)
                else:
                    btn.colour = (0, 0, 0, 0)
                btn.draw(win)


    pygame.quit()



#function of game itself
def main_game():
    #set internal variables for player, enemy and laser
    lifes = 5
    lvl = 0
    run = True
    play = True
    counter = 0
    font = pygame.font.SysFont('comicsans', 40)

    clock = pygame.time.Clock()
    player_damage = 50

    player_velocity = 5

    laser_velocity = 8
    enemy_amount = 5
    enemies = []
    #creates player entity
    player = Player(WIDTH//2 - PLAYER_SHIP.get_width()//2 , HEIGHT//2, health = 100, damage = player_damage)

    #updates the screen with writing lives and wave No on the top
    def reset():
        win.blit(BACKGROUND, (0,0))

        #'draws' the player calling special method
        player.draw(win)
        #draw every enemy on the screen
        for enemy in enemies:
            enemy.draw(win)

        lives_label = font.render(f'lives: {lifes}', 1, (255,255,255))
        lvl_label = font.render(f'Wave No: {lvl}', 1, (255,255,255))
        win.blit(lives_label, (10,10))
        win.blit(lvl_label, (WIDTH-20-lvl_label.get_width(), 10))
        #if player has lost it shows message
        if play == False:
            lost_label = font.render(f'You lost!!!', 1, (255,255,255))
            lost_label2 = font.render(f'Your survived in {lvl-1} waves', 1, (255,255,255))
            win.blit(lost_label, (WIDTH //2 - lost_label.get_width()//2, HEIGHT//2 - lost_label.get_height()//2))
            win.blit(lost_label2, (WIDTH //2 - lost_label2.get_width()//2, HEIGHT//2 - lost_label.get_height()//2+20))



        pygame.display.update()



    while run:
        clock.tick(FPS)
        reset()

        #check is player had lost already
        if lifes <= 0 or player.health <=0:
            play = False

        # wait for 3 seconds so player will see how many waves he survived in
        if play == False:
            reset()
            while counter < FPS * 3:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                counter+=1
                clock.tick(FPS)

            else:
                #finishes the game and cleans the screen
                run = False
                win.blit(BACKGROUND, (0,0))

        #checks for Pygame event so by closing the window it will nit give any errors
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #checks enemy list and increments lvl by 1 if list is empty(level completed)
        if len(enemies) == 0:
            lvl+=1
            player.health += 10
            if player.health > player.max_health:
                player.health = player.max_health

            #sets difficulties of level
            if lvl <=3:
                enemy_amount = 3
            else:
                enemy_amount = enemy_amount + random.randint(0, enemy_amount-1)

            #renders each enemy seperately
            for _ in range(enemy_amount):

                y = random.randint(-1500, -300)
                x = random.randint(int(player.get_width()), int(WIDTH - 70))
                speed = random.randint(1, min(6, lvl))

                if lvl <=3:
                    enemy = Enemy(x,y, colour = 'green', health = random.choice([50, 75]), speed = 2, damage = 10, delay = 1)
                    enemies.append(enemy)
                    continue

                #different classes of enemy

                #super tank
                if speed == 1:
                    damage = 30
                    delay = 5
                    colour = 'red'
                    health = 200

                #simple tank
                elif speed == 2 or speed == 3:
                    damage = 15
                    colour = 'red'
                    health = 100
                    delay = 1

                #average
                elif speed == 4 or speed == 5:
                    damage = 10
                    colour = 'green'
                    health = 50
                    delay = 1

                #speedy one
                elif speed == 6:
                    damage = 5
                    delay = 1
                    health = 25
                    colour = 'blue'


                if speed == 1:
                    pass
                else:
                    speed //= 2

                #adds enemy to a list
                enemy = Enemy(x,y, colour,  health = health, damage = damage, speed = speed, delay = delay)
                enemies.append(enemy)

        #checks through keys being pressed
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - player_velocity > 0: # left
            player.x -= player_velocity
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + player_velocity + player.get_width() < WIDTH: # right
            player.x += player_velocity
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - player_velocity > 0: # up
            player.y -= player_velocity
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + player_velocity + player.get_height() + 15 < HEIGHT: # down
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()


        #cheks through enemy list and renders it
        for enemy in enemies[::]:
            enemy.move(enemy.speed)
            enemy.move_lasers(laser_velocity, player, enemy)
            if random.randint(0, enemy.delay*FPS//2) == 1:
                enemy.shoot()
            #checks collision with anything
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lifes -=1
                enemies.remove(enemy)

        player.move_lasers(-laser_velocity, enemies)





#sets window with constant width and height
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')




if __name__ == '__main__':
    main()
