import json
from data_analysis import PERCENTAGE_DATA_PATH_N10, PERCENTAGE_DATA_PATH_N1000
import matplotlib.pyplot as plt

def create_graph(path:str, img_name:str): # Full disclosure, Chat GPT wrote this function 
    with open(path, "r") as file:
        data = json.load(file)

    # Extract sorted time steps (as ints)
    time_steps = sorted(int(step) for step in data.keys())

    # Pull data for each time step
    avg_infected_per_step = [data[str(step)]["average_infected_this_step"] for step in time_steps]
    avg_total_infected = [data[str(step)]["average_total_infected"] for step in time_steps]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, avg_infected_per_step, label="New Infections This Step", linewidth=2)
    plt.plot(time_steps, avg_total_infected, label="Cumulative Infections", linewidth=2)

    # Styling the plot
    plt.title("Average Infections Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Number of Infected Agents")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save to image instead of showing it
    plt.savefig(img_name)
    print("Graph saved as " + img_name)


def main():
    create_graph(PERCENTAGE_DATA_PATH_N10, "n10_graph.png")
    create_graph(PERCENTAGE_DATA_PATH_N1000, "n1k_graph.png")

if __name__ == "__main__":
    main()