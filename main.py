import pygame
from pygame import mixer
import os
from fighter import Fighter

# Initialize Pygame and mixer
mixer.init()
pygame.init()

# Set the base directory (assuming the assets folder is in the same directory as the script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # Player scores [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load music and sounds with dynamic paths
mixer.music.load(os.path.join(BASE_DIR, "assets/audio/music.mp3"))
mixer.music.set_volume(0.5)
mixer.music.play(-1, 0.0, 5000)

sword_fx = mixer.Sound(os.path.join(BASE_DIR, "assets/audio/sword.wav"))
sword_fx.set_volume(0.5)

magic_fx = mixer.Sound(os.path.join(BASE_DIR, "assets/audio/magic.wav"))
magic_fx.set_volume(0.75)

# Load background image
bg_image = pygame.image.load(os.path.join(BASE_DIR, "assets/images/background/background.jpg")).convert_alpha()

# Load spritesheets
warrior_sheet = pygame.image.load(os.path.join(BASE_DIR, "assets/images/warrior/Sprites/warrior.png")).convert_alpha()
wizard_sheet = pygame.image.load(os.path.join(BASE_DIR, "assets/images/wizard/Sprites/wizard.png")).convert_alpha()

# Load victory image
victory_img = pygame.image.load(os.path.join(BASE_DIR, "assets/images/icons/victory.png")).convert_alpha()

# Define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Define fonts
count_font = pygame.font.Font(os.path.join(BASE_DIR, "assets/fonts/turok.ttf"), 80)
score_font = pygame.font.Font(os.path.join(BASE_DIR, "assets/fonts/turok.ttf"), 30)

# Function to draw text
def draw_text(text, font, text_col, x, y, center=False):
    img = font.render(text, True, text_col)
    if center:
        x -= img.get_width() // 2
    screen.blit(img, (x, y))

# Function to draw background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Function to draw fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# Game loop
run = True
while run:

    clock.tick(FPS)

    # Draw background
    draw_bg()

    # Show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text(f"P1: {score[0]}", score_font, RED, 20, 60)
    draw_text(f"P2: {score[1]}", score_font, RED, 580, 60)

    # Update countdown
    if intro_count <= 0:
        # Move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # Display count timer (centered)
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, center=True)
        # Update count timer
        if pygame.time.get_ticks() - last_count_update >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # Update fighters
    fighter_1.update()
    fighter_2.update()

    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Check for player defeat
    if not round_over:
        if not fighter_1.alive:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif not fighter_2.alive:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # Display victory image
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # play attack handing
    key = pygame.key.get_pressed()
    if not round_over:
        if key[pygame.K_r]:
            fighter_1.attack(fighter_2)
        if key[pygame.K_KP1]:
            fighter_2.attack(fighter_1)
    # Update display
    pygame.display.update()

# Exit pygame
pygame.quit()