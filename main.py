import pygame
import heapq
import math
import time
# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Kích thước màn hình và ô vuông
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 30
BORDER_SIZE = 1  # Kích thước viền cho mỗi ô


def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        size = tuple(map(int, lines[0].split()))
        map_matrix = []
        for line in lines[1:-2]:
            map_matrix.append(list(map(int, line.split())))
        obstacles = [tuple(map(int, line.split())) for line in lines[-2:]]
    return size, map_matrix, obstacles


def draw_map(screen, map_matrix):
    for i in range(len(map_matrix)):
        for j in range(len(map_matrix[0])):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            if map_matrix[i][j] == 0:  # Ô trống
                pygame.draw.rect(screen, BLACK, rect, BORDER_SIZE)  # Vẽ viền màu trắng
            else:  # Các ô khác
                pygame.draw.rect(screen, BLACK, rect, BORDER_SIZE)  # Vẽ viền màu đen
                if map_matrix[i][j] == 1:  # Tường
                    pygame.draw.rect(screen, BLACK, rect)
                elif map_matrix[i][j] == 2:  # Người trốn
                    pygame.draw.rect(screen, GREEN, rect)
                elif map_matrix[i][j] == 3:  # Người tìm kiếm
                    pygame.draw.rect(screen, RED, rect)

def draw_obstacles(screen, obstacles):
    for obstacle in obstacles:
        rect = pygame.Rect(obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE,
                           (obstacle[3] - obstacle[1] + 1) * CELL_SIZE,
                           (obstacle[2] - obstacle[0] + 1) * CELL_SIZE)
        pygame.draw.rect(screen, BLUE, rect, BORDER_SIZE)  # Vẽ viền cho mỗi ô

def astar(map_matrix, start, end):
    heap = [(0, start)]
    heapq.heapify(heap)
    visited = set()
    parent = {}
    g_scores = {start: 0}
    found = False

    while heap:
        _, current = heapq.heappop(heap)
        for neighbor in get_neighbors(map_matrix, current):
            tentative_g_score = g_scores[current] + 1
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(heap, (f_score, neighbor))
                parent[neighbor] = current

        if current == end:
            found = True
            break

    if found:
        path = []
        while current != start:
            path.append(current)
            current = parent[current]
        path.append(start)
        path.reverse()
        return path
    else:
        return None

# Heuristic function (Euclidean distance)
def heuristic(node, end):
    return math.sqrt((node[0] - end[0])**2 + (node[1] - end[1])**2)

# Get neighboring nodes
def get_neighbors(map_matrix, node):
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left
    for dx, dy in directions:
        x, y = node[0] + dx, node[1] + dy
        if 0 <= x < len(map_matrix) and 0 <= y < len(map_matrix[0]) and map_matrix[x][y] == 0:
            neighbors.append((x, y))
    return neighbors

def main():
    size, map_matrix, obstacles = read_input_file("input.txt")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Finding Path")

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_map(screen, map_matrix)
        draw_obstacles(screen, obstacles)
         # Define start and end points
        
        for i in range(len(map_matrix)):
            for j in range(len(map_matrix[0])):
                if map_matrix[i][j] == 3:
                    start = (i, j)  

        for i in range(len(map_matrix)):
            for j in range(len(map_matrix[0])):
                if map_matrix[i][j] == 2:
                    end = (i, j-1) 
        # Find path using A*
        path = astar(map_matrix, start, end)
                # Draw the path on the screen
        if path:
            for node in path:
                rect = pygame.Rect(node[1] * CELL_SIZE, node[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, RED, rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()