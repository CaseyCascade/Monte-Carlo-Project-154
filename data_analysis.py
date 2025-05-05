from pprint import pprint
from disease import Grid
import json 
from tqdm import tqdm
from create_graphs import create_graph, create_heatmap

# 20 x 20 with 240 Agents 
# OR
# 100 x 100 with 6k Agents
GRID_SIZE = 20
NUM_AGENTS = 240

ACTUAL_DATA_PATH = "actual_data.json"
PERCENTAGE_DATA_PATH_N1000 = "percentage_data_n1000.json"
PERCENTAGE_DATA_PATH_N10 = "percentage_data_n10.json"
START_POSITION_SURVIVABILITY = "start_position_survivability.json"


def run_n_times(n: int):
    if n == 1000:
        path = PERCENTAGE_DATA_PATH_N1000
    elif n == 10:
        path = PERCENTAGE_DATA_PATH_N10
    else: 
        print("Must run either 10 or 1000 times to save to JSON")
        return 
    
    position_data = {}
    data = {}
    turn_counts = {}  # Track how many simulations reached each timestep

    data[0] = {
    "average_infected_this_step": 0,
    "average_total_infected": n
    }

    
    turn_counts[0] = n  # All simulations start with the same initial state

    # Run Simulation n times
    for i in tqdm(range(n), desc="Running Simulations"):
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
        
        position_data[i] = {
                            "start_pos": sim.get_start_pos(),
                            "turns_lasted": sim.get_turns_lasted()
                            }

    # Compute averages per time step based on how many runs reached that step
    for turn in data:
        data[turn]["average_infected_this_step"] /= turn_counts[turn]
        data[turn]["average_total_infected"] /= turn_counts[turn]

    for turn in data:
        # If percentage, show the ratio of infected agents compared to the amount we started with, otherwise show the average number of agents
        data[turn]["average_infected_this_step"] /= NUM_AGENTS 
        data[turn]["average_total_infected"] /= NUM_AGENTS 
        data[turn]["average_infected_this_step"] *= 100
        data[turn]["average_total_infected"] *= 100

    # Save Percentage Data to JSON
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    with open(START_POSITION_SURVIVABILITY, "w") as json_file:
        json.dump(position_data, json_file, indent=4)
    

def main():
    #run_n_times(10)
    #run_n_times(1000)
    #create_graph(PERCENTAGE_DATA_PATH_N10, "n10_graph.png")
    #create_graph(PERCENTAGE_DATA_PATH_N1000, "n1k_graph.png")
    create_heatmap(START_POSITION_SURVIVABILITY, "start_position_survivability.png")


if __name__ == "__main__":
    main()