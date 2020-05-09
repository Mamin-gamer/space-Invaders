import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import random
pygame.font.init()

FPS = 60
WIDTH, HEIGHT = 800, 600

BOOST_HEALTH_ICON = None
BOOST_DAMAGE_ICON = None
BOOST_SPEED_ICON = None
BOOST_LIFE_ICON = None


RED_SHIP = pygame.image.load(os.path.join("pics", "pixel_ship_red_small.png"))
GREEN_SHIP = pygame.image.load(os.path.join("pics", "pixel_ship_green_small.png"))
BLUE_SHIP = pygame.image.load(os.path.join("pics", "pixel_ship_blue_small.png"))

PLAYER_SHIP = pygame.image.load(os.path.join("pics", "pixel_ship_yellow.png"))
YELLOW_LASER = pygame.image.load(os.path.join("pics", "pixel_laser_yellow.png"))

RED_LASER = pygame.image.load(os.path.join("pics", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("pics", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("pics", "pixel_laser_blue.png"))

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("pics", "background-black.png")), (WIDTH, HEIGHT))

class Boost:
    icons = {
        'health':BOOST_HEALTH_ICON,
        'damage':BOOST_DAMAGE_ICON,
        'speed':BOOST_SPEED_ICON,
        'life':BOOST_LIFE_ICOT
    }


    def __init__(self, x,y, boost, duration):
        self.x = x
        self.y = y
        self.boost = boost
        self.boost_icon = icons[boost]
        self.duration = duration

        self.mask = pygame.mask.from_surface(self.boost_icon)

    def draw(self):
        pass

    def move(self, icon):
        pass


