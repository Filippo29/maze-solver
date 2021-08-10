import cv2
import numpy
import numpy as np

delay = 2

path = r"maze2.png"
img = cv2.imread(path)

print("Image shape: " + str(img.shape))

cv2.namedWindow("Maze")
cv2.imshow("Maze", img)

dim = 0


def find_entrance(image):  # find the entrance on the left of the file
    global dim
    x = 0
    y = 0
    while image[y, x][0] < 100:
        y += 1
        if y == image.shape[0] - 1:
            break
    start_y = y
    color = image[y, x]
    while np.array_equal(image[y, x], color):
        dim += 1
        y += 1
    print("Square dim: " + str(dim))
    dim -= 1
    cv2.imshow("Maze", image)
    return start_y


def check_borders(maze, x, y, actual):
    # in some maze images black lines are not always as black as (0, 0, 0)
    # same for the white zones, they are not as white as (255, 255, 255)
    # for that reason in some cases its better to compare color like I did in this function or in find_entrance
    free_borders = []
    if x - dim - 2 >= 0 and maze[y, x - 1][0] > 100 and maze[y, x - 1][2] > 100 and actual != 'l' and actual != 'r':
        free_borders.append((x - dim - 2, y, 'l'))
    if y - dim - 2 >= 0 and maze[y - 1, x][0] > 100 and maze[y - 1, x][2] > 100 and actual != 't' and actual != 'b':
        free_borders.append((x, y - dim - 2, 't'))
    if x + dim + 2 <= maze.shape[1] and maze[y, x + dim + 1][0] > 100 and maze[y, x + dim + 1][2] > 100 and \
            actual != 'r' and actual != 'l':
        free_borders.append((x + dim + 2, y, 'r'))
    if y + dim + 2 <= maze.shape[0] and maze[y + dim + 1, x][0] > 100 and maze[y + dim + 1, x][2] > 100 and \
            actual != 'b' and actual != 't':
        free_borders.append((x, y + dim + 2, 'b'))
    return free_borders


def find_next_node(maze, x, y, direction):
    x_offset = 0
    y_offset = 0
    if direction == 'r':
        x_offset = 1
    elif direction == 'l':
        x_offset = -1
    elif direction == 't':  # top
        y_offset = -1
    elif direction == 'b':  # bottom
        y_offset = 1
    df = int(dim / 4)
    while x < maze.shape[1] and y < maze.shape[0] and \
            (((direction == 'r' or direction == 'b') and
              numpy.array_equal(maze[y - y_offset, x - x_offset], [255, 255, 255])) or
             ((direction == 'l' or direction == 't') and
              numpy.array_equal(maze[y - y_offset * dim + 1, x - x_offset * dim + 1], [255, 255, 255]))):
        cv2.rectangle(maze, (x + df, y + df), (x + 3 * df, y + 3 * df), (255, 0, 0), -1)
        cv2.imshow("Maze", maze)
        cv2.waitKey(delay)
        free = check_borders(maze, x, y, direction)
        for f in free:
            if f[0] == maze.shape[1]:
                print("PATH FOUND")
                return True
            img2 = maze.copy()
            if find_next_node(img2, f[0], f[1], f[2]):
                return True
        x += x_offset*dim + 2*x_offset
        y += y_offset*dim + 2*y_offset
        if x == maze.shape[1] and numpy.array_equal(maze[y, x - 1], [255, 255, 255]):
            print("PATH FOUND")
            return True
    return False


start = find_entrance(img)
find_next_node(img, 1, start, 'r')
cv2.waitKey(0)
cv2.destroyAllWindows()
