
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
    return [(location[0]+1, location[1]), (location[0]-1, location[1]),
            (location[0], location[1]+1), (location[0], location[1]-1),
            (location[0]-1, location[1]+1), (location[0]+1, location[1]-1)]
