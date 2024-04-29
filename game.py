import pygame
import sys
import random

# Constants
width, height = 800, 600
ball_radius = 20
platform_width, platform_height = 100, 10
fps = 60
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
orange = (255, 165, 0)
light_blue = (173, 216, 230)

# Initialize Pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((width, height))  # Creates the window
pygame.display.set_caption("Bouncing Ball Game")   # Sets the title of the window
font = pygame.font.Font(None, 36)       # Initializes a font object for rendering text

# Clock for controlling the frame rate
clock = pygame.time.Clock()     # Creates a clock object to control the frame rate

# Initalize variables for the game
ball_pos = [width//2, height//2]    # Initializing that starting point of the ball
ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]   # Initializing the start speed of the ball with random values
platform_pos = [width//2 - platform_width//2, height - platform_height-10]  # Initializes the starting position och the platform
platform_speed = 10  # The speed of the platform movement
score = 0   # The player's score
lives = 3   # The lives of the player
current_level = 1   # The current level of the game
platform_color = orange  # Platform color


# Functions
def start_screen():
    screen.fill(black)
    show_text_on_screen("Bouncing Ball Game", 50, height//4)
    show_text_on_screen("Press any key to start...", 30, height//3)
    show_text_on_screen("Move the platform with arrow keys...", 30, height//2)
    pygame.display.flip()
    wait_for_key()


def game_over_screen():
    screen.fill(black)
    show_text_on_screen("Game Over", 50, height//3)
    show_text_on_screen(f"Your final score: {score}", 30, height // 2)
    show_text_on_screen("Press any key to restart...", 20, height * 2 // 3)
    pygame.display.flip()
    wait_for_key()


def victory_screen():
    screen.fill(black)
    show_text_on_screen("Congratulations", 50, height//3)
    show_text_on_screen(f"You've won with a score of {score}", 30, height//2)
    show_text_on_screen("Press any key to exit...", 20, height*2//3)
    pygame.display.flip()
    wait_for_key()


def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False


def show_text_on_screen(text, font_size, y_position):
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, white)
    text_rect = text_render.get_rect(center=(width//2, y_position))
    screen.blit(text_render, text_rect)


def change_platform_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


# Main game
start_screen()
game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()

    # Move platform
    platform_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
    platform_pos[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * platform_speed

    # Ensure that the platform stays within the screen boundaries
    platform_pos[0] = max(0, min(platform_pos[0], width - platform_width))
    platform_pos[1] = max(0, min(platform_pos[1], height - platform_height))

    # Move the ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Bounce of the walls
    if ball_pos[0] <= 0 or ball_pos[0] >= width:
        ball_speed[0] = -ball_speed[0]

    if ball_pos[1] <= 0:
        ball_speed[1] = ball_speed[1]

    # Check if the ball hits the platform
    if (
        platform_pos[0] <= ball_pos[0] <= platform_pos[0] + platform_width
            and platform_pos[1] <= ball_pos[1] <= platform_pos[1] + platform_height
    ):
        ball_speed[1] = -ball_speed[1]
        score += 1

    # Check if player advances to the next level
    if score >= current_level * 10:
        current_level += 1
        ball_pos = [width//2, height//2]
        ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]  # Randomize ball speed
        platform_color = change_platform_color()

    # Check if ball falls of the screen
    if ball_pos[1] >= height:
        # Decrease lives
        lives -= 1
        if lives == 0:
            game_over_screen()
            start_screen()  # Restart the game after game over
            score = 0
            lives = 3
            current_level = 1
        else:
            # Reset the ball position
            ball_pos = [width//2, height//2]
            # Randomize ball speed
            ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]

    # Clear the screen
    screen.fill(black)

    # Draw the ball
    pygame.draw.circle(screen, white, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Draw the platform
    pygame.draw.rect(screen, platform_color, (int(platform_pos[0]), int(platform_pos[1]), platform_width, platform_height))

    # Display information
    info_line_y = 10
    info_spacing = 75

    # Draw the score in an orange rectangle at the top left
    score_text = font.render(f"Score: {score}", True, white)
    score_rect = score_text.get_rect(topleft=(10, info_line_y))
    pygame.draw.rect(screen, orange, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)

    # Draw the level indicator in a light-blue rectangle at the top left (next to the score)
    level_text = font.render(f"Level: {current_level}", True, white)
    level_rect = level_text.get_rect(topleft=(score_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, light_blue, level_rect.inflate(10, 5))
    screen.blit(level_text, level_rect)

    # Draw the lives in a red rectangle at the top left (next to the level)
    lives_text = font.render(f"Lives: {lives}", True, white)
    lives_rect = lives_text.get_rect(topleft=(level_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, red, lives_rect.inflate(10, 5))
    screen.blit(lives_text, lives_rect)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()