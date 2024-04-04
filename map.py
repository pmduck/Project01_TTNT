import pygame

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
                elif map_matrix[i][j] == 2:  # Người giấu
                    pygame.draw.rect(screen, GREEN, rect)
                elif map_matrix[i][j] == 3:  # Người tìm kiếm
                    pygame.draw.rect(screen, RED, rect)

def draw_obstacles(screen, obstacles):
    for obstacle in obstacles:
        rect = pygame.Rect(obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE,
                           (obstacle[3] - obstacle[1] + 1) * CELL_SIZE,
                           (obstacle[2] - obstacle[0] + 1) * CELL_SIZE)
        pygame.draw.rect(screen, BLUE, rect, BORDER_SIZE)  # Vẽ viền cho mỗi ô

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

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
