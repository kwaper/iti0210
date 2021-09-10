MAP = [
    ["S", " ", "B", "P"],
    ["W", "GSB", "P", "B"],
    ["S", " ", "B", " "],
    ["A", "B", "P", "B"]
]

AI_MAP = [
    [" ", " ", " ", " "],
    [" ", " ", " ", " "],
    [" ", " ", " ", " "],
    [" ", " ", " ", " "]
]

# {coords : [Breeze, Stench]}
visited = {}
feel = ["B", "S"]


def move(pos):
    current = pos
    neighbours = find_neighbours(current)

    for i in visited.keys():
        AI_MAP[i[0]][i[1]] = "_"
    if AI_MAP[current[0]][current[1]] != "?":
        AI_MAP[current[0]][current[1]] = "A"
        map_show()

    if MAP[current[0]][current[1]] not in feel:
        visited[current] = [False, False]
    if MAP[current[0]][current[1]] == "S":
        visited[current] = [False, True]
    if MAP[current[0]][current[1]] == "B":
        visited[current] = [True, False]
    spl = MAP[current[0]][current[1]]
    if "S" in spl and "B" in spl:
        visited[current] = [True, True]

    if True in visited[current]:
        mark_danger(current)

    if len(visited) > 2:
        unvisited_joint_neighbours = []
        all_unvisited_neighbours_lists = [find_neighbours(x) for x in visited.keys()]
        all_unvisited_neighbours = []
        for i in all_unvisited_neighbours_lists:
            all_unvisited_neighbours += i

        for n in range(len(all_unvisited_neighbours) - 1):
            for n1 in range(n + 1, len(all_unvisited_neighbours)):
                if all_unvisited_neighbours[n] == all_unvisited_neighbours[n1] and \
                        all_unvisited_neighbours[n] not in visited.keys() and \
                        all_unvisited_neighbours[n] not in unvisited_joint_neighbours:
                    unvisited_joint_neighbours.append(all_unvisited_neighbours[n])

        joint_room_neighbours = {}
        for i in unvisited_joint_neighbours:
            nb = []
            for x in visited.keys():
                if i in find_neighbours(x):
                    nb.append(x)
            joint_room_neighbours[i] = nb

        if len(joint_room_neighbours) > 0:
            unmark_danger(joint_room_neighbours)

    if "G" in MAP[current[0]][current[1]]:
        map_show()
        print("WIN")
        return "WIN"
    if MAP[current[0]][current[1]] == "W":
        map_show()
        print("LOSE")
        return "LOSE"
    if MAP[current[0]][current[1]] == "P":
        map_show()
        print("LOSE")
        return "LOSE"

    for i in neighbours:
        if i not in visited.keys() and AI_MAP[i[0]][i[1]] != "?":
            if move(i) != "":
                break

    return ""


def map_show():
    for i in AI_MAP:
        print(i)
    print()


def unmark_danger(jnb):
    for k, v in jnb.items():
        if not (visited[v[0]][0] and visited[v[1]][0]) and not (visited[v[0]][1] and visited[v[1]][1]):
            AI_MAP[k[0]][k[1]] = " "
        if visited[v[0]][0] and visited[v[1]][0]:
            AI_MAP[k[0]][k[1]] = "P"
            visited[k] = [True, False]
        if visited[v[0]][1] and visited[v[1]][1]:
            AI_MAP[k[0]][k[1]] = "W"
            visited[k] = [False, True]

    map_show()
    pass


def mark_abs_danger():
    clone = visited.copy()
    for k, v in clone.items():
        if v[0]:
            nb = find_neighbours(k)
            only_one = True
            for i in nb:
                if i in visited.keys():
                    if visited[i][0]:
                        only_one = False
            trap = []
            if only_one:
                for i in nb:
                    if i not in visited.keys():
                        trap.append(i)

            if len(trap) == 1:
                AI_MAP[trap[0][0]][trap[0][1]] = "P"
                visited[trap[0]] = [True, False]


def mark_danger(current):
    neighbours = find_neighbours(current)
    for n in neighbours:
        if n not in visited.keys():
            AI_MAP[n[0]][n[1]] = "?"

    mark_abs_danger()
    map_show()


def find_neighbours(current):
    neighbours = []
    if 0 < current[0] < 3:
        if 0 < current[1] < 3:
            neighbours.append((current[0] - 1, current[1]))
            neighbours.append((current[0] + 1, current[1]))
            neighbours.append((current[0], current[1] - 1))
            neighbours.append((current[0], current[1] + 1))
        elif current[1] == 0:
            neighbours.append((current[0] - 1, current[1]))
            neighbours.append((current[0] + 1, current[1]))
            neighbours.append((current[0], current[1] + 1))
        elif current[1] == 3:
            neighbours.append((current[0] - 1, current[1]))
            neighbours.append((current[0] + 1, current[1]))
            neighbours.append((current[0], current[1] - 1))
    elif current[0] == 0:
        if 0 < current[1] < 3:
            neighbours.append((current[0] + 1, current[1]))
            neighbours.append((current[0], current[1] - 1))
            neighbours.append((current[0], current[1] + 1))
        elif current[1] == 0:
            neighbours.append((current[0] + 1, current[1]))
            neighbours.append((current[0], current[1] + 1))
        elif current[1] == 3:
            neighbours.append((current[0] + 1, current[1]))
            neighbours.append((current[0], current[1] - 1))
    elif current[0] == 3:
        if 0 < current[1] < 3:
            neighbours.append((current[0] - 1, current[1]))
            neighbours.append((current[0], current[1] - 1))
            neighbours.append((current[0], current[1] + 1))
        elif current[1] == 0:
            neighbours.append((current[0] - 1, current[1]))
            neighbours.append((current[0], current[1] + 1))
        elif current[1] == 3:
            neighbours.append((current[0] - 1, current[1]))
            neighbours.append((current[0], current[1] - 1))

    return neighbours


if __name__ == '__main__':
    move((3, 0))
