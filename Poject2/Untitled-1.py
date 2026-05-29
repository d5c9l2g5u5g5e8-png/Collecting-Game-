from pygame import *
from random import randint
from time import time as timer

win_width = 1550
win_height = 800

#Klasy

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), ( size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Buff(GameSprite):

    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y - 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Collectables(GameSprite):

    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0


class Enemy(GameSprite):

    def update(self):
        global rocket

        distance_x = rocket.rect.x - self.rect.x
        distance_y = rocket.rect.y - self.rect.y

        if abs(distance_x) > 50:
            if distance_x > 0:
                self.rect.x += 1
            else:
                self.rect.x -= 1

        if abs(distance_y) > 50:
            if distance_y > 0:
                self.rect.y += 1
            else:
                self.rect.y -= 1

        collisions = sprite.spritecollide(self, Enemies, False)

        for enemy in collisions:
            if enemy != self:
                if self.rect.x < enemy.rect.x:
                    self.rect.x -= 2
                    enemy.rect.x += 2
                else:
                    self.rect.x += 2
                    enemy.rect.x -= 2

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0


score = 0
lost = 0
lives = 3

#sozdanie npc i igroka

window = display.set_mode((win_width, win_height))
display.set_caption("Collecting Game")
background = transform.scale(image.load("Space.jpg"),(win_width, win_height))

rocket = Player("player.png", 5 ,win_height - 80, 80, 80, 2)

coins = sprite.Group()
for i in range(1, 6):
    coin = Collectables("Block.png", randint(80, win_width - 80), randint(0, 500),80, 80,  0  )
    coins.add(coin)

buffs = sprite.Group()
for i in range(1, 3):
    buff = Buff("Buff.png", randint(80, win_width - 80), randint(0, 500),80, 80,  0  )
    buffs.add(buff)

Enemies = sprite.Group()
for i in range(1, 6):
    enemy = Enemy("Enemy.png", randint(80, win_width - 80), randint(0, 700),80, 80, randint(1, 2)  )
    Enemies.add(enemy)

game = True
finish = False
clock = time.Clock()
FPS = 144

#zvuki puki

mixer.init()
mixer.music.load('CoralReef.mp3')
mixer.music.set_volume(0.3)
mixer.music.play()

coin_sound = mixer.Sound("coin.mp3")
buff_sfx = mixer.Sound("buff.mp3")
hurt_sfx = mixer.Sound("hurt.mp3")
lose_sfx = mixer.Sound("lose.mp3")
win_sfx = mixer.Sound("win.mp3")

#text


font.init()
font2 = font.SysFont("Comic Sans MS", 36)

win = font2.render("YOU WON!", 1, (0,255,0))
lose = font2.render("YOU LOSE!", 1, (255,10,10))

#cikl

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    last_time = timer()


    if finish != True:
        window.blit(background,(0,0))

        text_score = font2.render("SCORE:" + str(score), 1 , (255,255,255))
        window.blit(text_score, (10, 20)  )

        text_lives = font2.render("LIVES:" + str(lives), 1 , (0,255,0))
        window.blit(text_lives, (30, 60))

        rocket.reset()
        rocket.update()
        coins.update()
        coins.draw(window)
        Enemies.update()
        Enemies.draw(window)
        buffs.update()
        buffs.draw(window)


        collides = sprite.spritecollide(rocket, coins, True)

        for c in collides:
            score += 1
            coin = Collectables("Block.png", randint(80, win_width - 80), randint(0, 500),80, 80, 0  )
            coin.kill()
            coins.add(coin)
            coin_sound.set_volume(0.2)
            coin_sound.play()

        collides_enemy = sprite.spritecollide(rocket, Enemies, True)

        for e in collides_enemy:
            lives -= 1
            enemy = Enemy("Enemy.png",randint(80, win_width - 80),randint(0, 700),80, 80,randint(1, 2))
            Enemies.add(enemy)
            hurt_sfx.set_volume(0.2)
            hurt_sfx.play()
        
        collides_buff = sprite.spritecollide(rocket, buffs, True)

        for b in collides_buff:
            lives += 1
            buff = Buff("Buff.png",randint(80, win_width - 80),randint(0, 500),80,80,0)
            buff.kill()
            buffs.add(buff)
            buff_sfx.set_volume(0.2)
            buff_sfx.play()
            

        if score >= 15:
            finish = True
            window.blit(win, (675, 400))
            win_sfx.set_volume(0.2)
            win_sfx.play()

        if lives <= 0:
            finish = True
            window.blit(lose, (675, 400))
            lose_sfx.set_volume(0.2)
            lose_sfx.play()
    display.update()
    clock.tick(FPS)