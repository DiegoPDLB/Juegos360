from ..fpfr import Tile, Barrier, Bombero
from ..fpfr import NUM_BOMBEROS, SIZE_X, SIZE_Y, NUM_FIRE_START
from ..fpfr import NUM_POI_START, NUM_SMOKE_START

def barrier_key(a, b):
    return tuple(sorted[a, b])


def set_map_barriers(model):
    barriers = [
        # doors
        [(0, 3), (1, 3), False, True, True],
        [(3, 1), (4, 1), False, True, False],
        [(6, 0), (6, 1), False, True, True],
        [(5, 2), (6, 2), False, True, False],
        [(2, 3), (3, 3), False, True, False],
        [(4, 4), (4, 5), False, True, False],
        [(6, 4), (7, 4), False, True, False],
        [(8, 2), (8, 3), False, True, False],
        [(8, 4), (9, 4), False, True, True],
        [(3, 6), (3, 7), False, True, True],
        [(5, 6), (5, 7), False, True, False],
        [(7, 7), (7, 8), False, True, False],
    ]

    for i in range(1, SIZE_X):
        barriers.append([(i, 0), (i, 1), True, False, False]) # top wall
        barriers.append([(i, 6), (i, 7), True, False, False]) # bottom wall
    for i in range(1, SIZE_Y):
        barriers.append([(0, i), (1, i), True, False, False]) # left wall
        barriers.append([(8, i), (9, i), True, False, False]) # right wall

    for (a, b, is_wall, is_door, is_open) in barriers:
        key = barrier_key(a, b)
        model.barriers[key] = Barrier(a, b, is_wall, is_door, is_open)


def setRandomTokens(model):
    i = 0
    starter_map = {1: "curr_smoke", 2: "curr_fire", 3: "curr_poi"}
    setattr(model, starter_map[starter], getattr(model, starter_map[starter]) + 1)

    while i < NUM_SMOKE_START + NUM_FIRE_START + NUM_POI_START:
        x = model.random.randrange(1, SIZE_X - 1)
        y = model.random.randrange(1, SIZE_Y - 1)
        if model.cells[x][y] == 0:
            if starter == 1:
                model.smoke_spots.append(Tile(x, y))
            elif starter == 2:
                model.fire_spots.append(Tile(x, y))
            elif starter == 3:
                model.poi_spots.append(Tile(x, y))
            model.cells[x][y] = starter
            model.curr_[starter] += 1
            i += 1
        if model.curr_[starter] >= 3:
            starter += 1 

def setBomberos(model):
    print('')