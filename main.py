import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)

# Шрифты
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

# Звук (опционально)
pygame.mixer.init()
try:
    bounce_sound = pygame.mixer.Sound('bounce.wav')
    goal_sound = pygame.mixer.Sound('goal.wav')
except:
    print("Звуки не найдены — продолжаем без них")

# Ракетки
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PADDLE_SPEED = 7
COMPUTER_PADDLE_SPEED = 6

# Мяч
BALL_SIZE = 20
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Состояния игры
MENU = 0
PLAYING_PVP = 1
PLAYING_PVE = 2
game_state = MENU

# Вспомогательные функции
def gradient_surface(width, height, color1, color2):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    return surface

def create_starfield(num_stars=100):
    return [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.choice([1, 2])) for _ in range(num_stars)]

def draw_stars(stars, scroll_speed):
    for i, (x, y, size) in enumerate(stars):
        new_y = (y + scroll_speed) % HEIGHT
        stars[i] = (x, new_y, size)
        brightness = int(255 * (size / 2))
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, new_y), size)

# Объекты
player1_paddle_rect = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle_rect = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball_rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Поверхности для градиента и теней
paddle_gradient = gradient_surface(PADDLE_WIDTH, PADDLE_HEIGHT, (100, 200, 255), (0, 100, 255))
shadow = pygame.Surface((BALL_SIZE + 10, BALL_SIZE + 10), pygame.SRCALPHA)
pygame.draw.ellipse(shadow, (0, 0, 0, 50), (0, 0, *shadow.get_size()))

# Меню
selected = 0
menu_items = ["Играть против друга", "Играть против компьютера", "Выход"]
flash_text = ""

# Анимация мяча
pulse_angle = 0

# Звёзды
stars = create_starfield(100)


def reset_ball():
    ball_rect.center = (WIDTH // 2, HEIGHT // 2)
    speed_x = random.choice((-BALL_SPEED_X, BALL_SPEED_X))
    speed_y = random.choice((-BALL_SPEED_Y, BALL_SPEED_Y))
    return speed_x, speed_y


def computer_move():
    if player2_paddle_rect.centery < ball_rect.centery and player2_paddle_rect.bottom < HEIGHT:
        player2_paddle_rect.y += COMPUTER_PADDLE_SPEED
    elif player2_paddle_rect.centery > ball_rect.centery and player2_paddle_rect.top > 0:
        player2_paddle_rect.y -= COMPUTER_PADDLE_SPEED


def draw_menu():
    screen.fill(BLACK)
    draw_stars(stars, 0.5)

    title = font_large.render("PONG", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    for i, item in enumerate(menu_items):
        color = WHITE if selected == i else GRAY
        text = font_medium.render(item, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 300 + i * 50))

    # Курсор
    cursor = font_medium.render("▶", True, LIGHT_BLUE)
    screen.blit(cursor, (WIDTH // 2 - 200, 300 + selected * 50))

    pygame.display.flip()


def draw_game():
    screen.fill(BLACK)
    draw_stars(stars, 1)

    # Тень мяча
    shadow_pos = (ball_rect.centerx - shadow.get_width() // 2, ball_rect.centery - shadow.get_height() // 2 + 5)
    screen.blit(shadow, shadow_pos)

    # Градиентная ракетка
    screen.blit(paddle_gradient, player1_paddle_rect.topleft)
    screen.blit(paddle_gradient, player2_paddle_rect.topleft)

    # Мяч с анимацией пульсации
    global pulse_angle
    scale = 1 + 0.05 * math.sin(pulse_angle)
    scaled_ball = pygame.transform.smoothscale(ball_surf, (int(BALL_SIZE * scale), int(BALL_SIZE * scale)))
    ball_rect_scaled = scaled_ball.get_rect(center=ball_rect.center)
    screen.blit(scaled_ball, ball_rect_scaled.topleft)

    # Линия по центру
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Счёт
    score1 = font_small.render(f"{player1_score}", True, WHITE)
    score2 = font_small.render(f"{player2_score}", True, WHITE)
    screen.blit(score1, (WIDTH // 4 - score1.get_width() // 2, 20))
    screen.blit(score2, (3 * WIDTH // 4 - score2.get_width() // 2, 20))

    # Вспышка GOAL!
    if flash_text:
        flash = font_large.render(flash_text, True, (255, 255, 0))
        screen.blit(flash, (WIDTH // 2 - flash.get_width() // 2, HEIGHT // 2 - 50))

    pygame.display.flip()
    pulse_angle += 0.1


# Мяч как поверхность
ball_surf = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
pygame.draw.ellipse(ball_surf, WHITE, (0, 0, BALL_SIZE, BALL_SIZE))

# Игровые переменные
player1_score = 0
player2_score = 0
ball_speed_x, ball_speed_y = reset_ball()
flash_timer = 0

# Основной игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # PvP
                        game_state = PLAYING_PVP
                        player1_score = player2_score = 0
                        ball_speed_x, ball_speed_y = reset_ball()
                    elif selected == 1:  # PvE
                        game_state = PLAYING_PVE
                        player1_score = player2_score = 0
                        ball_speed_x, ball_speed_y = reset_ball()
                    elif selected == 2:  # Quit
                        running = False

            elif game_state in (PLAYING_PVP, PLAYING_PVE):
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU

    if game_state == MENU:
        draw_menu()

    elif game_state in (PLAYING_PVP, PLAYING_PVE):
        keys = pygame.key.get_pressed()

        # Игрок 1
        if keys[pygame.K_w] and player1_paddle_rect.top > 0:
            player1_paddle_rect.y -= PADDLE_SPEED
        if keys[pygame.K_s] and player1_paddle_rect.bottom < HEIGHT:
            player1_paddle_rect.y += PADDLE_SPEED

        # Игрок 2 или компьютер
        if game_state == PLAYING_PVP:
            if keys[pygame.K_UP] and player2_paddle_rect.top > 0:
                player2_paddle_rect.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and player2_paddle_rect.bottom < HEIGHT:
                player2_paddle_rect.y += PADDLE_SPEED
        else:
            computer_move()

        # Движение мяча
        ball_rect.x += ball_speed_x
        ball_rect.y += ball_speed_y

        # Отскок от стен
        if ball_rect.top <= 0 or ball_rect.bottom >= HEIGHT:
            ball_speed_y *= -1
            bounce_sound.play()

        # Отскок от ракеток
        if ball_rect.colliderect(player1_paddle_rect) or ball_rect.colliderect(player2_paddle_rect):
            ball_speed_x *= -1
            bounce_sound.play()

        # Гол
        if ball_rect.left <= 0:
            player2_score += 1
            flash_text = "GOAL!"
            flash_timer = 60
            goal_sound.play()
            ball_speed_x, ball_speed_y = reset_ball()

        if ball_rect.right >= WIDTH:
            player1_score += 1
            flash_text = "GOAL!"
            flash_timer = 60
            goal_sound.play()
            ball_speed_x, ball_speed_y = reset_ball()

        if flash_timer > 0:
            flash_timer -= 1
        else:
            flash_text = ""

        draw_game()

    clock.tick(60)

pygame.quit()
sys.exit()