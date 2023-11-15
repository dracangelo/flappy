import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
GRAVITY = 1
BIRD_JUMP = -15
PIPE_WIDTH = 50
PIPE_HEIGHT = 300
GAP = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_image = pygame.image.load("bird.png")
pipe_image = pygame.image.load("piptop.png")

# Resize images
bird_image = pygame.transform.scale(bird_image, (50, 50))
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))

# Clock to control the frame rate
clock = pygame.time.Clock()

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Check if the bird hits the ground
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

        # Check if the bird hits the top
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0

    def jump(self):
        self.velocity = BIRD_JUMP

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.height = random.randint(100, PIPE_HEIGHT)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height - GAP)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.height = random.randint(100, PIPE_HEIGHT)
            self.rect.y = random.randint(0, HEIGHT - self.rect.height - GAP)

# Create sprite groups
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# Create bird
bird = Bird()
all_sprites.add(bird)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    # Update
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.spritecollide(bird, pipes, False)
    if hits:
        running = False

    # Generate pipes
    if random.randint(0, 100) < 2:
        pipe = Pipe(WIDTH)
        all_sprites.add(pipe)
        pipes.add(pipe)

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Refresh screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
