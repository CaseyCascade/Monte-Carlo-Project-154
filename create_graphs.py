import numpy as np
import json 
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap

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
    plt.plot(time_steps, avg_infected_per_step, label="Average Rate of Infections this Step", linewidth=2)
    plt.plot(time_steps, avg_total_infected, label="Average Cumulative Infections", linewidth=2)

    # Styling the plot
    n_string = "10"
    if img_name == "n1k_graph.png":
        n_string = "1000"
    
    plt.title("Average Infections Over Time for n = " + n_string)
    plt.xlabel("Time Step")
    plt.ylabel("Ratio of Infected Agents")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save to image instead of showing it
    plt.savefig(img_name)
    print("Graph saved as " + img_name)


def create_heatmap(path: str, img_name: str):
    # Parameters
    grid_size = (20, 20)
    low_thresh = 20
    high_thresh = 25

    # Heatmaps for low and high duration categories
    low_grid = np.zeros(grid_size)
    high_grid = np.zeros(grid_size)

    # Load JSON file
    with open(path, "r") as f:
        data = json.load(f)

    # Process each run
    for entry in data.values():
        x, y = entry["start_pos"]
        turns = entry["turns_lasted"]

        if turns <= low_thresh:
            low_grid[x, y] += 1
        elif turns >= high_thresh:
            high_grid[x, y] += 1

    # Determine shared color scale range
    combined_max = max(np.max(low_grid), np.max(high_grid))
    vmin = 0
    vmax = combined_max


    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))  # Width x Height in inches

    # Plot the two layers
    # Plot with normalized color scaling
    vmin = 0
    # Create a custom colormap from Reds
    reds = cm.get_cmap('Reds', 256)
    reds_rgba = reds(np.linspace(0, 1, 256))
    reds_rgba[0] = [0, 0, 0, 0]  # Make 0 fully transparent
    transparent_reds = ListedColormap(reds_rgba)

    # Do the same for Blues
    blues = cm.get_cmap('Blues', 256)
    blues_rgba = blues(np.linspace(0, 1, 256))
    blues_rgba[0] = [0, 0, 0, 0]
    transparent_blues = ListedColormap(blues_rgba)

    # Use with vmin=0, vmax=6
    low_plot = ax.imshow(low_grid.T, cmap=transparent_reds, interpolation='nearest', vmin=vmin, vmax=vmax)
    high_plot = ax.imshow(high_grid.T, cmap=transparent_blues, interpolation='nearest', vmin=vmin, vmax=vmax)

    # Low threshold colorbar (Red) – close to the plot
    cbar_low = plt.colorbar(low_plot, ax=ax, fraction=0.046, pad=0.2, orientation='vertical')
    cbar_low.set_label(f'Starts ≤ {low_thresh} turns', color='black', rotation=90, labelpad=15)
    cbar_low.ax.yaxis.set_label_position('right')
    cbar_low.ax.yaxis.set_ticks_position('right')

    # High threshold colorbar (Blue) – spaced further away to prevent overlap
    cbar_high = plt.colorbar(high_plot, ax=ax, fraction=0.046, pad=0.2, orientation='vertical')
    cbar_high.set_label(f'Starts ≥ {high_thresh} turns', color='black', rotation=90, labelpad=15)
    cbar_high.ax.yaxis.set_label_position('right')
    cbar_high.ax.yaxis.set_ticks_position('right')

    # Set ticks from 0 to 19 for both axes
    ax.set_xticks(np.arange(20))
    ax.set_yticks(np.arange(20))
    ax.set_xticklabels(np.arange(20))
    ax.set_yticklabels(np.arange(20))

    # Final plot settings
    fig.suptitle("Patient Zero Start Positions by Number of Survived Turns")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(img_name)
    print("Graph saved as " + img_name)