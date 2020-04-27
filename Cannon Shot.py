import pygame
import random

pygame.init()

screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
w, h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Space Invaders")
bg = pygame.image.load('full_bg.jpg')
the_cannon = pygame.image.load('the cannon.png')
the_explosion = pygame.image.load('the explosion.png')
score = 0
lives = 3
bulletSound = pygame.mixer.Sound('Laser.wav')
music = pygame.mixer.music.load('theme.mp3')
pygame.mixer.music.play(-1)
all_enemies = [pygame.image.load('the enemy.png'), pygame.image.load('the enemy1.png'), pygame.image.load('the enemy2.png'), pygame.image.load('the enemy4.png'), pygame.image.load('the enemy5.png'), pygame.image.load('the enemy6.png'),]

class Cannon(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 25

    def draw(self, screen):
        screen.blit(the_cannon, (self.x, self.y))


class Projectile(object):
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.vel = 20

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Ship(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8
        self.pos = random.randrange(6)
        self.the_enemy = all_enemies[self.pos]

    def draw(self, screen):
        screen.blit(self.the_enemy, (self.x, self.y))
        self.y = self.y + self.vel

def redrawGameWindow():
    global score, lives
    cannon.draw(screen)
    screen.blit(bg, (0, 0))
    cannon.draw(screen)
    text = font.render('Score: ' + str(score), 1, (51, 153, 255))
    text_lives = font.render("Lives: " + str(lives), 1,  (51, 152, 255))
    screen.blit(text, (0, 0))
    screen.blit(text_lives, (0, 30))
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for enemy in enemies:
        for bullet in bullets:
            if((bullet.y < enemy.y + enemy.height) and (bullet.y > enemy.y) and (bullet.x > enemy.x) and (bullet.x < enemy.x + enemy.width)):
                score = score + ((enemy.pos + 1) * 10)
                bullets.pop(bullets.index(bullet))
                enemies.pop(enemies.index(enemy))

    for enemy in enemies:
        if(enemy.y + enemy.height >= h):
            enemies.pop(enemies.index(enemy))
            lives -= 1
        if((enemy.y + enemy.height >= cannon.y + 10) and ((enemy.x >= cannon.x) and (enemy.x <= cannon.x + cannon.width))):
            enemies.pop(enemies.index(enemy))
            lives -= 1
    pygame.display.update()

game_over = False
running = True
bullets = []
enemies = []
explosions = []
pos = 0

cannon = Cannon(w // 2, h - 78, 64, 64)
font = pygame.font.SysFont('comicsans', 40, True)
def main_function():
    global running, started
    while (running):
        pygame.time.delay(50)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
        for bullet in bullets:
            if (bullet.y > 0):
                bullet.y -= bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
        keys = pygame.key.get_pressed()
        if (len(enemies) < 4):
            posx = random.randrange(5, w - 60, 1)
            posy = 0
            enemies.append(Ship(posx, posy, 40, 40))
        if (keys[pygame.K_SPACE]):
            if (len(bullets) < 20):
                bullets.append(Projectile(round(cannon.x + cannon.width // 2), cannon.y, (255, 255, 102), 4))
            bulletSound.play()
        if (keys[pygame.K_LEFT] and cannon.x > 5):
            cannon.x -= cannon.vel

        elif (keys[pygame.K_RIGHT] and cannon.x + cannon.width < w - 5):
            cannon.x += cannon.vel

        if(keys[pygame.K_q]):
            running = False
        if lives == 0:
            running = False
        redrawGameWindow()

def start_game():
    global game_over, score
    run = True
    text = pygame.font.SysFont('comicsans', 40)
    data = text.render("Click space to start the game!", 1,  (51, 152, 255))
    tutorial = text.render("Left and right arrow keys to move and space to shoot", 1,  (51, 152, 255))
    while run and not game_over:
        screen.blit(bg, (0, 0))
        screen.blit(data, (w//2 - 200, h // 2 - 20))
        screen.blit(tutorial, (w // 2 - 200, h // 2 + 20))
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_SPACE]):
            main_function()
            game_over = True
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                game_over = True
                run = False
        pygame.display.update()

    game_over = False
    while not game_over:
        screen.blit(bg, (0, 0))
        go = text.render("Game Over!", 1, (51, 152, 255))
        screen.blit(go, (w // 2 - 200, h // 2 - 20))
        start_again = text.render("Press q to quit", 1, (51, 152, 255))
        score_text = text.render("Score: " + str(score), 1, (51, 152, 255))
        screen.blit(start_again, (w // 2 - 200, h // 2 + 20))
        screen.blit(score_text, (w // 2 - 200, h // 2 + 50))
        keys1 = pygame.key.get_pressed()
        if (keys1[pygame.K_q]):
            game_over = True
        pygame.event.pump()
        pygame.display.update()

if not game_over:
    start_game()
pygame.quit()
