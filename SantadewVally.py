import pygame

from player import Player

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player = Player(10,10)
    player.update()
    player.render(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()