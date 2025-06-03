from model.fpfr import GameBoard

class GameModel:
    def __init__(self, init_data):
        self.board = GameBoard(init_data)

    def step(self):
        self.board.step()
        return self.get_state()

    @property
    def state(self):
        return self.board.get_state()
