import pygame
import random

pygame.init()

# Set up the window
window_width = 600
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Avoid the Objects")

# Set up the player
player_width = 50
player_height = 50
player_x = window_width // 2 - player_width // 2
player_y = window_height // 2 - player_height // 2
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
player_speed = 5

# Set up the obstacles
obstacle_width = 50
obstacle_height = 50
obstacle_min_y = 50
obstacle_max_y = window_height - obstacle_height - obstacle_min_y
obstacle_speed = 3
obstacle_list = []

# Set up the clock
clock = pygame.time.Clock()

# Set up the fonts
font_small = pygame.font.SysFont(None, 30)
font_large = pygame.font.SysFont(None, 50)

# Set up the colors
color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_red = (255, 0, 0)
color_green = (0, 255, 0)

def spawn_obstacle():
    obstacle_x = window_width
    obstacle_y = random.randint(obstacle_min_y, obstacle_max_y)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    obstacle_direction = random.choice([-1, 1])
    obstacle_list.append((obstacle_rect, obstacle_direction))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)

# Game loop
game_over = False
score = 0
while not game_over:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    # Spawn obstacles
    if random.random() < 0.02:
        spawn_obstacle()

    # Move obstacles
    for obstacle_rect, obstacle_direction in obstacle_list:
        obstacle_rect.x += obstacle_speed * obstacle_direction

        # Check for collision with player
        if player_rect.colliderect(obstacle_rect):
            game_over = True

        # Remove obstacles that have gone off screen
        if obstacle_rect.right < 0 or obstacle_rect.left > window_width:
            obstacle_list.remove((obstacle_rect, obstacle_direction))

    # Draw the screen
    window.fill(color_white)
    pygame.draw.rect(window, color_black, player_rect)
    for obstacle_rect, _ in obstacle_list:
        pygame.draw.rect(window, color_red, obstacle_rect)
    draw_text(f"Score: {score}", font_small, color_black, window_width // 2, 20)
    pygame.display.update()

    # Update the score
    score += 1

    # Limit the frame rate
    clock.tick(60)

# Game over screen
window.fill(color_white)
draw_text("Game Over")
