from pprint import pprint
from disease import Grid 
import json 

GRID_SIZE = 20
NUM_AGENTS = 240

ACTUAL_DATA_PATH = "actual_data.json"
PERCENTAGE_DATA_PATH = "percentage_data.json"

def run_n_times(n: int):
    data = {}
    turn_counts = {}  # Track how many simulations reached each timestep

    # Run Simulation n times
    for i in range(n):
        sim = Grid(GRID_SIZE)
        sim.fill_grid(NUM_AGENTS, 1)
        instance_data = sim.run_simulation(visualize=False)

        # Accumulate data per time step
        for turn in instance_data:
            if turn not in data:
                data[turn] = {
                    "average_infected_this_step": 0,
                    "average_total_infected": 0
                }
                turn_counts[turn] = 0

            data[turn]["average_infected_this_step"] += instance_data[turn]["num_infected_this_step"]
            data[turn]["average_total_infected"] += instance_data[turn]["total_num_infected"]
            turn_counts[turn] += 1

    # Compute averages per time step based on how many runs reached that step
    for turn in data:
        data[turn]["average_infected_this_step"] /= turn_counts[turn]
        data[turn]["average_total_infected"] /= turn_counts[turn]

    # Save Actual Data to JSON
    with open(ACTUAL_DATA_PATH, "w") as json_file:
        json.dump(data, json_file, indent=4)

    for turn in data:
        # If percentage, show the ratio of infected agents compared to the amount we started with, otherwise show the average number of agents
        data[turn]["average_infected_this_step"] /= NUM_AGENTS 
        data[turn]["average_total_infected"] /= NUM_AGENTS 
        data[turn]["average_infected_this_step"] *= 100
        data[turn]["average_total_infected"] *= 100

    # Save Percentage Data to JSON
    with open(PERCENTAGE_DATA_PATH, "w") as json_file:
        json.dump(data, json_file, indent=4)

    

def main():
    run_n_times(100)

if __name__ == "__main__":
    main()