
def distance(location1, location2):
    if location1[0] > location2[0]:
        location1, location2 = location2, location1
    dx = abs(location1[0] - location2[0])
    dy = abs(location1[1] - location2[1])
    if location2[1] >= location1[1]:
        return dx + dy
    else:
        return max(dx, dy)


def around_location(location):
    chart = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
    neighbour = []
    for move in chart:
        neighbour.append((location[0] + move[0], location[1] + move[1]))
    return neighbour


def check_chessboard(chessboard):
    location_list = list(set([p.location for p in chessboard]))
    begin_station = location_list[0]
    exist_neighbour = [p for p in around_location(begin_station) if p in location_list]
    station_visited = [begin_station] + exist_neighbour
    while len(exist_neighbour) > 0:
        station = exist_neighbour.pop(0)
        new_exist_neighbour = [p for p in around_location(station) if p in location_list
                               and p not in station_visited]
        exist_neighbour.extend(new_exist_neighbour)
        station_visited.extend(new_exist_neighbour)
    return len(location_list) == len(station_visited)


def check_occupy(location, chessboard):
    for piece in chessboard:
        if piece.location == location:
            return True
    else:
        return False


def one_step(move_location, fix_location, chessboard):
    if distance(move_location, fix_location) != 1:
        raise ValueError('No Adjacent!')
    chart = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
    relative_position = (move_location[0] - fix_location[0], move_location[1] - fix_location[1])
    i, j = right_left_door(relative_position, chart)
    ans = []
    # i: clockwise j: anticlockwise
    for p in [i, j]:
        location = (fix_location[0]+chart[p][0], fix_location[1]+chart[p][1])
        door = (relative_position[0]+location[0], relative_position[1]+location[1])
        if not check_occupy(location, chessboard) and not check_occupy(door, chessboard):
            ans.append(location)
    return ans


def right_left_door(relative_position, chart):
    k = chart.index(relative_position)
    return (k + 1) % 6, k - 1
