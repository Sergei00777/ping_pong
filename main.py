import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ракетки
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
paddle_speed = 7

# Ракетка игрока 1 (левая)
player1_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
# Ракетка игрока 2 (правая)
player2_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Мяч
BALL_SIZE = 15
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x, ball_speed_y = 5, 5

# Счёт
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 36)

# Основной игровой цикл
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление ракетками
    keys = pygame.key.get_pressed()

    # Игрок 1 (W/S)
    if keys[pygame.K_w] and player1_paddle.top > 0:
        player1_paddle.y -= paddle_speed
    if keys[pygame.K_s] and player1_paddle.bottom < HEIGHT:
        player1_paddle.y += paddle_speed

    # Игрок 2 (↑/↓)
    if keys[pygame.K_UP] and player2_paddle.top > 0:
        player2_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and player2_paddle.bottom < HEIGHT:
        player2_paddle.y += paddle_speed

    # Движение мяча
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Отскок мяча от стен
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Отскок от ракеток
    if ball.colliderect(player1_paddle) or ball.colliderect(player2_paddle):
        ball_speed_x *= -1

    # Гол (если мяч ушёл за границы)
    if ball.left <= 0:
        player2_score += 1
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2
        ball_speed_x *= -1  # Меняем направление

    if ball.right >= WIDTH:
        player1_score += 1
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2
        ball_speed_x *= -1

    # Отрисовка
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player1_paddle)
    pygame.draw.rect(screen, WHITE, player2_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Отображение счёта
    player1_text = font.render(f"{player1_score}", True, WHITE)
    player2_text = font.render(f"{player2_score}", True, WHITE)
    screen.blit(player1_text, (WIDTH // 4, 20))
    screen.blit(player2_text, (3 * WIDTH // 4, 20))

    pygame.display.flip()
    clock.tick(60)  # 60 FPS