import random 
import os
import time 
import sys

EMPTY = "\033[90m- \033[0m"
HEALTHY = "\u2022 " # Green Bullet
SICK = "\033[31m\u2022\033[0m " # Red Bullet
RECOVERED = "\033[34m\u2022\033[0m "  # Blue Bullet


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class Agent: 
    def __init__(self, symbol):
        self.symbol = symbol 
        self.time_infected = None
        if symbol == SICK:
            self.time_infected = 20
        
    def infect(self):
        if self.symbol == HEALTHY:
            self.symbol = SICK
            self.time_infected = 20 
     
     # False if Dead, True if alive 
    def check_for_recovery(self)->bool:
        if self.time_infected == 0:
            result = random.randint(1, 10)
            if result == 1: 
                return False
            else:
                self.symbol = RECOVERED
                self.time_infected = None 

    def __eq__(self, other):
        if not isinstance(other, str):
            return NotImplemented
        return self.symbol == other

class Grid:
    def __init__(self, size):
        self.cols = size 
        self.rows = size 
        self.grid = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]

    def fill_grid(self, n_healthy, n_sick):
        healthy_cells = []
        for i in range(n_healthy):
            empty_cell_positions = self.find_all(EMPTY)
            random_index = random.randint(0, len(empty_cell_positions) - 1)
            random_cell = empty_cell_positions[random_index]
            self.grid[random_cell[0]][random_cell[1]] = HEALTHY

        for i in range(n_sick):
            healthy_cell_positions = self.find_all(HEALTHY)
            random_index = random.randint(0, len(healthy_cell_positions) - 1)
            random_cell = healthy_cell_positions[random_index]
            self.grid[random_cell[0]][random_cell[1]] = SICK

    def get_orthogonal_neighbors(self, row, col)->list[tuple[int,int]]:
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                neighbors.append((new_row, new_col))  # or grid[new_row][new_col] if you want values

        return neighbors
    
    def find_all(self, target)->list[tuple[int,int]]: # valid targets are HEALTHY, EMPTY, SICK, RECOVERED
        result = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == target:
                    result.append((row, col))  
        return result

    def move(self, row, col):
        neighbors = self.get_orthogonal_neighbors(row, col)
        if neighbors is None:
            return

        # Check the grid value at each neighbor's coordinates
        neighbors = [cell for cell in neighbors if self.grid[cell[0]][cell[1]] == EMPTY]

        if not neighbors:
            return

        # Pick a random empty neighbor
        target = random.choice(neighbors)

        # Move the entity
        self.grid[target[0]][target[1]] = self.grid[row][col]
        self.grid[row][col] = EMPTY


    def move_agents(self):
        agent_coords = self.find_all(HEALTHY) + self.find_all(SICK)
        random.shuffle(agent_coords) # Randomizes the order in which agents are allowed to move to avoid having a bias 
        for coord in agent_coords:
            self.move(coord[0], coord[1])
        self.spread_disease()

    def spread_disease(self):
        sick_agent_coords = self.find_all(SICK)
        for coord in sick_agent_coords:
            neighbors = self.get_orthogonal_neighbors(coord[0], coord[1])
            for neighbor in neighbors:
                if self.grid[neighbor[0]][neighbor[1]] == HEALTHY:
                    self.grid[neighbor[0]][neighbor[1]] = SICK

    def visualize(self, turn, playback_delay):
        # Move cursor to top-left only — don't wipe the screen
        sys.stdout.write("\033[H")
        sys.stdout.flush()

        # Build the grid string
        output = '\n'.join(''.join(row) for row in self.grid)
        output += f"\n\nTurn: {turn}"

        sys.stdout.write(output)
        sys.stdout.flush()
        time.sleep(playback_delay)

    def run_simulation(self, visualize=False, playback_delay=0.1) -> dict:
        print("\033[3J\033[H\033[2J")  # Clear scrollback + screen
        print("\033[?25l", end="")     # Hide cursor
        
        
        turn = 0
        data = {}
        while self.find_all(HEALTHY):
            if visualize:
                self.visualize(turn, playback_delay)
            previous_num_infected = self.find_all(SICK)
            self.move_agents()
            new_num_infected = self.find_all(SICK)
            turn += 1
            data[turn] = self.get_data(previous_num_infected, new_num_infected)
        if visualize:
            self.visualize(turn, playback_delay)
        print("\033[?25h", end="")  # Show cursor again
        print("\n")
        return data 

    def get_data(self, prev_num_infected, new_num_infected)->dict:
        data = {
            "num_infected_this_step" :  len(new_num_infected) - len(prev_num_infected),
            "total_num_infected" : len(new_num_infected)
        }
        return data 
                    

def main():
    # Simulation can handle much larger grid size, but visualizing it becomes ugly if grid size is above 49x49
    new_grid = Grid(20)
    new_grid.fill_grid(240, 1)
    new_grid.run_simulation(True)

    

if __name__ == "__main__":
    main()