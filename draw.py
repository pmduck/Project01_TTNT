import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)

# Draw the maze
def draw_maze(maze, src, dest):
    pygame.init()
    cell_size = 15
    maze_size = (len(maze[0]) * cell_size, len(maze) * cell_size)
    screen = pygame.display.set_mode(maze_size)
    pygame.display.set_caption("Maze")
    screen.fill(WHITE)

    # Draw the maze grid
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:  # Blocked cell
                pygame.draw.rect(screen, BLACK, (j * cell_size, i * cell_size, cell_size, cell_size))
            else:  # Unblocked cell
                for paird in dest:
                    xd, yd = paird
                    if i == xd and j == yd:
                        pygame.draw.rect(screen, BLUE, (j * cell_size, i * cell_size, cell_size, cell_size))
                for pairs in src:
                    xs, ys = pairs
                    if i == xs and j == ys:
                        pygame.draw.rect(screen, RED, (j * cell_size, i * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, BLACK, (j * cell_size, i * cell_size, cell_size, cell_size), 1)
    pygame.display.flip()
    return screen

# Draw the path
def draw_path(path, maze, screen):
    cell_size = 15
    visited = set()  # Keep track of visited cells
    for pos in path:
        i, j = pos
        # Change the color of the current cell to green
        pygame.draw.rect(screen, GREEN, (j * cell_size + 5, i * cell_size + 5, cell_size - 7, cell_size - 7))
        pygame.display.flip()
        pygame.time.delay(100)  # Delay to visualize the path
        
        # Change the color of the previously visited cell to dark green
        for visited_pos in visited:
            vi, vj = visited_pos
            pygame.draw.rect(screen, DARK_GREEN, (vj * cell_size + 5, vi * cell_size + 5, cell_size - 7, cell_size - 7))
        
        # Add the current cell to the visited set
        visited.add((i, j))
        
    # Keep the window open until the user closes it
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
