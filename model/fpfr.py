from mesa import Agent, Model
from mesa.time import RandomActivation
# from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from model.helpers.inits import set_map_barriers, setRandomTokens, setBomberos
from model.helpers.rounds import begin_round

import numpy as np

import time
import datetime
import random

NUM_BOMBEROS = 6
SIZE_X = 10 + 1
SIZE_Y = 8 + 1
LIMIT_RESCUED = 7
LIMIT_LOST = 4
LIMIT_BUILDING = 24
NUM_FIRE_START = 3
NUM_SMOKE_START = 3
NUM_POI_START = 3


class Tile(Agent):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fire = False
        self.smoke = False
        self.victim = False
        self.poi = False
        self.hot_spot = False
        self.bombero = None


class Barrier:
    def __init__(self, a, b, is_wall, is_door, is_open):
        self.a = tuple(sorted(a))  # normalize
        self.b = tuple(sorted(b))
        self.damage_counters = 0 
        self.is_wall = is_wall
        self.is_door = is_door
        self.is_open = is_open


class Bombero():
    def __init__(self):
        super.__init__()

        self.ap = 4
        self.has_victim = False


def get_grid(model):
    return np.array([[
        4 if tile.firefighter else
        3 if tile.victim else
        2 if tile.fire else
        1 if tile.smoke else
        0
        for tile in row
    ] for row in model.grid])


class GameBoard(Model):
    def __init__(self, init_data):
        super().__init__()

        self.grid = [[Tile(x, y) for y in range(SIZE_Y)] for x in range(SIZE_X)]
        self.barriers = {}
        self.schedule = RandomActivation(self)

        self.saved_victims = 0
        self.lost_victims = 0
        self.total_damage_counters = 0
        self.fireSpots = []
        self.bomberos = []

        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})

        self.__init__board()
        self.load_state(init_data)


    def __init__board(self):
        set_map_barriers(self)
        setRandomTokens(self)
        setBomberos(self)


    def load_state(self, init_data):
        for row in init_data["grid"]:
            for tile_data in row:
                x, y = tile_data["x"], tile_data["y"]
                tile = self.grid[x][y]
                tile.fire = tile_data.get("fire", False)
                tile.smoke = tile_data.get("smoke", False)
                tile.victim = tile_data.get("victim", False)
                tile.poi = tile_data.get("poi", False)
                tile.hot_spot = tile_data.get("hot_spot", False)
                tile.firefighter = tile_data.get("firefighter", None)

    def get_state(self):
        state = []
        for row in self.grid:
            row_data = []
            for tile in row:
                row_data.append({
                    "x": tile.x,
                    "y": tile.y,
                    "fire": tile.fire,
                    "smoke": tile.smoke,
                    "victim": tile.victim,
                    "poi": tile.poi,
                    "hot_spot": tile.hot_spot,
                    "firefighter": tile.firefighter
                })
            state.append(row_data)
        return {"grid": state}


    def game_over(self):
        return (
            self.saved_victims >= LIMIT_RESCUED or 
            self.lost_victims >= LIMIT_LOST or 
            self.total_damage_counters >= LIMIT_BUILDING
    )

    def step(self):
        if self.game_over():
            return { "grid": self.get_state()["grid"], "status": "game_over" }

        begin_round(self)
        self.datacollector.collect(self)
        self.schedule.step()

        return self.get_state()


# start_time = time.time()

# model = GameBoard()
# while not model.game_over():
#     model.step()

# print('Tiempo de ejecución:', str(datetime.timedelta(seconds=(time.time() - start_time))))

# all_agents_info = model.datacollector.get_agent_vars_dataframe()
# all_agents_info.info()
# all_grids = model.datacollector.get_model_vars_dataframe()
# all_grids.info()

# fig, axs = plt.subplots(figsize=(4,4))
# axs.set_xticks([])
# axs.set_yticks([])
# patch = plt.imshow(all_grids.iloc[0, 0], cmap=plt.cm.binary)

# def animate(i):
#     patch.set_data(all_grids.iloc[i, 0])

# anim = animation.FuncAnimation(fig, animate, frames=len(all_grids))

# anim