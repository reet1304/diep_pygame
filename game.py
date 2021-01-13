import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Sema Game")
x = 50
y = 50
width = 40
height = 60
speed = 5
run = True
snake_body = [[100, 50], [90, 50], [80, 50]]
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x = x - speed
    if keys[pygame.K_RIGHT]:
        x = x + speed
    if keys[pygame.K_UP]:
        y = y - speed
    if keys[pygame.K_DOWN]:
        y = y + speed
    win.fill((0,0,0))
    pygame.draw.rect(win, (0, 0, 255), (x, y, width, height))
    pygame.display.update()
pygame.quit()
