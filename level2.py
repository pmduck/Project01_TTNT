import math
import heapq
import pygame
import sys
import time

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)

 
# Define the Cell class
class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination
 
# Define the size of the grid
def read_input_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    size = tuple(map(int, lines[0].strip().split()))
    maze = []
    hider_positions = []
    seeker_position = None
    for i in range(1, size[0] + 1):
        row = list(map(int, lines[i].strip().split()))
        maze.append(row)
        for j, cell in enumerate(row):
            if cell == 2:  # Hider
                hider_positions.append((i - 1, j)) 
                row[j] = 0
            elif cell == 3:  # Seeker
                seeker_position = (i - 1, j)
                row[j] = 0
    return maze, hider_positions, seeker_position

maze, dest, src = read_input_from_file('input_level_9.txt')
ROW = len(maze)
COL = len(maze[0])
 
# Check if a cell is valid (within the grid)
def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)
 
# Check if a cell is unblocked
def is_unblocked(grid, row, col):
    return grid[row][col] == 0
 
# Check if a cell is the destination
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]
 
# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest):
    return math.sqrt((row - dest[0]) ** 2 + (col - dest[1]) ** 2)
 
# Trace the path from source to destination
def trace_path(cell_details, dest):
    #print("The Path is ")
    path = []
    row = dest[0]
    col = dest[1]

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append((row, col))
    # Reverse the path to get the path from source to destination
    path.reverse()

    # Print the path
    #for i in path:
    #    print("->", i, end=" ")
    #print()
    
    return path if path else []  # Return empty list if no path found
 

def a_star_search(grid, src, destinations):
    paths = []
    a = src
    for dest in destinations:
        # Check if the source and destination are valid
        if not is_valid(a[0], a[1]) or not is_valid(dest[0], dest[1]):
            print("Source or destination is invalid")
            return paths

        # Check if the source and destination are unblocked
        if not is_unblocked(grid, a[0], a[1]) or not is_unblocked(grid, dest[0], dest[1]):
            print("Source or the destination is blocked")
            return paths

        # Check if we are already at the destination
        if is_destination(a[0], a[1], dest):
            print("We are already at the destination")
            return paths

        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

        # Initialize the start cell details
        i = a[0]
        j = a[1]
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j

        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        # Initialize the flag for whether destination is found
        found_dest = False

        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Mark the cell as visited
            i = p[1]
            j = p[2]
            closed_list[i][j] = True

            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]

                # If the successor is valid, unblocked, and not visited
                if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                    # If the successor is the destination
                    if is_destination(new_i, new_j, dest):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        print("The destination cell is found")
                        # Trace and print the path from source to destination
                        paths.append(trace_path(cell_details, dest))
                        found_dest = True
                        break
                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[i][j].g + 1.0
                        h_new = calculate_h_value(new_i, new_j, dest)
                        f_new = g_new + h_new

                        # If the cell is not in the open list or the new f value is smaller
                        if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            cell_details[new_i][new_j].f = f_new
                            cell_details[new_i][new_j].g = g_new
                            cell_details[new_i][new_j].h = h_new
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j
            if found_dest:
                a = dest
                break
        print("Failed to find the destination cell")
    return paths


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

def main():
    print("Maze:")
    for row in maze:
        print(row)

    print("Hider positions:", dest)
    print("Seeker position:", src)

    start_time = time.time()

    paths = a_star_search(maze, src, dest)
    execution_time = time.time() - start_time
    print("Thời gian tìm đường: ", execution_time, "giây")
    
    path2 = []
    for idx, path in enumerate(paths):
        for item in path:
            # Tạo một danh sách con mới chứa từng phần tử của tuple
            sublist = [item[0], item[1]]
            # Thêm danh sách con vào danh sách mới src2
            path2.append(sublist)
    print (path2)

    dest2 = []

    for item in dest:
    # Tạo một danh sách con mới chứa từng phần tử của tuple
        sublist = [item[0], item[1]]
    # Thêm danh sách con vào danh sách mới dest2
        dest2.append(sublist)
    print("dest2", dest2)
    src2 = [src]
    print("src2", src2)

    points = 11
    TOTAL = 0
    found_destinations = []  # Danh sách để theo dõi các điểm đích đã được tìm thấy

    for path in paths:
        for point in path:
            p1, p2 = point
            points -= 1
            print(points)
            first_element = path[0]
            s1, s2 = first_element
            found = False  # Biến này để kiểm tra xem điểm đích đã được tìm thấy trước đó chưa
            for pair in dest2:
                x, y = pair
                if x == p1 and y == p2 and s1 != x and s2 != y and pair not in found_destinations:
                    points += 20
                    found_destinations.append(pair)  # Thêm điểm đích vào danh sách đã tìm thấy
                    found = True
                    print("Fiding hider bonus + 20:", points)
        TOTAL = points - 1
    if TOTAL >= 0:
        print ("You Win")
    else:
        print ("You Lose")    

   

    screen = draw_maze(maze, src2, dest2)
    draw_path(path2, maze, screen)

if __name__ == '__main__':
    main()
