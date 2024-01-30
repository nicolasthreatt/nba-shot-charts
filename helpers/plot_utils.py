import argparse
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from classes.shotchart import ShotChart
from enums.court_dimensions import CourtDimensions
from matplotlib.patches import Circle, Rectangle, Arc


def generate_title(shotchart_df: pd.DataFrame, args: argparse.Namespace):
    """Generate title for shot data display.

    Args:
        shotchart_df (pd.DataFrame): DataFrame containing shot chart data.
        args: Arguments controlling the display.

    Returns:
        str: Generated title.
    """
    title = shotchart_df.iloc[0]['PLAYER_NAME'] if args.player else shotchart_df.iloc[0]['TEAM_NAME']
    title += ' - ' + shotchart_df.iloc[0]['HTM'] + ' vs.' + shotchart_df.iloc[0]['VTM'] + ' on ' + shotchart_df.game_date.strftime('%m/%d/%Y')
    return title


def display_shot_data(shotchart_df: pd.DataFrame, processed_data, args: argparse.Namespace):
    """Display shot data using processed data.

    Args:
        shotchart_df (pd.DataFrame): DataFrame containing shot chart data.
        processed_data: Processed data to be displayed.
        args: Arguments controlling the display.
    """
    if shotchart_df is not None:
        title = generate_title(shotchart_df, args)
        determine_plot(shotchart_df, args.plot_type, plot_data=args.plot_data,
                       title=title, xlabel=get_xlabel(args), ylabel=get_ylabel(args))
    else:
        exit("No data to display.")


