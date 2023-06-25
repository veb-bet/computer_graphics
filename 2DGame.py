import pygame
import sys
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
pygame.init()
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Invaders')
player = pygame.Rect(525, 650, 50, 50)
enemy1 = pygame.Rect(525, 50, 30, 30)
enemy2 = pygame.Rect(300, 50, 30, 30)
ENEMY_SPEED = 1
bullet = None  # Player's bullet
enemy1_bullet = None  # Enemy 1's bullet
enemy2_bullet = None  # Enemy 2's bullet
BULLET_SPEED = 5
ENEMY_BULLET_SPEED = 1
ENEMY_FIRE_RATE = 60  # Number of frames between enemy shots
enemy1_fire_counter = 0  # Counter for enemy 1 firing rate
enemy2_fire_counter = 0  # Counter for enemy 2 firing rate
enemy1_hits = 0  # Counter for how many times player hit enemy 1
enemy2_hits = 0  # Counter for how many times player hit enemy 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not bullet: bullet = pygame.Rect(player.centerx, player.top, 5, 10)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.x -= 5
    if keys[pygame.K_RIGHT]: player.x += 5
    # Bullet movement
    if bullet:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0: bullet = None
    enemy1.x += ENEMY_SPEED
    if enemy1.x > WINDOW_WIDTH - enemy1.width or enemy1.x < 0:
        ENEMY_SPEED *= -1
        enemy1.y += enemy1.height
    if enemy1.y >= player.y: print('Game Over')
    if not enemy1_bullet and enemy1_fire_counter >= ENEMY_FIRE_RATE:
        enemy1_bullet = pygame.Rect(enemy1.centerx, enemy1.bottom, 5, 10)
        enemy1_fire_counter = 0
    elif enemy1_fire_counter < ENEMY_FIRE_RATE: enemy1_fire_counter += 1
    enemy2.x += ENEMY_SPEED * -1
    if enemy2.x > WINDOW_WIDTH - enemy2.width or enemy2.x < 0:
        ENEMY_SPEED *= -1
        enemy2.y += enemy2.height
    if enemy2.y >= player.y: print('Game Over')
    if not enemy2_bullet and enemy2_fire_counter >= ENEMY_FIRE_RATE:
        enemy2_bullet = pygame.Rect(enemy2.centerx, enemy2.bottom, 5, 10)
        enemy2_fire_counter = 0
    elif enemy2_fire_counter < ENEMY_FIRE_RATE: enemy2_fire_counter += 1
    if player.colliderect(enemy1): print('Collision with Enemy 1!')
    if player.colliderect(enemy2): print('Collision with Enemy 2!')
    if bullet and bullet.colliderect(enemy1):
        print('Enemy 1 hit!')
        enemy1_hits += 1
        bullet = None
        if enemy1_hits == 3: print('Player wins!')
    if bullet and bullet.colliderect(enemy2):
        print('Enemy 2 hit!')
        enemy2_hits += 1
        bullet = None
        if enemy2_hits == 3: print('Player wins!')
    if enemy1_bullet and enemy1_bullet.colliderect(player):
        print('Player hit by Enemy 1!')
        enemy1_bullet = None
    if enemy2_bullet and enemy2_bullet.colliderect(player):
        print('Player hit by Enemy 2!')
        enemy2_bullet = None
    background_image = pygame.image.load('background.png')
    game_window.blit(background_image, (0, 0))
    pygame.draw.polygon(game_window, WHITE,
                        [(player.x, player.y + player.height), (player.x + player.width / 2, player.y),
                         (player.x + player.width, player.y + player.height)])
    pygame.draw.circle(game_window, GREEN, (enemy1.x + enemy1.width / 2, enemy1.y + enemy1.height / 2), enemy1.width / 2)
    pygame.draw.circle(game_window, PURPLE, (enemy2.x + enemy2.width / 2, enemy2.y + enemy2.height / 2), enemy2.width / 2)
    if bullet: pygame.draw.rect(game_window, WHITE, bullet)
    if enemy1_bullet: pygame.draw.rect(game_window, WHITE, enemy1_bullet)
    if enemy2_bullet: pygame.draw.rect(game_window, WHITE, enemy2_bullet)
    if enemy1_bullet:
        enemy1_bullet.y += ENEMY_BULLET_SPEED
        if enemy1_bullet.y > WINDOW_HEIGHT:
            enemy1_bullet = None
    if enemy2_bullet:
        enemy2_bullet.y += ENEMY_BULLET_SPEED
        if enemy2_bullet.y > WINDOW_HEIGHT: enemy2_bullet = None
    pygame.display.update()