import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders Clone")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Player
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5
player_color = blue

# Bullet
bullet_width = 4
bullet_height = 10
bullet_speed = 30  # Increased bullet speed for responsiveness
max_bullets = 5  # Maximum number of bullets on screen at a time
bullet_color = red
bullets = []

# Enemy
enemy_width = 50
enemy_height = 50
enemy_speed = 2
enemies = []

# Game variables
max_lives = 5
lives = max_lives
score = 0

font = pygame.font.Font(None, 36)

# Terminal updates
def print_terminal(message):
    print("[INFO]:", message)

# Game loop
clock = pygame.time.Clock()
running = True
menu = True
game_over = False

while running:
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
                    print_terminal("Game started")

        screen.fill(black)
        title_text = font.render("Space Invaders Clone", True, white)
        play_text = font.render("Press SPACE to play", True, white)
        color_text = font.render("Press R for Red ship, B for Blue ship", True, white)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
        screen.blit(play_text, (screen_width // 2 - play_text.get_width() // 2, 300))
        screen.blit(color_text, (screen_width // 2 - color_text.get_width() // 2, 350))
        pygame.display.update()

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    lives = max_lives
                    score = 0
                    enemies.clear()
                    print_terminal("Game restarted")
                if event.key == pygame.K_q:
                    game_over = False
                    running = False

        screen.fill(black)
        game_over_text = font.render("Game Over", True, white)
        retry_text = font.render("Press R to retry", True, white)
        exit_text = font.render("Press Q to exit", True, white)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, 300))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, 350))
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
        print_terminal("Ship moved right")
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
        print_terminal("Ship moved up")
    if keys[pygame.K_DOWN] and player_y < screen_height - player_height:
        player_y += player_speed
        print_terminal("Ship moved down")
    if keys[pygame.K_SPACE] and len(bullets) < max_bullets:
        bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])
        print_terminal("Bullet fired")

   # Bullet movement
    for bullet in bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Spawn new enemies if there are fewer than 6
    while len(enemies) < 6:
        enemies.append([random.randint(0, screen_width - enemy_width), random.randint(0, screen_height // 2)])

    # Enemy movement and collision detection
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > screen_height:
            enemies.remove(enemy)
        if (player_x < enemy[0] + enemy_width and
                player_x + player_width > enemy[0] and
                player_y < enemy[1] + enemy_height and
                player_y + player_height > enemy[1]):
            enemies.remove(enemy)
            lives -= 1
            print_terminal("Player hit by enemy!")

        for bullet in bullets:
            if (enemy[0] < bullet[0] < enemy[0] + enemy_width and
                    enemy[1] < bullet[1] < enemy[1] + enemy_height):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10
                print_terminal("Enemy destroyed!")

    if lives <= 0:
        game_over = True
        print_terminal("Game over - Lives exhausted")

    # Draw everything
    screen.fill(black)
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, (bullet[0], bullet[1], bullet_width, bullet_height))
    for enemy in enemies:
        pygame.draw.rect(screen, green, (enemy[0], enemy[1], enemy_width, enemy_height))

    # Draw lives and score
    lives_text = font.render(f"Lives: {lives}", True, white)
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (10, 40))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
