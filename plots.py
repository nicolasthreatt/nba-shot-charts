import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from classes.shotchart import ShotChart
from enums.court_dimensions import CourtDimensions
from helpers import plot_utils as plotutils


def plot_shotchart(shotchart: ShotChart, title: str, zones: bool=False):
    """Plot the shotchart with optional zones.

    Parameters:
        shotchart (ShotChart): Object containing shot data.
        title (str): Title for the plot.
        zones (bool, optional): Whether to include additional zones on the plot. Defaults to False.
    """
    # Create Figure and plot makes/misses
    plt.figure(figsize=(12,11))
    plt.scatter(shotchart.shots_missed.LOC_X, shotchart.shots_missed.LOC_Y, marker='o', color='green',s=200)
    plt.scatter(shotchart.shots_made.LOC_X, shotchart.shots_made.LOC_Y, marker='x', color='red', s=200)

    # Create axis
    ax = plt.gca()

    # Draw Basketball Court
    ax = plotutils.draw_court(ax, zones=zones)

    # Adjust plot limits to fit in only half court
    plt.xlim(-CourtDimensions.SIDE_BOUNDARY, CourtDimensions.SIDE_BOUNDARY)
    plt.ylim(CourtDimensions.HALFCOURT_BOUNDARY, CourtDimensions.FRONTCOURT_BOUNDARY)

    # Create Labels
    plt.title(title, fontsize=18)
    plt.text(275, 422.5, 'Created By: Nicolas Threatt', fontsize=12, color = '#000000')
    plt.tight_layout()

    # Add shooting text
    plotutils.plot_shooting_text(plt, shotchart, zones=zones)

    # Reformat Axes
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g} ft'.format(x/10))
    ax.xaxis.set_major_formatter(ticks_x)
    ticks_y = ticker.FuncFormatter(lambda y, pos: '{0:g} ft'.format(y/10 + 5))
    ax.yaxis.set_major_formatter(ticks_y)

    # Display plot
    plt.show()


def plot_data_line(shots_dict: dict, categories: list, xlabel: str=None, ylabel: str=None, title: str=None):
    """Plot data as a line graph.

    Parameters:
        shots_dict (dict): A dictionary containing shot data.
        categories (list): A list of categories to plot from the shot data.
        xlabel (str, optional): Label for the x-axis. Defaults to None.
        ylabel (str, optional): Label for the y-axis. Defaults to None.
        title (str, optional): Title for the plot. Defaults to None.

    TODO:
        FINISH (WHAT IF PLAYER DOESNT SCORE IN QUARTER)
    """
    # Create a new figure and axis
    fig, ax = plt.subplots(constrained_layout=True)
    
    # Iterate over each category
    for category in categories:
        labels, shot_data = [], []
        
        # Extract labels and data for the category from the shot dictionary
        for key in shots_dict.keys():
            labels.append(key)
            shot_data.append(shots_dict[key][category])

        # Set x-axis ticks
        ax.xaxis.set_ticks(np.arange(1, 5, 1))
        
        # Plot the data for the category
        plt.plot(labels, shot_data, label=category.title())

    # Set title, xlabel, and ylabel if provided
    if title:
        ax.set_title(title, fontweight="bold")
    if xlabel:
        ax.set_xlabel(xlabel, fontweight="bold")
    if ylabel:
        ax.set_ylabel(ylabel, fontweight="bold")

    # Add legend
    plt.legend(loc="best", title="Shot Type", fancybox=True,
               ncol=1, shadow=True)
    
    # Display the plot
    plt.show()


def plot_data_pie(shots_dict: dict, categories: list, title: str=None):
    """Plot data as pie charts.

    Parameters:
        shots_dict (dict): A dictionary containing shot data.
        categories (list): A list of categories to plot from the shot data.
        title (str, optional): Title for the plot. Defaults to None.
    """
    # Determine the number of columns and rows for subplots based on the number of categories
    cols, rows = (len(categories), 1) if len(categories) <= 3 else (3, len(categories) - 3)

    # Create a new figure
    fig = plt.figure()

    # Iterate over each category
    for i, category in enumerate(categories):
        # Add a subplot to the figure
        ax = fig.add_subplot(rows, cols, i + 1)

        # Extract labels and data for the category from the shot dictionary
        labels = []
        shot_data = []
        for key in shots_dict.keys():
            labels.append(key)
            shot_data.append(shots_dict[key][category])

        # Plot pie chart for the category
        ax.pie(shot_data, labels=labels,
               autopct='%1.1f%%',  # Display percentage values
               shadow=False,       # Disable shadow
               startangle=45)      # Rotate the start of the pie chart

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        ax.set_title(category.title())  # Set title for the subplot

    # Set the main title for the entire plot
    fig.suptitle(title, size=16, fontweight="bold")

    # Adjust layout to accommodate the title
    plt.subplots_adjust(top=0.75)

    # Add legend
    plt.legend(loc="lower right", title="Shot Type", fancybox=True,
               ncol=1, shadow=True)

    # Display the plot
    plt.show()


