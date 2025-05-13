import pygame
import random

pygame.init()

# Screen setup
width, height = 600, 600
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Load forest background (grass tile)
grass_img = pygame.image.load("grass2.png")
grass_img = pygame.transform.scale(grass_img, (30, 30))

# Snake and food setup
snake_x, snake_y = width // 2, height // 2
change_x, change_y = 0, 0
food_x, food_y = random.randrange(0, width, 10), random.randrange(0, height, 10)
snake_body = [(snake_x, snake_y)]

# Fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 80)
score = 0
show_bite_message = False
bite_timer = 0

def display_score():
    shadow = font.render(f"Score: {score}", True, (0, 0, 0))
    game_screen.blit(shadow, [11, 11])
    score_text = font.render(f"Score: {score}", True, (0, 128, 255))
    game_screen.blit(score_text, [10, 10])

def show_game_over():
    over_text = font.render("GAME OVER!", True, (255, 0, 0))
    game_screen.blit(over_text, [width // 2 - 100, height // 2])
    pygame.display.update()
    pygame.time.wait(2000)
    quit()

def show_manual_game_over():
    global snake_x, snake_y, change_x, change_y, food_x, food_y, snake_body, score
    draw_background()
    game_over_text = large_font.render("GAME OVER", True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
    game_screen.blit(game_over_text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

    # Reset game state
    snake_x, snake_y = width // 2, height // 2
    change_x, change_y = 0, 0
    food_x, food_y = random.randrange(0, width, 10), random.randrange(0, height, 10)
    snake_body = [(snake_x, snake_y)]
    score = 0
    pygame.event.clear()  # Clear key events after reset

def draw_background():
    for x in range(0, width, 30):
        for y in range(0, height, 30):
            game_screen.blit(grass_img, (x, y))

def display_snake_and_food():
    global snake_x, snake_y, food_x, food_y, score, show_bite_message, bite_timer

    snake_x = (snake_x + change_x) % width
    snake_y = (snake_y + change_y) % height

    if (snake_x, snake_y) in snake_body[1:]:
        show_game_over()

    snake_body.append((snake_x, snake_y))

    if food_x == snake_x and food_y == snake_y:
        score += 1
        food_x, food_y = random.randrange(0, width, 10), random.randrange(0, height, 10)
        show_bite_message = True
        bite_timer = pygame.time.get_ticks()
    else:
        del snake_body[0]

    draw_background()

    # Draw food (orange circle)
    pygame.draw.circle(game_screen, (255, 165, 0), (food_x + 5, food_y + 5), 5)

    # Draw snake
    head_x, head_y = snake_body[-1]
    pygame.draw.ellipse(game_screen, (255, 0, 0), [head_x - 2, head_y - 2, 14, 14])
    pygame.draw.circle(game_screen, (0, 0, 0), (head_x + 4, head_y + 3), 2)
    pygame.draw.circle(game_screen, (0, 0, 0), (head_x + 8, head_y + 3), 2)

    for index, (x, y) in enumerate(snake_body[:-1]):
        color = (255, 0, 0) if index % 2 == 0 else (0, 0, 0)
        pygame.draw.circle(game_screen, color, (x + 5, y + 5), 5)

    display_score()

    if show_bite_message:
        if pygame.time.get_ticks() - bite_timer < 500:
            bite_text = small_font.render("CHOMP!", True, (255, 140, 0))
            game_screen.blit(bite_text, (food_x - 10, food_y - 15))
        else:
            show_bite_message = False

    pygame.display.update()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and change_x == 0:
                change_x = -10
                change_y = 0
            elif event.key == pygame.K_RIGHT and change_x == 0:
                change_x = 10
                change_y = 0
            elif event.key == pygame.K_UP and change_y == 0:
                change_x = 0
                change_y = -10
            elif event.key == pygame.K_DOWN and change_y == 0:
                change_x = 0
                change_y = 10
            elif event.key == pygame.K_RETURN:
                show_manual_game_over()

    display_snake_and_food()
    clock.tick(12)
