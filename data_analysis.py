from pprint import pprint
from disease import Grid, HEALTHY, SICK, EMPTY



def run_n_times(n:int, death_rule:bool):
    data = {}
    turns_to_finish = {}

    # Run Simulation n times
    for i in range(n):
        sim = Grid(20)
        sim.fill_grid(240, 1)
        instance_data = sim.run_simulation(visualize=False, death_rule=death_rule)

        # Add up amount of turns to finish each simulation run 
        if not len(instance_data) in turns_to_finish:
            turns_to_finish[len(instance_data)] = 0 
        turns_to_finish[len(instance_data)] += 1

        # Add up data from every run according to time step 
        for turn in instance_data:
            if turn not in data:
                data[turn] = {
                    "average_infected_this_step": 0,
                    "average_total_infected": 0
                }
            data[turn]["average_infected_this_step"] += instance_data[turn]["num_infected_this_step"]
            data[turn]["average_total_infected"] += instance_data[turn]["total_num_infected"]

    # Average across all runs per time step 
    for turn in data:
        data[turn]["average_infected_this_step"] /= n
        data[turn]["average_total_infected"] /= n

    # Average infected per time step (amount per step & running total)
    pprint(data)

    # Histogram of runs and how many turns it took for them to finish 
    pprint(turns_to_finish)
            
            


def main():
    # Simulation can handle much larger grid size, but visualizing it becomes ugly if grid size is above 49x49
    new_grid = Grid(20)
    new_grid.fill_grid(240, 1)
    #pprint(new_grid.run_simulation(True))
    run_n_times(1000, death_rule=True)


if __name__ == "__main__":
    main()