def plot_shot_category(shots_dict: ShotChart, category: str, xlabel: str=None, ylabel: str=None, title: str=None):
    """Plot shot data for a specific category.

    Parameters:
    - shots_dict (dict): A dictionary containing shot data.
    - category (str): The category of shots to plot.
    - xlabel (str, optional): Label for the x-axis. Defaults to None.
    - ylabel (str, optional): Label for the y-axis. Defaults to None.
    - title (str, optional): Title for the plot. Defaults to None.
    """
    # Initialize empty lists to store labels and shot data
    labels = []
    shot_data = []
    
    # Extract labels and data for the category from the shot dictionary
    for key in shots_dict.keys():
        labels.append(key)
        shot_data.append(shots_dict[key][category])

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Plot the bar chart
    rects = ax.bar(x - width/2, shot_data, width, label=category.title(), color=plotutils.bar_color(category))

    # Add labels
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    if title:
        ax.set_title(title)

    # Add custom tick labels
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Add labels on top of the bars
    ax.bar_label(rects, padding=3)

    fig.tight_layout()

    # Display the plot
    plt.show()


def plot_shot_categories(shots_dict: dict, category1: str, category2: str, xlabel: str=None, ylabel: str=None, title: str=None):
    """Plot shot data for two categories side by side.

    Parameters:
    - shots_dict (dict): A dictionary containing shot data.
    - category1 (str): The first category of shots to plot.
    - category2 (str): The second category of shots to plot.
    - xlabel (str, optional): Label for the x-axis. Defaults to None.
    - ylabel (str, optional): Label for the y-axis. Defaults to None.
    - title (str, optional): Title for the plot. Defaults to None.
    """
    # Initialize empty lists to store labels and shot data for each category
    labels = []
    shot_data1 = []
    shot_data2 = []
    
    # Extract labels and data for both categories from the shot dictionary
    for key in shots_dict.keys():
        labels.append(key)
        shot_data1.append(shots_dict[key][category1])
        shot_data2.append(shots_dict[key][category2])

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Plot the bar charts for both categories side by side
    rects1 = ax.bar(x - width/2, shot_data1, width, label=category1.title(), color=plotutils.bar_color(category1))
    rects2 = ax.bar(x + width/2, shot_data2, width, label=category2.title(), color=plotutils.bar_color(category2))

    # Set labels, title, and custom tick labels
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Add labels on top of the bars for both categories
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    # Display the plot
    plt.show()


def determine_plot(shots_data: dict, plot_type: str, zones: bool=None, plot_data: list=None, title: str=None, xlabel: str=None, ylabel: str=None):
    """Determine the type of plot to create based on parameters.

    Parameters:
    - shots_data (dict): A dictionary containing shot data.
    - plot_type (str): The type of plot to create.
    - zones (bool, optional): Whether to include zone markings. Defaults to None.
    - plot_data (list, optional): Data to plot (e.g., categories). Defaults to None.
    - title (str, optional): Title for the plot. Defaults to None.
    - xlabel (str, optional): Label for the x-axis. Defaults to None.
    - ylabel (str, optional): Label for the y-axis. Defaults to None.
    """
    match plot_type:
        case 'shotchart':
            if zones is not None:
                plot_shotchart(shots_data, title, zones=zones)
            else:
                plot_shotchart(shots_data, title)
        case 'bar':
            if plot_data and len(plot_data) == 1:
                plot_shot_category(shots_data, plot_data[0], xlabel="Shots Taken", title=title)
        case 'double-bar':
            if plot_data and len(plot_data) == 2:
                plot_shot_categories(shots_data, plot_data[0], plot_data[1], xlabel=xlabel, title=title)
        case 'pie':
            if plot_data:
                plot_data_pie(shots_data, plot_data, title=title)
        case 'line':
            if plot_data:
                plot_data_line(shots_data, plot_data, xlabel=xlabel, ylabel=ylabel, title=title)
        case _:
            exit("No shotchart data to plot")
