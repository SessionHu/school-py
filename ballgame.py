import pygame
import random
import sys

class Ball(pygame.sprite.Sprite):

    def __init__(self, image, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        if self.rect.x == 0 and self.rect.y == 0:
            self.rect.x = random.randint(0, screen.get_width() - self.rect.width)
            self.rect.y = random.randint(0, screen.get_height() - self.rect.height)
        self.screen = screen
        self.v = [random.randint(-8, 8), random.randint(-8, 8)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args, **kwargs):
        self.rect.move_ip(self.v[0], self.v[1])
        # bounce off walls
        if self.rect.left < 0:
            self.v[0] *= -1
            self.rect.left = 0
        elif self.rect.left > self.screen.get_width() - self.rect.width:
            self.v[0] *= -1
            self.rect.left = self.screen.get_width() - self.rect.width
        if self.rect.top < 0:
            self.v[1] *= -1
            self.rect.top = 0
        elif self.rect.top > self.screen.get_height() - self.rect.height:
            self.v[1] *= -1
            self.rect.top = self.screen.get_height() - self.rect.height

    def inrange(self, abspos):
        relpos = (abspos[0] - self.rect.left, abspos[1] - self.rect.top)
        if 0 <= relpos[0] < self.rect.width and 0 <= relpos[1] < self.rect.height:
            return self.mask.get_at(relpos) == 1
        else:
            return False

pygame.init()

ballimg = pygame.image.load('./ball.gif')

pygame.display.set_icon(ballimg)
pygame.display.set_caption('SessTester')
screen = pygame.display.set_mode((800, 600))

fontslist = ['JetBrains Mono', 'Consolas', 'Arial']
fontmono = pygame.font.SysFont(fontslist, 16)

ball = Ball(ballimg, screen)
group = pygame.sprite.Group(ball)

score = 0

clock = pygame.time.Clock()
isrunning = True
isexit = False

while True:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isexit = True
    if isexit:
        break
    elif not isrunning:
        continue
    # update score
    if ball.inrange(pygame.mouse.get_pos()):
        score += .2
    else:
        score -= .1
    # update difficulty
    if score > 0 and int(score) % 10 == 0:
        if abs(ball.v[0]) < abs(ball.v[1]):
            ball.v[0] += 1
        else:
            ball.v[1] += 1
    elif score < 0:
        if ball.v[0] > 1:
            ball.v[0] -= 1
        elif ball.v[0] < -1:
            ball.v[0] += 1
        if ball.v[1] > 1:
            ball.v[1] -= 1
        elif ball.v[1] < -1:
            ball.v[1] += 1
    # check gameover
    if score < -101:
        print('Game over')
        pygame.display.set_caption('SessTester - Game over')
        bigmono = pygame.font.SysFont(fontslist, 48)
        sf = bigmono.render('Game over', True, (0, 0, 0))
        screen.blit(sf, (screen.get_width() // 2 - sf.get_width() // 2, screen.get_height() // 2 - sf.get_height() // 2))
        pygame.display.flip()
        isrunning = False
        continue
    # update ball
    group.update()
    # render
    screen.fill('#66ccff')
    scorestr = f'Score: {int(score)}'
    screen.blit(fontmono.render(scorestr, True, (0, 0, 0)), (10, 10))
    pygame.display.set_caption(f'SessTester - {scorestr}')
    # print(scorestr)
    group.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
