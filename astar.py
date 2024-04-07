import math
import heapq
from readmap import read_input_from_file
from readmap import read_input_from_file_multi

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
         
maze1, dest1, src1 = read_input_from_file('input_level_1.txt')
maze2, dest2, src2 = read_input_from_file_multi('input_level_2.txt')
ROW1 = len(maze1)
COL1 = len(maze1[0])
ROW2 = len(maze2)
COL2 = len(maze2[0])
 
# Check if a cell is valid (within the grid)
def is_valid(row, col):
    return (row >= 0) and (row < ROW1) and (col >= 0) and (col < COL1)

def is_valid2(row, col):
    return (row >= 0) and (row < ROW2) and (col >= 0) and (col < COL2)
 
# Check if a cell is unblocked
def is_unblocked(grid, row, col):
    return grid[row][col] == 0
 
# Check if a cell is the destination
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]
 
def calculate_h_value(row, col, dest):
    return math.sqrt((row - dest[0]) ** 2 + (col - dest[1]) ** 2)  

def calculate_h_value2(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5
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

def a_star_search(grid, src, dest):
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("Source or destination is invalid")
        return []

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return []

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return []

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL1)] for _ in range(ROW1)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL1)] for _ in range(ROW1)]

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

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
                    # Trace the path from source to destination
                    path = trace_path(cell_details, dest)
                    return path
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

    # If the destination is not found after visiting all cells
    print("Failed to find the destination cell")
    return []

#Multi hiders search
def a_star_search_multi(grid, src, destinations):
    paths = []
    a = src
    for dest in destinations:
        # Check if the source and destination are valid
        if not is_valid2(a[0], a[1]) or not is_valid2(dest[0], dest[1]):
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
        closed_list = [[False for _ in range(COL2)] for _ in range(ROW2)]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(COL2)] for _ in range(ROW2)]

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
                if is_valid2(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
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
                        h_new = calculate_h_value2(new_i, new_j, dest)
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

        # If the destination is not found after visiting all cells
        #if not found_dest:
        #    print("Failed to find the destination cell")

    return paths
