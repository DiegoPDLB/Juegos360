from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

# Función para cargar el mapa desde final.txt
def load_map(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    grid = []
    for i in range(6):
        row = [list(cell.strip()) for cell in lines[i].split()]
        grid.append(row)

    pois = []
    for i in range(6, 9):
        r, c, t = lines[i].split()
        pois.append((int(r), int(c), t.strip()))

    fires = []
    for i in range(9, 19):
        r, c = lines[i].split()
        fires.append((int(r), int(c)))

    doors = []
    for i in range(19, 27):
        r1, c1, r2, c2 = lines[i].split()
        doors.append((int(r1), int(c1), int(r2), int(c2)))

    entrances = []
    for i in range(27, 31):
        r, c = lines[i].split()
        entrances.append((int(r), int(c)))

    return {
        "walls": grid,
        "pois": pois,
        "fires": fires,
        "doors": doors,
        "entrances": entrances
    }

# Clase para representar objetos como fuego
class StaticElement:
    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return self.symbol

# Modelo del juego
class FireRescueModel(Model):
    def __init__(self, map_data, width=8, height=6):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.map_data = map_data

        # Colocar fuego inicial en el grid
        for (x, y) in map_data["fires"]:
            self.grid.place_agent(StaticElement("🔥"), (y - 1, x - 1))

    def step(self):
        self.schedule.step()

# Ejecución del simulador
if __name__ == "__main__":
    map_data = load_map("final.txt")
    model = FireRescueModel(map_data)

    print("🧯 Mapa inicial con marcadores de fuego:")
    for y in range(6):
        row = ""
        for x in range(8):
            cell = model.grid.get_cell_list_contents((x, y))
            row += cell[0].symbol if cell else "⬜"
        print(row)
