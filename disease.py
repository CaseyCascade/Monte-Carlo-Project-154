import random 

EMPTY = "- "
HEALTHY = "\u2022 "
SICK = "\033[31m\u2022\033[0m "

class Grid:
    def __init__(self, size):
        self.cols = size 
        self.rows = size 
        self.grid = [["- " for _ in range(self.cols)] for _ in range(self.rows)]

    def print(self):
        for row in self.grid:
            line = ''.join(row)
            print(line)

    def fill_grid(self, n_healthy, n_sick):
        healthy_cells = []
        for i in range(n_healthy):
            random_row = random.randint(0, len(self.grid) - 1)
            random_col = random.randint(0, len(self.grid[random_row]) - 1)
            random_cell = self.grid[random_row][random_col]

            if random_cell == EMPTY:
                self.grid[random_row][random_col] = HEALTHY
                healthy_cells.append((random_row, random_col))

        for i in range(n_sick):
            random_index = random.randint(0, len(healthy_cells) - 1)
            chosen_healthy_cell = healthy_cells[random_index]
            self.grid[chosen_healthy_cell[0]][chosen_healthy_cell[1]] = SICK

    def get_orthogonal_neighbors(self, row, col):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                neighbors.append((new_row, new_col))  # or grid[new_row][new_col] if you want values

        return neighbors
    
    def find(self, target):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == target:
                    return (row, col)  # Return as soon as it's found
        return None  

    def move(self, row, col):
        neighbors = self.get_orthagonal_neighbors(row, col)
        if neighbors == None: return 

        neighbors = [cell for cell in neighbors if cell == EMPTY]
        
        random_index = random.randint(0, len(neighbors))
        self.grid[neighbors[random_index][0], neighbors[random_index][1]] = neighbors[row, col]
        neighbors[row][col] = EMPTY

    def move_agents(self):
        pass


    def spread_disease(self):
        pass

    def next_turn(self):
        self.move_agents()
        self.spread_disease()
                    

def main():
    new_grid = Grid(10)
    new_grid.fill_grid(5, 1)
    new_grid.print()
    

if __name__ == "__main__":
    main()