import time
from queue import Queue, PriorityQueue

with open("cave300x300") as f:
    kaart1 = [l.strip() for l in f.readlines() if len(l) > 1]

with open("cave600x600") as f:
    kaart2 = [l.strip() for l in f.readlines() if len(l) > 1]

with open("cave900x900") as f:
    kaart3 = [l.strip() for l in f.readlines() if len(l) > 1]


def bfs(kaart, start):
    """Breadth First Search"""
    frontier = Queue()
    frontier.put(start)
    iterations = 0
    came_from = {}
    diamond = ()
    path = []
    came_from[start] = None
    found = False

    while not frontier.empty() and not found:
        iterations += 1
        neighbors = []
        current = frontier.get()

        if current[0] - 1 >= 0:
            map_point = kaart[current[0] - 1][current[1]]
            if map_point != "*":
                top = (current[0] - 1, current[1])
                neighbors.append(top)

        if current[0] + 1 < len(kaart):
            map_point = kaart[current[0] + 1][current[1]]
            if map_point != "*":
                bottom = (current[0] + 1, current[1])
                neighbors.append(bottom)

        if current[1] - 1 >= 0:
            map_point = kaart[current[0]][current[1] - 1]
            if map_point != "*":
                left = (current[0], current[1] - 1)
                neighbors.append(left)

        if current[1] + 1 < len(kaart[current[0]]):
            map_point = kaart[current[0]][current[1] + 1]
            if map_point != "*":
                right = (current[0], current[1] + 1)
                neighbors.append(right)

        for next in neighbors:
            if next not in came_from:
                map_point = kaart[next[0]][next[1]]
                frontier.put(next)
                came_from[next] = current
                if map_point == "D":
                    diamond = (next[0], next[1])
                    found = True
                    break

    if found:
        backtrack = diamond
        path.append(diamond)
        while not backtrack == start:
            path.append(came_from[backtrack])
            backtrack = came_from[backtrack]

    path.reverse()
    print(f"Iteratsioonide arv : {iterations}")
    # print(f"Path size : {len(path)}")
    return path


def gbfs(kaart, start, goal):
    """Greedy Best First Search"""
    frontier = PriorityQueue()
    frontier.put((0, start))
    iterations = 0
    found = False
    zig_zag = True
    size_counter = 0
    path = []
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        iterations += 1
        neighbors = []

        if size_counter > 0:
            first = frontier.get()
            second = frontier.get()

            if first[0] == second[0]:
                if zig_zag:
                    current = first[1]
                    frontier.put(second)
                    zig_zag = False
                else:
                    current = second[1]
                    frontier.put(first)
                    zig_zag = True
            else:
                current = first[1]
                frontier.put(second)
        else:
            current = frontier.get()[1]

        if current == goal:
            found = True
            break

        if current[0] - 1 >= 0:
            map_point = kaart[current[0] - 1][current[1]]
            if map_point != "*":
                top = (current[0] - 1, current[1])
                neighbors.append(top)

        if current[0] + 1 < len(kaart):
            map_point = kaart[current[0] + 1][current[1]]
            if map_point != "*":
                bottom = (current[0] + 1, current[1])
                neighbors.append(bottom)

        if current[1] - 1 >= 0:
            map_point = kaart[current[0]][current[1] - 1]
            if map_point != "*":
                left = (current[0], current[1] - 1)
                neighbors.append(left)

        if current[1] + 1 < len(kaart[current[0]]):
            map_point = kaart[current[0]][current[1] + 1]
            if map_point != "*":
                right = (current[0], current[1] + 1)
                neighbors.append(right)

        for next in neighbors:
            if next not in came_from:
                priority = heuristic(next, goal)
                frontier.put((priority, next))
                came_from[next] = current
                size_counter += 1

    if found:
        backtrack = goal
        path.append(goal)
        while not backtrack == start:
            path.append(came_from[backtrack])
            backtrack = came_from[backtrack]

    path.reverse()
    print(f"Iteratsioonide arv : {iterations}")
    # print(f"Path size : {len(path)}")
    return path