def draw_court(ax: matplotlib.axes.Axes, color: str='black', lw: int=2, zones: bool=False) -> matplotlib.axes.Axes:
    """Draw the various parts of an NBA basketball court.

    Parameters:
        ax (matplotlib.axes.Axes): The axes on which to draw the court.
        color (str, optional): The color of the court lines. Defaults to 'black'.
        lw (int, optional): The linewidth of the court lines. Defaults to 2.
        zones (bool, optional): Whether to draw additional zones on the court. Defaults to False.

    Returns:
        - ax (matplotlib.axes.Axes): The axes with the court drawn on it.
    """
    plt.tight_layout()

    # Basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Backboard
    backboard = Rectangle((-30, -7.5), CourtDimensions.INNER_PAINT, -1, linewidth=lw, color=color)

    # Paint (Outer Box - width=16ft, height=19ft, Inner Box - width=12ft, height=19ft)
    outer_box = Rectangle((-CourtDimensions.OUTER_PAINT, CourtDimensions.FRONTCOURT_BOUNDARY), 160, 190, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-CourtDimensions.INNER_PAINT, CourtDimensions.FRONTCOURT_BOUNDARY), 120, 190, linewidth=lw, color=color, fill=False)

    # Create free throw
    top_free_throw = Arc((0, CourtDimensions.FREE_THROW_LINE), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    bottom_free_throw = Arc((0, CourtDimensions.FREE_THROW_LINE), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')

    # Restricted Zone (Arc with 4ft radius from center of the hoop)
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three Pointer Line (14 Long Before Arc)
    corner_three_a = Rectangle((-220, CourtDimensions.FRONTCOURT_BOUNDARY), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, CourtDimensions.FRONTCOURT_BOUNDARY), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Half-Court
    center_outer_arc = Arc((0, CourtDimensions.HALFCOURT_BOUNDARY), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, CourtDimensions.HALFCOURT_BOUNDARY), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # Draw Half-Court, Base, and Side-Out Bound Lines
    outer_lines = Rectangle((-CourtDimensions.SIDE_BOUNDARY, CourtDimensions.FRONTCOURT_BOUNDARY), 500, 470, linewidth=lw, color=color, fill=False)

    # List of the Court Elements to Plot
    court_elements = [hoop, backboard, outer_box, inner_box,
                      top_free_throw, bottom_free_throw, restricted,
                      corner_three_a, corner_three_b, three_arc,
                      center_outer_arc, center_inner_arc,
                      outer_lines]

    # Add Court Elements onto Axes
    for element in court_elements:
        ax.add_patch(element)

    # Create zones, if specified
    if zones:
        draw_zones(ax)

    return ax


def draw_zones(ax, color='slategray', lw=1.5):
    """Draws additional zones on the basketball court.

    Parameters:
        ax (matplotlib.axes.Axes): The axes on which to draw the zones.
        color (str, optional): The color of the zone lines. Defaults to 'slategray'.
        lw (int, optional): The linewidth of the zone lines. Defaults to 1.5.
    """
    if zones:
        # Right Block
        ax.plot([-(CourtDimensions.CORNER3_X - 1), -CourtDimensions.OUTER_PAINT], [CourtDimensions.CORNER3_Y, CourtDimensions.CORNER3_Y], linewidth=lw, color=color)

        # Left Block
        ax.plot([(CourtDimensions.CORNER3_X - 1), CourtDimensions.OUTER_PAINT], [CourtDimensions.CORNER3_Y, CourtDimensions.CORNER3_Y], linewidth=lw, color=color)

        # Right Elbow
        ax.plot([-CourtDimensions.OUTER_PAINT, -CourtDimensions.OUTER_PAINT], [CourtDimensions.FREE_THROW_LINE, 224], linewidth=lw, color=color)

        # Left Elbow
        ax.plot([CourtDimensions.OUTER_PAINT, CourtDimensions.OUTER_PAINT], [CourtDimensions.FREE_THROW_LINE, 224], linewidth=lw, color=color)

        # Right Corner 3
        ax.plot([-CourtDimensions.SIDE_BOUNDARY, -(CourtDimensions.CORNER3_X + 1)], [CourtDimensions.CORNER3_Y, CourtDimensions.CORNER3_Y], linewidth=lw, color=color)

        # Left Corner 3
        ax.plot([CourtDimensions.SIDE_BOUNDARY, (CourtDimensions.CORNER3_X + 1)], [CourtDimensions.CORNER3_Y, CourtDimensions.CORNER3_Y], linewidth=lw, color=color)

        # Above the Break 3 Line Left
        ax.plot([-CourtDimensions.RIGHT_WING_3, -CourtDimensions.RIGHT_WING_3], [201, CourtDimensions.DEEP3_Y], linewidth=lw, color=color)

        # Above the Break 3 Line Right
        ax.plot([CourtDimensions.RIGHT_WING_3, CourtDimensions.RIGHT_WING_3], [201, CourtDimensions.DEEP3_Y], linewidth=lw, color=color)

        # Deep 3 Line
        ax.plot([-CourtDimensions.SIDE_BOUNDARY, CourtDimensions.SIDE_BOUNDARY], [CourtDimensions.DEEP3_Y, CourtDimensions.DEEP3_Y], linewidth=lw, color=color)

        # Deep 3 Line Left
        ax.plot([-CourtDimensions.DEEP3_X, -CourtDimensions.DEEP3_X], [CourtDimensions.DEEP3_Y, CourtDimensions.HALFCOURT_BOUNDARY], linewidth=lw, color=color)

        # Deep 3 Line Right
        ax.plot([CourtDimensions.DEEP3_X, 100], [CourtDimensions.DEEP3_Y, CourtDimensions.HALFCOURT_BOUNDARY], linewidth=lw, color=color)


def plot_shooting_text(plt: matplotlib.pyplot, shotchart: ShotChart, zones: bool=False):
    """Plot shooting text on the chart.

    Parameters:
        plt: matplotlib.pyplot object.
        shotchart (ShotChart): Shooting data object.
        zones (bool, optional): Whether to include zone markings. Defaults to False.
    """
    if zones:
        text_data = [
            ('Paint', shotchart.paint),
            ('Right Corner 3', shotchart.right_corner_3),
            ('Right Block', shotchart.right_block),
            ('Right Elbow', shotchart.right_elbow),
            ('Right Wing 3', shotchart.right_wing_3),
            ('Right Deep 3', shotchart.right_deep_3),
            ('Left Corner 3', shotchart.left_corner_3),
            ('Left Block', shotchart.left_block),
            ('Left Elbow', shotchart.left_elbow),
            ('Left Wing 3', shotchart.left_wing_3),
            ('Left Deep 3', shotchart.left_deep_3),
            ('High Post', shotchart.high_post),
            ('Top of Key 3', shotchart.top_of_key_3),
            ('Straight Deep 3', shotchart.straight_deep_3),
            ('Total', shotchart.total_points)
        ]
    else:
        text_data = [
            ('2PT', shotchart.two_points),
            ('3PT', shotchart.three_points),
            ('Total', shotchart.total_points)
        ]

    for i, (label, data) in enumerate(text_data):
        text = format_shooting_text(label, data["made"], data["attempted"], data["percent"])
        plt.text(275, i * 20, text, fontsize=15)


def format_shooting_text(location: str, made: int, attempt: int, percentage: float) -> str:
    """Format shooting statistics as a string.

    Parameters:
        location (str): Description of the shooting location.
        made (int): Number of shots made from the location.
        attempt (int): Total number of attempts from the location.
        percentage (float): Shooting percentage from the location.

    Returns:
        str: Formatted string representing shooting statistics.
    """
    return f"{location}: {made}/{attempt} ({percentage:.2%})"


def bar_color(category: str):
    """Determines color for bar based on category.

    Args:
        category (str): Category type.

    Returns:
        str: Color.
    """
    if category == 'made':
        return 'green'
    elif category == 'missed':
        return 'red'
    elif category == "percent":
        return 'dodgerblue'
    elif category == "frequency":
        return 'orange'
    else:
        return 'blue'
