import pygame
import sys
import random
import time
# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
DARK = (30, 30, 30)
RED = (200, 50, 50)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RAT")
clock = pygame.time.Clock()

# Game variables
direction = "up"
speed = 5
HIT = 0

# Difficulty variables
obstacle_speed = 3  # Initial obstacle speed
min_gap = 170  # Minimum space between obstacles (decreases over time)
max_gap = 250  # Maximum space (for initial easier levels)
min_spawn_time = 50   # Minimum possible spawn time
max_spawn_time = 100  # Initial spawn time (decreases over time)
spawn_timer = random.randint(min_spawn_time, max_spawn_time)
SCORE = 0
frame_count = 0  # Track time to increase difficulty
def play_again():
    global obstacle_speed, HIT, SCORE
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_just_released()
        if keys[pygame.K_SPACE]:
            running = False
            obstacle_speed = 3
            HIT = 0
            SCORE = 0
        font = pygame.font.Font(None, 32)
        text = font.render(f"Game Over! Press Space to play again", True, WHITE)
        

        screen.fill(DARK)
        screen.blit(text, (WIDTH//2-200, HEIGHT//2))
        pygame.display.flip()
        clock.tick(60)
        



class Rat():
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.size = 10
        self.color = WHITE

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    def move(self):
        global direction
        if direction == "up":
            self.y -= speed
        elif direction == "down":
            self.y += speed

    def check_collision(self, obstacles):
        global HIT
        # Check boundary collision
        if self.y - self.size <= 0 or self.y + self.size >= HEIGHT:
            self.y = HEIGHT / 2
            HIT += 1
            return True

        # Check obstacle collision
        for obstacle in obstacles:
            if (obstacle.x < self.x + self.size and 
                obstacle.x + obstacle.width > self.x - self.size and 
                (self.y - self.size < obstacle.top_height or self.y + self.size > HEIGHT - obstacle.bottom_height)):
                if not obstacle.to_remove:  # Prevent multiple hits
                    obstacle.remove()
                    HIT += 1  # Increase hit count only once
                return True
        return False

def toggle_direction():
    global direction
    direction = "down" if direction == "up" else "up"

class Obstacle():
    def __init__(self):
        self.x = WIDTH
        self.width = 40
        self.color = RED
        self.gap_size = random.randint(min_gap, max_gap)  # Gap size reduces over time
        self.gap_y = random.randint(150, HEIGHT - 150)  # Randomized gap position
        self.top_height = self.gap_y - (self.gap_size // 2)
        self.bottom_height = HEIGHT - (self.gap_y + (self.gap_size // 2))
        self.to_remove = False  # Initialize the flag

    def move(self):
        self.x -= obstacle_speed  # Speed increases over time

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, self.color, (self.x, HEIGHT - self.bottom_height, self.width, self.bottom_height))

    def is_off_screen(self):
        return self.x + self.width < 0

    def remove(self):
        """Mark this obstacle for removal."""
        self.to_remove = True

# Initialize game objects
rat = Rat()
obstacles = []
path = []
initial_x = WIDTH // 2
path.append((initial_x, HEIGHT // 2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    keys = pygame.key.get_just_released()
    if keys[pygame.K_SPACE]:
        toggle_direction()
        path.append((initial_x, rat.y))

    # Update game state
    rat.move()

    # Check collision
    if rat.check_collision(obstacles):
        if HIT > 5:
            play_again()

    # Spawn new obstacles at random intervals
    if frame_count >= spawn_timer:
        obstacles.append(Obstacle())
        frame_count = 0
        spawn_timer = random.randint(min_spawn_time, max(max_spawn_time, min_spawn_time))


    # Move and remove off-screen obstacles or those marked for removal
    for obstacle in obstacles[:]:
        obstacle.move()
        if obstacle.is_off_screen() or obstacle.to_remove:  # Now checking `to_remove`
            obstacles.remove(obstacle)

    # **Difficulty Scaling Over Time**
    if frame_count % 300 == 0:  # Every 5 seconds (assuming 60 FPS)
        obstacle_speed += 0.05 # Obstacles move faster
        max_spawn_time = max(40, max_spawn_time - 5)  # Reduce max spawn interval
        min_gap = max(80, min_gap - 5)  # Reduce gap size for increased difficulty

    # Clear screen
    screen.fill(DARK)

    # Draw elements
    rat.draw()
    for obstacle in obstacles:
        obstacle.draw()

    # Display stats
    SCORE = int(obstacle_speed*100-300)+1
    font = pygame.font.Font(None, 32)
    text = font.render(f"SCORE: {SCORE}", True, WHITE)
    screen.blit(text, (100, 10))
    text = font.render(f"Hit: {HIT}", True, WHITE)
    screen.blit(text, (100, 40))
    
    

    # Update display
    pygame.display.flip()
    clock.tick(60)
    frame_count += 1  # Increase frame count

pygame.quit()
sys.exit()