def a_star(kaart, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    iterations = 0
    found = False
    zig_zag = True
    size_counter = 0
    path = []
    came_from = {}
    came_from[start] = None
    cost_so_far = {}
    cost_so_far[start] = 0

    while not frontier.empty():
        iterations +=1
        neighbors = []

        if size_counter > 0:
            first = frontier.get()
            second = frontier.get()

            if first[0] == second[0]:
                if zig_zag:
                    current = first[1]
                    frontier.put(second)
                    zig_zag = False
                else:
                    current = second[1]
                    frontier.put(first)
                    zig_zag = True
            else:
                current = first[1]
                frontier.put(second)
        else:
            current = frontier.get()[1]

        if current == goal:
            found = True
            break

        if current[0] - 1 >= 0:
            map_point = kaart[current[0] - 1][current[1]]
            if map_point != "*":
                top = (current[0] - 1, current[1])
                neighbors.append(top)

        if current[0] + 1 < len(kaart):
            map_point = kaart[current[0] + 1][current[1]]
            if map_point != "*":
                bottom = (current[0] + 1, current[1])
                neighbors.append(bottom)

        if current[1] - 1 >= 0:
            map_point = kaart[current[0]][current[1] - 1]
            if map_point != "*":
                left = (current[0], current[1] - 1)
                neighbors.append(left)

        if current[1] + 1 < len(kaart[current[0]]):
            map_point = kaart[current[0]][current[1] + 1]
            if map_point != "*":
                right = (current[0], current[1] + 1)
                neighbors.append(right)

        for next in neighbors:
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put((priority, next))
                came_from[next] = current
                size_counter += 1

    if found:
        backtrack = goal
        path.append(goal)
        while not backtrack == start:
            path.append(came_from[backtrack])
            backtrack = came_from[backtrack]

    path.reverse()
    print(f"Iteratsioonide arv : {iterations}")
    # print(f"Path size : {len(path)}")
    return path


def heuristic(current, goal):
    """Priority maker"""
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


def print_path(path, kaart):
    """Joonistab kogu kaardi path`i kaudu"""
    visited_map = kaart
    for i in path:
        to_change = list(visited_map[i[0]])
        if to_change[i[1]] != "s" and to_change[i[1]] != "D":
            to_change[i[1]] = "X"
        visited_map[i[0]] = "".join(to_change)

    with open("map.txt", "w+") as visit:
        for x in visited_map:
            visit.writelines(x + "\n")


def print_realtime(coords):
    """Joonistab kaardi vahetades uhe kaupa read, vajab coordinates"""
    visited_map = kaart3
    to_change = list(visited_map[coords[0]])
    if to_change[coords[1]] != "s" and to_change[coords[1]] != "D":
        to_change[coords[1]] = "X"
    visited_map[coords[0]] = "".join(to_change)

    with open("map.txt", "w+") as visit:
        for x in visited_map:
            visit.writelines(x + "\n")


if __name__ == '__main__':
    lava_map1 = [
        "      **               **      ",  # 0
        "     ***     D        ***      ",  # 1
        "     ***                       ",  # 2
        "                      *****    ",  # 3
        "                     ********  ",  # 4
        "                        *******",  # 5
        " **                      ******",  # 6
        "*****  *********** ****** ***** ",  # 7
        "*****               *          ",  # 8
        "***                            ",  # 9
        "              **         ******",  # 10
        "**            ***       *******",  # 11
        "*                        ***** ",  # 12
        "                               ",  # 13
        "  s                            ",  # 14
    ]

    start = (14, 2)
    goal = (1, 13)
    # print_path(bfs(lava_map1, start), lava_map1)

    default_start = (2, 2)
    d1 = (295, 257)
    d2 = (598, 595)
    d3 = (898, 895)



    '''Breadth First Search'''

    print("===========================BFS=============================")
    print("___________________________________________________________\n")

    startT = time.time()
    result = bfs(kaart1, (2, 2))
    end = time.time()
    # print(f"Breadth First Search path : {result}")
    print(f"Breadth First Search path size : {len(result)}")
    # print_path(result, kaart1)

    print("Breadth First Search 300x300 time : " + str(end - startT))
    print("___________________________________________________________\n")

    startT = time.time()
    result = bfs(kaart2, (2, 2))
    end = time.time()
    # print(f"Breadth First Search path : {result}")
    print(f"Breadth First Search path size : {len(result)}")
    # print_path(result, kaart2)

    print("Breadth First Search 600x600 time : " + str(end - startT))
    print("___________________________________________________________\n")

    startT = time.time()
    result = bfs(kaart3, (2, 2))
    end = time.time()
    # print(f"Breadth First Search path : {result}")
    print(f"Breadth First Search path size : {len(result)}")
    # print_path(result, kaart3)

    print("Breadth First Search 900x900 time : " + str(end - startT))
    print("___________________________________________________________\n")

    '''Greedy Best First Search'''

    print("===========================GBFS============================")
    print("___________________________________________________________\n")

    startT = time.time()
    result = gbfs(kaart1, (2, 2), d1)
    end = time.time()
    # print(f"Greedy Best First Search path : {result}")
    print(f"Greedy Best First Search path size : {len(result)}")
    print_path(result, kaart1)

    print("Greedy Best First Search 300x300 time : " + str(end - startT))

    print("___________________________________________________________\n")

    startT = time.time()
    result = gbfs(kaart2, (2, 2), d2)
    end = time.time()
    # print(f"Greedy Best First Search path : {result}")
    print(f"Greedy Best First Search path size : {len(result)}")
    # print_path(result, kaart2)

    print("Greedy Best First Search 600x600 time : " + str(end - startT))

    print("___________________________________________________________\n")

    startT = time.time()
    result = gbfs(kaart3, (2, 2), d3)
    end = time.time()
    # print(f"Greedy Best First Search path : {result}")
    print(f"Greedy Best First Search path size : {len(result)}")
    # print_path(result, kaart3)

    print("Greedy Best First Search 900x900 time : " + str(end - startT))

    print("___________________________________________________________\n")

    '''A_STAR'''
    print("==========================A_STAR===========================")
    print("___________________________________________________________\n")

    startT = time.time()
    result = a_star(kaart1, (2, 2), d1)
    end = time.time()
    # print(f"Greedy Best First Search path : {result}")
    print(f"A_STAR path size : {len(result)}")
    # print_path(result, kaart1)

    print("A_STAR 300x300 time : " + str(end - startT))

    print("___________________________________________________________\n")

    startT = time.time()
    result = a_star(kaart2, (2, 2), d2)
    end = time.time()
    # print(f"Greedy Best First Search path : {result}")
    print(f"A_STAR path size : {len(result)}")
    # print_path(result, kaart2)

    print("A_STAR 600x600 time : " + str(end - startT))

    print("___________________________________________________________\n")

    startT = time.time()
    result = a_star(kaart3, (2, 2), d3)
    end = time.time()
    # print(f"Greedy Best First Search path : {result}")
    print(f"A_STAR path size : {len(result)}")
    # print_path(result, kaart3)

    print("A_STAR 900x900 time : " + str(end - startT))

    print("___________________________________________________________\n")