class SpaceShip:
    def __init__(self, x, y, health = 100, damage = 50, delay = 0.5):

        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.delay = delay

        self.lasers = []
        self.ship_pic = None
        self.lazer_pic = None

        self.pause = 1

    def draw(self, master):
        self.healthbar(master)
        master.blit(self.ship_pic, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(master)


    def move_lasers(self, velocity, object, shooter):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off() == True:
                self.lasers.remove(laser)
            elif laser.collision(object):
                object.health -= shooter.damage
                self.lasers.remove(laser)
                if object.health <= 0:
                    if laser in self.lasers:
                        self.lasers.remove(laser)


    def cooldown(self):
        if self.pause >= self.delay *FPS:
            self.pause = 0
        elif self.pause > 0:
            self.pause +=1


    def shoot(self):
        if self.pause == 0:
            laser = Laser(self.x, self.y, self.laser_pic)
            self.lasers.append(laser)
            self.pause = 1

    def healthbar(self, master):
        pygame.draw.rect(master, (255,0,0), (self.x, self.y + self.ship_pic.get_height() +10, self.ship_pic.get_width(), 10) )
        if self.health >0:
            pygame.draw.rect(master, (0,255,0), (self.x, self.y + self.ship_pic.get_height() + 10, self.ship_pic.get_width() * (self.health/self.max_health), 10))

    def get_width(self):
        return self.ship_pic.get_width()

    def get_height(self):
        return self.ship_pic.get_height()



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


                        if laser in self.lasers:
                            self.lasers.remove(laser)


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

    def move(self, velocity):
        self.y += velocity


    def shoot(self):
        if self.pause == 0:
            laser = Laser(self.x , self.y, self.laser_pic)
            self.lasers.append(laser)
            self.pause = 1


class Laser:
    def __init__(self, x,y, picture):
        self.x = x
        self.y = y
        self.pic = picture
        self.mask = pygame.mask.from_surface(self.pic)

    def draw(self, master):
        master.blit(self.pic, (self.x - 15, self.y))

    def move(self, velocity):
        self.y += velocity

    def off(self):
        return not(self.y > 0 and self.y < HEIGHT)


    def collision(self, object):
        return collide(self, object)


def collide(object1, object2):
    distance_x = object2.x - object1.x
    distance_y = object2.y - object1.y

    return object1.mask.overlap(object2.mask, (distance_x, distance_y)) !=None




def main():
    run = True

    font = pygame.font.SysFont('comicsans', 60)

    while run:
        win.blit(BACKGROUND, (0,0))
        label_start = font.render('WASD, Space - shoot', 1, (65,65,100))
        label = font.render('Press spacebar to start...', 1, (65,65,100))
        height = HEIGHT/2 -  label.get_height()/2
        width = WIDTH/2 - label.get_width()/2

        win.blit(label, (WIDTH/2 - label.get_width()/2, HEIGHT/2 -  label.get_height()/2 - 20))
        win.blit(label_start, (WIDTH/2 - label_start.get_width()/2, HEIGHT/2 -  label_start.get_height()/2 + 120))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game()

    pygame.quit()



def main_game():
    lifes = 5
    lvl = 0
    run = True
    play = True
    c = 0
    font = pygame.font.SysFont('comicsans', 40)

    clock = pygame.time.Clock()
    player_damage = 50

    player_velocity = 5

    laser_velocity = 7
    enemy_amount = 5
    enemies = []

    player = Player(WIDTH//2, HEIGHT//2, health = 100, damage = player_damage)
    def reset():
        win.blit(BACKGROUND, (0,0))
        lives_label = font.render(f'lives: {lifes}', 1, (255,255,255))
        lvl_label = font.render(f'Wave No: {lvl}', 1, (255,255,255))

        win.blit(lives_label, (10,10))
        win.blit(lvl_label, (WIDTH-10-lvl_label.get_width(), 10))

        if play == False:
            lost_label = font.render(f'You lost!!!', 1, (255,255,255))
            lost_label2 = font.render(f'Your survived in {lvl-1} waves', 1, (255,255,255))
            win.blit(lost_label, (WIDTH //2 - lost_label.get_width()//2, HEIGHT//2 - lost_label.get_height()//2))
            win.blit(lost_label2, (WIDTH //2 - lost_label2.get_width()//2, HEIGHT//2 - lost_label.get_height()//2+20))

        player.draw(win)

        for enemy in enemies:
            enemy.draw(win)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        reset()
        if lifes <= 0 or player.health <=0:
            play = False


        if play == False:
            if c < FPS * 5:
                continue
            else:
                run = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        if len(enemies) == 0:
            lvl+=1
            player.health += 10
            if player.health > player.max_health:
                player.health = player.max_health

            if lvl <=3:
                enemy_amount = 3
            else:
                enemy_amount = enemy_amount + random.randint(0, enemy_amount-1)


            for _ in range(enemy_amount):

                y = random.randint(-1500, -300)
                x = random.randint(int(player.get_width()), int(WIDTH - 70))
                speed = random.randint(1, min(6, lvl))

                if lvl <=3:
                    enemy = Enemy(x,y, colour = 'green', health = random.choice([50, 75]), speed = 2, damage = 10, delay = 1)
                    enemies.append(enemy)
                    continue
                # speed /= 2
                if speed == 1: #Tank
                    damage = 30
                    delay = 5
                    colour = 'red'
                    health = 200
                elif speed == 2 or speed == 3:
                    damage = 15
                    colour = 'red'
                    health = 100
                    delay = 1
                elif speed == 4 or speed == 5:
                    damage = 10
                    colour = 'green'
                    health = 50
                    delay = 1
                elif speed == 6:
                    damage = 5
                    delay = 1
                    health = 25
                    colour = 'blue'
                if speed == 1:
                    pass
                else:
                    speed //= 2
                enemy = Enemy(x,y, colour,  health = health, damage = damage, speed = speed, delay = delay)
                enemies.append(enemy)


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



        for enemy in enemies[::]:
            enemy.move(enemy.speed)
            enemy.move_lasers(laser_velocity, player, enemy)
            if random.randint(0, enemy.delay*FPS//2) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lifes -=1
                enemies.remove(enemy)

        player.move_lasers(-laser_velocity, enemies)




win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Raiders')

if __name__ == '__main__':

    main()
