import pygame
import cv2
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Assets
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 40
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 40
BULLET_WIDTH, BULLET_HEIGHT = 5, 15

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(random.randint(0, WIDTH - ENEMY_WIDTH), -ENEMY_HEIGHT))
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Function to play the video
def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Resize frame to match screen dimensions
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        # Convert frame to RGB for Pygame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Transpose to fix rotation if needed
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        # Display the frame
        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()
        # Allow exiting during the video playback
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()
        clock.tick(90)  # Adjust playback speed
    cap.release()

# Initialize player, enemies, and bullets
player = Player()
player_group = pygame.sprite.GroupSingle(player)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Score and health
score = 0
health = 3

# Play the video before starting the game
video_path = "space.mp4"
play_video(video_path)

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()

    # Spawn enemies
    if random.random() < 0.02:  # Adjust spawn rate
        enemy = Enemy()
        enemies.add(enemy)

    # Update
    player_group.update()
    enemies.update()
    bullets.update()

    # Check collisions
    for bullet in bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
        if hit_enemies:
            score += len(hit_enemies)
            bullet.kill()

    if pygame.sprite.spritecollide(player, enemies, True):
        health -= 1
        if health <= 0:
            print(f"Game Over! Final Score: {score}")
            running = False

    # Draw everything
    player_group.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)

    # Display score and health
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(f"Health: {health}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
