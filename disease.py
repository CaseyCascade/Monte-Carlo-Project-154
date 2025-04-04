import random 
import os
import time 
import sys

EMPTY = "- "
HEALTHY = "\u2022 "
SICK = "\033[31m\u2022\033[0m "

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class Grid:
    def __init__(self, size):
        self.cols = size 
        self.rows = size 
        self.grid = [["- " for _ in range(self.cols)] for _ in range(self.rows)]

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

    def get_orthogonal_neighbors(self, row, col)->list[tuple[int,int]]:
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                neighbors.append((new_row, new_col))  # or grid[new_row][new_col] if you want values

        return neighbors
    
    def find_all(self, target)->list[tuple[int,int]]: # valid targets are HEALTHY, EMPTY, SICK 
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

    def run_simulation(self, visualize=False, playback_delay=0.1):
        turn = 0
        while self.find_all(HEALTHY):
            if visualize:
                self.visualize(turn, playback_delay)
            self.move_agents()
            turn += 1
        if visualize:
            self.visualize(turn, playback_delay)
        print("\033[?25h", end="")  # Show cursor again
                    

def main():
    print("\033[3J\033[H\033[2J")  # Clear scrollback + screen
    print("\033[?25l", end="")     # Hide cursor

    # Simulation can handle much larger grid size, but visualizing it becomes ugly if grid size is above 49x49
    new_grid = Grid(20)
    new_grid.fill_grid(240, 1)
    new_grid.run_simulation(True)

    print("\033[?25h", end="")     # Show cursor again

    

if __name__ == "__main__":
    main()