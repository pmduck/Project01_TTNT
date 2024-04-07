def read_input_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    size = tuple(map(int, lines[0].strip().split()))
    maze = []
    hider_position = None
    seeker_position = None
    for i in range(1, size[0] + 1):
        row = list(map(int, lines[i].strip().split()))
        maze.append(row)
        for j, cell in enumerate(row):
            if cell == 2:  # Hider
                hider_position = (i - 1, j)
                row[j] = 0
            elif cell == 3:  # Seeker
                seeker_position = (i - 1, j)
                row[j] = 0
    return maze, hider_position, seeker_position

def read_input_from_file_multi(filename):
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
                hider_positions.append((i - 1, j))  # Thêm vị trí của hider vào danh sách
                row[j] = 0
            elif cell == 3:  # Seeker
                seeker_position = (i - 1, j)
                row[j] = 0
    return maze, hider_positions, seeker_position
