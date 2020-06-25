#import all things for creating path, pygame, time and random for all internal things

import os
import random
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


#main function to call everything
def main():
    run = True

    font = pygame.font.SysFont('comicsans', 60)
    #infinate loop for playing
    while run:
        win.blit(BACKGROUND, (0,0))
        #create 2 texts with explanation of game
        label_start = font.render('WASD, Space - shoot', 1, (65,65,100))
        label = font.render('Press spacebar to start...', 1, (65,65,100))

        height = HEIGHT//2 - label.get_height()/2
        width = WIDTH//2 - label.get_width()/2
        #place labels on the screen
        win.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT//2 -  label.get_height()//2 - 20))
        win.blit(label_start, (WIDTH//2 - label_start.get_width()//2, HEIGHT//2 -  label_start.get_height()//2 + 120))
        #renders the screen
        pygame.display.flip()
        # pygame.QUIT so it won`t rause error when its quited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break

            #if spacebar is pressed - game starts
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game()

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

    laser_velocity = 7
    enemy_amount = 5
    enemies = []
    #creates player entity
    player = Player(WIDTH//2, HEIGHT//2, health = 10, damage = player_damage)

    #updates the screen with writing lives and wave No on the top
    def reset():
        win.blit(BACKGROUND, (0,0))
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

        #'draws' the player calling special method
        player.draw(win)
        #draw every enemy on the screen
        for enemy in enemies:
            enemy.draw(win)

        pygame.display.update()



    while run:

        clock.tick(FPS)
        reset()

        #check is player had lost already
        if lifes <= 0 or player.health <=0:
            play = False

        # wait for 5 seconds so player will see how many waves he survived in
        if play == False:
            while counter < FPS * 5:
                counter+=1
                clock.tick(FPS)
                reset()
            else:
                #finishes the game
                run = False

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
pygame.display.set_caption('Space Raiders')
if __name__ == '__main__':

    main()
