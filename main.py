import heapq
import pygame
import sys
from astar import a_star_search_multi
from astar import a_star_search
from readmap import read_input_from_file
from readmap import read_input_from_file_multi
from draw import draw_maze
from draw import draw_path



def main():
    choice = input("Menu:\n1. Hiện số 1\n2. Hiện số 2\nChọn: ")
    if choice == '2':
        maze2, dest2, src2 = read_input_from_file_multi('input_level_2.txt')

        print("Hider positions:", dest2)
        print("Seeker position:", src2)

        paths2 = a_star_search_multi(maze2, src2, dest2)
        
        path22 = []
        for idx, path2 in enumerate(paths2):
            for item2 in path2:
                sublist2 = [item2[0], item2[1]]
                path22.append(sublist2)
        print (path22)

        dest22 = []
        for item22 in dest2:
            sublist22 = [item22[0], item22[1]]
            dest22.append(sublist22)
        print("dest22", dest22)
        src22 = [src2]
        print("src2", src22)

        screen = draw_maze(maze2, src22, dest22)
        draw_path(path22, maze2, screen)

    else:
        maze, dest, src = read_input_from_file('input_level_1.txt')

        print("Hider position:", dest)
        print("Seeker position:", src)

        dest1 = [dest]
        print("dest", dest1)
        src1 = [src]
        print("src1", src1)
        # Run the A* search algorithm
        path = a_star_search(maze, src, dest)

        if path:
            # Draw the maze
            screen = draw_maze(maze,src1,dest1)
            # Draw the path found by A* algorithm
            draw_path(path, maze, screen)


if __name__ == '__main__':
    main()