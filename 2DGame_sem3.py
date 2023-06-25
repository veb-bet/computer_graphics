import pygame
import random
# Инициализация Pygame
pygame.init()

# Окно игры
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Многоуровневая игра")

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Шрифты
font = pygame.font.Font('freesansbold.ttf', 32)

# Количество злодеев на каждом уровне
levels = [1, 2, 3, 4, 5]

# Загрузка изображений
player_img = pygame.Surface((30, 30))
player_img.fill(green)
enemy_img = pygame.Surface((30, 30))
enemy_img.fill(red)
bullet_img = pygame.Surface((10, 10))
bullet_img.fill(black)
circle_img = pygame.Surface((20, 20))
circle_img.fill(green)
block_img = pygame.Surface((30, 30))
block_img.fill(black)

# Классы
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = block_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = circle_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.speed = 5
        self.bullet_cooldown = 0

    def set_speed(self, speed):
        self.speed = speed

    def update(self, blocks, circles):
        # Обработка движения игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if pygame.sprite.spritecollide(self, blocks, False):
                self.rect.x += self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if pygame.sprite.spritecollide(self, blocks, False):
                self.rect.x -= self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            if pygame.sprite.spritecollide(self, blocks, False):
                self.rect.y += self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            if pygame.sprite.spritecollide(self, blocks, False):
                self.rect.y -= self.speed

        # Обработка выстрела игрока
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1
        if keys[pygame.K_SPACE] and self.bullet_cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.rect.x, self.rect.y)
            #all_sprites.add(bullet)
            #bullets.add(bullet)
            self.bullet_cooldown = 10

        # Обработка сбора кругов игроком
        circle_collected = pygame.sprite.spritecollide(self, circles, True)
        if circle_collected:
            # Круг был собран
            you_win()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed =1
        self.direction = "right"
        self.bullet_cooldown = 0

    def update(self, blocks, player):
        # Обработка движения врага
        if self.direction == "right":
            self.rect.x += self.speed
            if pygame.sprite.spritecollide(self, blocks, False):
                self.rect.x -= self.speed
                self.direction = "down"
        elif self.direction == "down":
            self.rect.y += self.speed
            if pygame.sprite.spritecollide(self, blocks, False):
                self.rect.y -= self.speed
                self.direction = "left"
        elif self.direction == "left":
            self.rect.x -= self.speed
            if pygame.sprite.spritecollide(self, blocks, False):
                self.rect.x += self.speed
                self.direction = "up"
        elif self.direction == "up":
            self.rect.y -= self.speed
            if pygame.sprite.spritecollide(self, blocks, False):
                self.rect.y += self.speed
                self.direction = "right"

        # Обработка выстрела врага
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1
        bullet_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for direction in bullet_directions:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.rect.x, self.rect.y, direction, False)
            if pygame.sprite.spritecollide(bullet, blocks, False):
                continue
            if pygame.sprite.collide_rect(bullet, player):
                player.kill()
                game_over()
            #all_sprites.add(bullet)
            #bullets.add(bullet)
            self.bullet_cooldown = 10
            break

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, start_x, start_y, direction=(0, -1), player=True):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.direction = direction
        self.player = player
        self.start_x = start_x
        self.start_y = start_y

    def update(self, blocks, enemies, player):
        # Обработка движения пули
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Обработка столкновения пули с блоками
        if pygame.sprite.spritecollide(self, blocks, False):
            self.kill()

        # Обработка столкновения пули с врагами
        if self.player:
            enemy = pygame.sprite.spritecollideany(self, enemies)
            if enemy:
                enemy.kill()
                self.kill()
                if len(enemies) == 0:
                    you_win()

        # Обработка столкновения пули с игроком
        if not self.player and pygame.sprite.collide_rect(self, player):
            player.kill()
            game_over()

        # Обработка выхода пули за границы экрана
        if self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height:
            self.kill()

# Функции
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def game_over():
    draw_text("Game Over", font, black, screen_width // 2, screen_height // 2)
    pygame.display.update()
    pygame.time.delay(2000)
    main_menu()

def you_win():
    draw_text("You Win!", font, black, screen_width // 2, screen_height // 2)
    pygame.display.update()
    pygame.time.delay(2000)
    main_menu()

def main_menu():
    running = True
    while running:
        screen.fill(white)
        draw_text("Главное Меню", font, black, screen_width // 2, 100)

        # Отображение кнопок уровней
        level_buttons = []
        for i, level in enumerate(levels):
            button_text = "Уровень " + str(i + 1)
            button_width = 200
            button_height = 50
            button_x = screen_width // 2 - button_width // 2
            button_y = 200 + i * (button_height + 10)
            level_buttons.append(pygame.Rect(button_x, button_y, button_width, button_height))
            pygame.draw.rect(screen, black, level_buttons[i])
            draw_text(button_text, font, white, button_x + button_width // 2, button_y + button_height // 2)

        # Обработка нажатия на кнопки уровней
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                for i, button in enumerate(level_buttons):
                    if button.collidepoint(pygame.mouse.get_pos()):
                        running = False
                        game_loop(levels[i])

        pygame.display.update()

def game_loop(num_enemies):
    # Создание спрайтов и групп
    player = Player()
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    circles = pygame.sprite.Group()
    all_sprites.add(player)

    # Создание блоков
    for i in range(screen_width // 30):
        block1 = Block(i * 30, 0)
        blocks.add(block1)
        all_sprites.add(block1)
        block2 = Block(i * 30, screen_height - 30)
        blocks.add(block2)
        all_sprites.add(block2)
    for i in range(1, (screen_height - 30) // 30):
        block1 = Block(0, i * 30)
        blocks.add(block1)
        all_sprites.add(block1)
        block2 = Block(screen_width - 30, i * 30)
        blocks.add(block2)
        all_sprites.add(block2)
    for i in range(10):  # Количество случайных блоков
        x = random.randint(60, screen_width - 90)  # Координата x в пределах игровой области
        y = random.randint(60, screen_height - 90)  # Координата y в пределах игровой области
        block = Block(x, y)
        blocks.add(block)
        all_sprites.add(block)

    # Создание злодеев
    enemy_x = [screen_width // (num_enemies + 1) * (i + 1) for i in range(num_enemies)]
    enemy_y = [screen_height // (num_enemies + 1) * (i + 1) for i in range(num_enemies)]
    for x, y in zip(enemy_x, enemy_y):
        enemy = Enemy(x, y)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Создание круга
    circle_x = screen_width // 2
    circle_y = screen_height // 2
    circle = Circle(circle_x, circle_y)
    all_sprites.add(circle)
    circles.add(circle)

    # Игровой цикл
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Обновление спрайтов
        bullets.update(blocks, enemies, player)
        player.update(blocks, circles)
        for enemy in enemies:
            enemy.update(blocks, player)

        # Отрисовка
        screen.fill(white)
        all_sprites.draw(screen)
        pygame.display.update()

# Запуск игры
main_menu()