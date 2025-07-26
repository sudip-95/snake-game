import pygame
import random
import time

# Initialize pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SU_Dip GAMES: Snake Game")
clock = pygame.time.Clock()


def draw_grid():
    """Draw grid lines for better visibility"""
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))


def game_over_screen(score):
    """Display game over screen"""
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 48)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    restart_text = font.render("Press R to restart or Q to quit", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return False
    return True


def main():
    """Main game function"""
    running = True

    while running:
        # Initialize game state
        snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        direction = RIGHT
        new_direction = direction
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        score = 0
        speed = 6

# Main game loop
        game_active = True
        while game_active:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != DOWN:
                        new_direction = UP
                    elif event.key == pygame.K_DOWN and direction != UP:
                        new_direction = DOWN
                    elif event.key == pygame.K_LEFT and direction != RIGHT:
                        new_direction = LEFT
                    elif event.key == pygame.K_RIGHT and direction != LEFT:
                        new_direction = RIGHT

            # Update direction
            direction = new_direction

            # Move snake
            head_x, head_y = snake[0]
            new_x = (head_x + direction[0]) % GRID_WIDTH
            new_y = (head_y + direction[1]) % GRID_HEIGHT
            new_head = (new_x, new_y)

            # Check for collisions
            if new_head in snake:
                game_active = False
            else:
                snake.insert(0, new_head)

                # Check if food is eaten
                if new_head == food:
                    score += 1
                    speed += 0.005  # Slightly increase speed
                    # Generate new food (not on snake)
                    while food in snake:
                        food = (random.randint(0, GRID_WIDTH - 1),
                                random.randint(0, GRID_HEIGHT - 1))
                else:
                    snake.pop()  # Remove tail if no food eaten

            # Drawing
            screen.fill(BLACK)
            draw_grid()

            # Draw food
            pygame.draw.rect(screen, RED,
                             (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Draw snake
            for segment in snake:
                pygame.draw.rect(screen, GREEN,
                                 (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                                  GRID_SIZE, GRID_SIZE))

            # Draw score
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.update()
            clock.tick(speed)

        # Game over
        if running:
            running = game_over_screen(score)

    pygame.quit()


if __name__ == "__main__":
    main()