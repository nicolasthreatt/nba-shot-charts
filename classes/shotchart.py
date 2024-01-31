

import math
import pandas as pd
import sys
from collections import OrderedDict
from datetime import datetime
from enums.court_dimensions import CourtDimensions


class ShotChart:
    """A class representing a shot chart with various statistics and breakdowns."""
    def __init__(self, shotchart_df: pd.DataFrame = None):
        """Initialize a ShotChart object.

        Args:
            shotchart_df (pd.DataFrame, optional): DataFrame containing shot chart data.
        """
        self.df = shotchart_df

        # Create Dictionary Keys
        field_goal_keys = ["made", "missed", "attempted", "percent", "frequency"]

        # Shot Points ShotChart Members
        self.shots_missed = dict.fromkeys(field_goal_keys, 0)
        self.shots_made = dict.fromkeys(field_goal_keys, 0)
        self.two_points = dict.fromkeys(field_goal_keys, 0)
        self.three_points = dict.fromkeys(field_goal_keys, 0)
        self.total_points = dict.fromkeys(field_goal_keys, 0)

        # Shot Zone ShotChart Members
        self.right_corner_3 = dict.fromkeys(field_goal_keys, 0)
        self.right_block = dict.fromkeys(field_goal_keys, 0)
        self.right_elbow = dict.fromkeys(field_goal_keys, 0)
        self.right_wing_3 = dict.fromkeys(field_goal_keys, 0)
        self.right_deep_3 = dict.fromkeys(field_goal_keys, 0)
        self.left_corner_3 = dict.fromkeys(field_goal_keys, 0)
        self.left_block = dict.fromkeys(field_goal_keys, 0)
        self.left_elbow = dict.fromkeys(field_goal_keys, 0)
        self.left_wing_3 = dict.fromkeys(field_goal_keys, 0)
        self.left_deep_3 = dict.fromkeys(field_goal_keys, 0)
        self.paint = dict.fromkeys(field_goal_keys, 0)
        self.high_post = dict.fromkeys(field_goal_keys, 0)
        self.top_of_key_3 = dict.fromkeys(field_goal_keys, 0)
        self.straight_deep_3 = dict.fromkeys(field_goal_keys, 0)

        # Initialize shot chart member dictionaries
        self.shot_chart_data = {
            "points": {},
            "types": {},
            "breakdowns": {},
            "distances": OrderedDict.fromkeys(["0 - 5", "5 - 10", "10 - 15", "15 - 20", "20 - 25", "25 - 30", "30+"], 0),
            "periods": OrderedDict.fromkeys([1, 2, 3, 4], 0)
        }

    def process(self, zones: bool = False, points: bool = None, shot_type: bool = None, 
                shot_distances: bool = None, shot_periods: bool = None, shot_breakdown: bool = None):
        """


        Args:
            zones (bool, optional): Whether to process shots by zones.
            points (bool, optional): Whether to process shots by points.
            shot_type (bool, optional): Whether to process shots by type.
            shot_distances (bool, optional): Whether to process shots by distance.
            shot_periods (bool, optional): Whether to process shots by period.
            shot_breakdown (bool, optional): Whether to process shots by breakdown.
        """
        if isinstance(self.df, pd.DataFrame) and not self.df.empty:
            # Game Date
            self.game_date = datetime.strptime(str(self.df.iloc[0]['GAME_DATE']), '%Y%m%d')

            # Process shot statistics if corresponding flags are True
            if points:
                self.process_shots_by_points(self.shot_chart_data["points"])
            if zones:
                self.process_shots_by_zones()
            if shot_type:
                self.process_shots_by_type(self.shot_chart_data["types"])
            if shot_distances:
                self.process_shots_by_distance(self.shot_chart_data["distances"])
            if shot_periods:
                self.process_shots_by_period(self.shot_chart_data["periods"])
            if shot_breakdown:
                self.process_shots_by_breakdown(self.shot_chart_data["breakdowns"])

    def process_shots_by_points(self, points_dict) -> dict:
        """Process shot statistics by points based on the provided DataFrame."""
        for index, row in self.df.iterrows():
            # Determine shot type (2-point vs 3-point)
            shot_type = "2PT" if row["SHOT_TYPE"] == "2PT Field Goal" else "3PT"

            # Initialize shot statistics for the current shot type if not already present in the dictionary.
            if shot_type not in points_dict:
                keys = ["made", "missed", "attempted", "percent", "frequency"]
                points_dict[shot_type] = dict.fromkeys(keys, 0)

            # Collect made vs. missed shots
            event_type = row["EVENT_TYPE"]
            if event_type == "Made Shot":
                points_dict[shot_type]["made"] += 1
            elif event_type == "Missed Shot":
                points_dict[shot_type]["missed"] += 1

            # Record attempted shots and shooting percentage
            points_dict[shot_type]["attempted"] = points_dict[shot_type]["made"] + points_dict[shot_type]["missed"]
            points_dict[shot_type]["percent"] = points_dict[shot_type]["made"] / points_dict[shot_type]["attempted"]

            # Calculate frequency of points
            total_attempted = self.df['SHOT_ATTEMPTED_FLAG'].sum()
            points_dict[shot_type]["frequency"] = points_dict[shot_type]["attempted"] / total_attempted

        return points_dict


    def process_shots_by_zones(self) -> None:
        """Process shot statistics by different zones on the basketball court based on the provided DataFrame."""
        # Iterate through all shots
        for index, row in shotchart.iterrows():
            key = "made" if "Made" in row.EVENT_TYPE else "missed"
            # Right Corner 3
            if (row.LOC_X > -CourtDimensions.SIDE_BOUNDARY and row.LOC_X < -CourtDimensions.CORNER3_X) and \
               (row.LOC_Y < CourtDimensions.CORNER3_Y and row.LOC_Y > CourtDimensions.FRONTCOURT_BOUNDARY):
                self.right_corner_3[key] = self.right_corner_3[key] + 1
                self.right_corner_3["attempted"] = self.right_corner_3["made"] +  self.right_corner_3["missed"]
                self.right_corner_3["percent"] = self.right_corner_3["made"] / self.right_corner_3["attempted"]

            # Left Corner 3
            elif (row.LOC_X < CourtDimensions.SIDE_BOUNDARY and row.LOC_X > CourtDimensions.CORNER3_X) and \
                 (row.LOC_Y < CourtDimensions.CORNER3_Y and row.LOC_Y > CourtDimensions.FRONTCOURT_BOUNDARY):
                self.left_corner_3[key] = self.left_corner_3[key] + 1
                self.left_corner_3["attempted"] = self.left_corner_3["made"] +  self.left_corner_3["missed"]
                self.left_corner_3["percent"] = self.left_corner_3["made"] / self.left_corner_3["attempted"]

            # Paint
            elif (row.LOC_X > -CourtDimensions.OUTER_PAINT and row.LOC_X < CourtDimensions.OUTER_PAINT) and \
                 (row.LOC_Y < CourtDimensions.FREE_THROW_LINE and row.LOC_Y > CourtDimensions.FRONTCOURT_BOUNDARY):
                self.paint[key] = self.paint[key] + 1
                self.paint["attempted"] = self.paint["made"] +  self.paint["missed"]
                self.paint["percent"] = self.paint["made"] / self.paint["attempted"]

            # Right Post/Block
            elif (row.LOC_X > -220 and row.LOC_X < -CourtDimensions.OUTER_PAINT) and \
                 (row.LOC_Y < CourtDimensions.CORNER3_Y and row.LOC_Y > CourtDimensions.FRONTCOURT_BOUNDARY):
                self.right_block[key] = self.right_block[key] + 1
                self.right_block["attempted"] = self.right_block["made"] +  self.right_block["missed"]
                self.right_block["percent"] = self.right_block["made"] / self.right_block["attempted"]

            # Left Post/Block
            elif (row.LOC_Y < 219 and row.LOC_Y < CourtDimensions.OUTER_PAINT) and \
                 (row.LOC_Y < CourtDimensions.CORNER3_Y and row.LOC_Y > CourtDimensions.FRONTCOURT_BOUNDARY):
                self.left_block[key] = self.left_block[key] + 1
                self.left_block["attempted"] = self.left_block["made"] +  self.left_block["missed"]
                self.left_block["percent"] = self.left_block["made"] / self.left_block["attempted"]

            # Above Free Throw/High Post
            elif row.LOC_X > -CourtDimensions.OUTER_PAINT and row.LOC_X < CourtDimensions.OUTER_PAINT and \
                 row.LOC_Y > CourtDimensions.FREE_THROW_LINE and \
                 self.is_shot_inside_3pt_arc(row.LOC_X, row.LOC_Y, 22, 158):
                self.high_post[key] = self.high_post[key] + 1
                self.high_post["attempted"] = self.high_post["made"] +  self.high_post["missed"]
                self.high_post["percent"] = self.high_post["made"] / self.high_post["attempted"]

            # Right Elbow
            elif row.LOC_X < -CourtDimensions.OUTER_PAINT and \
                 row.LOC_Y > CourtDimensions.CORNER3_Y and \
                 self.is_shot_inside_3pt_arc(row.LOC_X, row.LOC_Y, 22, 158):
                self.right_elbow[key] = self.right_elbow[key] + 1
                self.right_elbow["attempted"] = self.right_elbow["made"] +  self.right_elbow["missed"]
                self.right_elbow["percent"] = self.right_elbow["made"] / self.right_elbow["attempted"]

            # Left Elbow
            elif row.LOC_X > CourtDimensions.OUTER_PAINT and \
                 row.LOC_Y > CourtDimensions.CORNER3_Y and \
                 self.is_shot_inside_3pt_arc(row.LOC_X, row.LOC_Y, 22, 158):
                self.left_elbow[key] = self.left_elbow[key] + 1
                self.left_elbow["attempted"] = self.left_elbow["made"] +  self.left_elbow["missed"]
                self.left_elbow["percent"] = self.left_elbow["made"] / self.left_elbow["attempted"]

            # Right Wing
            elif row.LOC_X < -CourtDimensions.RIGHT_WING_3 and row.LOC_X > -CourtDimensions.SIDE_BOUNDARY and \
                 row.LOC_Y > CourtDimensions.CORNER3_Y and row.LOC_Y < CourtDimensions.DEEP3_Y and \
                 not self.is_shot_inside_3pt_arc(row.LOC_X, row.LOC_Y,  158, 22):
                self.right_wing_3[key] = self.right_wing_3[key] + 1
                self.right_wing_3["attempted"] = self.right_wing_3["made"] +  self.right_wing_3["missed"]
                self.right_wing_3["percent"] = self.right_wing_3["made"] / self.right_wing_3["attempted"]

            # Left Wing
            elif row.LOC_X > CourtDimensions.RIGHT_WING_3 and row.LOC_X < CourtDimensions.SIDE_BOUNDARY and \
                 row.LOC_Y > CourtDimensions.CORNER3_Y and row.LOC_Y < CourtDimensions.DEEP3_Y and \
                 not self.is_shot_inside_3pt_arc(row.LOC_X, row.LOC_Y,  158, 22):
                self.left_wing_3[key] = self.left_wing_3[key] + 1
                self.left_wing_3["attempted"] = self.left_wing_3["made"] +  self.left_wing_3["missed"]
                self.left_wing_3["percent"] = self.left_wing_3["made"] / self.left_wing_3["attempted"]

            # Top of Key
            elif row.LOC_X > -CourtDimensions.RIGHT_WING_3 and row.LOC_X < CourtDimensions.RIGHT_WING_3 and \
                 row.LOC_Y < CourtDimensions.DEEP3_Y and \
                 not self.is_shot_inside_3pt_arc(row.LOC_X, row.LOC_Y, 22, 158):
                self.top_of_key_3[key] = self.top_of_key_3[key] + 1
                self.top_of_key_3["attempted"] = self.top_of_key_3["made"] +  self.top_of_key_3["missed"]
                self.top_of_key_3["percent"] = self.top_of_key_3["made"] / self.top_of_key_3["attempted"]

            # Straight Deep 3
            elif (row.LOC_X > CourtDimensions.DEEP3_Y and row.LOC_X < CourtDimensions.HALFCOURT_BOUNDARY) and \
                 (row.LOC_Y > -CourtDimensions.SIDE_BOUNDARY and row.LOC_Y < -CourtDimensions.DEEP3_X):
                self.straight_deep_3[key] = self.straight_deep_3[key] + 1
                self.straight_deep_3["attempted"] = self.straight_deep_3["made"] +  self.straight_deep_3["missed"]
                self.straight_deep_3["percent"] = self.straight_deep_3["made"] / self.straight_deep_3["attempted"]

            # Right Deep 3
            elif (row.LOC_Y > -CourtDimensions.SIDE_BOUNDARY and row.LOC_Y < -CourtDimensions.DEEP3_X) and \
                 (row.LOC_X > CourtDimensions.DEEP3_Y and row.LOC_X < CourtDimensions.HALFCOURT_BOUNDARY):
                self.right_deep_3[key] = self.right_deep_3[key] + 1
                self.right_deep_3["attempted"] = self.right_deep_3["made"] +  self.right_deep_3["missed"]
                self.right_deep_3["percent"] = self.right_deep_3["made"] / self.right_deep_3["attempted"]

            # Left Deep 3
            elif (row.LOC_Y < CourtDimensions.SIDE_BOUNDARY and row.LOC_Y > CourtDimensions.DEEP3_X) and \
                 (row.LOC_X > CourtDimensions.DEEP3_Y and row.LOC_X < CourtDimensions.HALFCOURT_BOUNDARY):
                self.left_deep_3[key] = self.left_deep_3[key] + 1
                self.left_deep_3["attempted"] = self.left_deep_3["made"] +  self.left_deep_3["missed"]
                self.left_deep_3["percent"] = self.left_deep_3["made"] / self.left_deep_3["attempted"]

    def process_shots_by_type(self, types_dict):
        """Process shot statistics by shot type (2-point vs 3-point) based on the provided DataFrame.

        Returns:
            dict: A dictionary containing shot statistics categorized by shot type.
        """
        # Initialize shot type statistics dictionary
        self.process_shots_by_mode(self.shot_types, self.df[["SHOT_TYPE", "EVENT_TYPE", "ACTION_TYPE"]], mode="type")

        # Calculate total shots attempted
        total_shots = self.df['SHOT_ATTEMPTED_FLAG'].sum()

        # Calculate frequency of each shot type
        self.process_column_frequency(self.types_dict, total_shots)

        # return self.shot_types

    def process_shots_by_breakdown(self, breakdowns_dict) -> dict:
        """Process shot statistics by detailed breakdown (e.g., jump shot, layup, dunk) based on the provided DataFrame.

        Returns:
            dict: A dictionary containing shot statistics categorized by detailed shot breakdown.
        """
        # Initialize shot breakdown statistics dictionary
        self.process_shots_by_mode(breakdowns_dict, self.df[["SHOT_TYPE", "EVENT_TYPE", "ACTION_TYPE"]], mode="breakdown")

        # Calculate total shots attempted
        total_shots = self.df['SHOT_ATTEMPTED_FLAG'].sum()

        # Calculate frequency of each detailed shot breakdown
        self.process_column_frequency(breakdowns_dict, total_shots)

        # return self.shot_types

    def process_shots_by_distance(self, distances_dict) -> OrderedDict:
        """Process shot statistics by shot distance based on the provided DataFrame.

        Returns:
            OrderedDict: An ordered dictionary containing shot statistics categorized by shot distance.
        """
        # Initialize shot distance statistics ordered dictionary
        self.process_shots_by_mode(distances_dict, self.df[["SHOT_DISTANCE", "EVENT_TYPE"]], mode="distance")

        # Calculate total shots attempted
        total_shots = self.df['SHOT_ATTEMPTED_FLAG'].sum()

        # Calculate frequency of each shot distance
        self.process_column_frequency(distances_dict, total_shots)

        # return self.shot_distances

    def process_shots_by_period(self, periods_dict) -> OrderedDict:
        """Process shot statistics by period (e.g., quarter) based on the provided DataFrame.

        Returns:
            OrderedDict: An ordered dictionary containing shot statistics categorized by period.
        """
        # Initialize period-based shot statistics ordered dictionary
        self.process_shots_by_mode(periods_dict, self.df[["PERIOD", "EVENT_TYPE"]], mode="period")

        # Calculate total shots attempted
        total_shots = self.df['SHOT_ATTEMPTED_FLAG'].sum()

        # Calculate frequency of shots attempted in each period
        self.process_column_frequency(periods_dict, total_shots)

        # return self.shot_periods


    def process_shots_by_mode(self, shots_dict: dict, mode: str):
        """Process shot statistics based on the specified mode and update the provided dictionary.

        Args:
            shots_dict (dict): A dictionary containing shot type statistics to be updated.
            mode (str): The mode of processing the shot statistics. Possible values are:
                - "type": Shot type (2-point vs 3-point).
                - "distance": Shot distance.
                - "breakdown": Detailed shot type breakdown.
        """
        for index, row in self.df.iterrows():
            if mode == "type":  # Shot Type (2Pt vs 3Pt)
                shot_type, event_type, action_type = row[:3]
                if "Layup" in action_type:
                    key = "Layup"
                elif "Dunk" in action_type:
                    key = "Dunk"
                else:
                    key = shot_type
            elif mode == "distance":  # Shot Distance
                distance, event_type = row[:2]
                if distance in range(0, 5):
                    key = "0 - 5"
                elif distance in range(5, 10):
                    key = "5 - 10"
                elif distance in range(10, 15):
                    key = "10 - 15"
                elif distance in range(15, 20):
                    key = "15 - 20"
                elif distance in range(20, 25):
                    key = "20 - 25"
                elif distance in range(25, 30):
                    key = "25 - 30"
                else:
                    key = "30+"
            elif mode == 'breakdown':  # Shot Breakdown (Detailed Shot Type)
                shot_type, event_type, action_type = row[:3]
                if action_type == "Jump Shot" and shot_type == "2PT Field Goal":
                    key = "Jump Shot Mid-Range"
                elif action_type == "Jump Shot" and shot_type == "3PT Field Goal":
                    key = "Jump Shot 3PT"
                elif "Dunk" in action_type:
                    key = "Dunk"
                elif "Floating" in action_type:
                    key = "Floater"
                elif "Hook Shot" in action_type:
                    key = "Hook Shot"
                elif "Fadeaway" in action_type and shot_type == "2PT Field Goal":
                    key = "Fadeaway Mid-Range"
                elif "Fadeaway" in action_type and shot_type == "3PT Field Goal":
                    key = "Fadeaway 3PT"
                elif ("Pullup" in action_type or "Pull-Up" in action_type) and shot_type == "2PT Field Goal":
                    key = "Pullup Mid-Range"
                elif ("Pullup" in action_type or "Pull-Up" in action_type) and shot_type == "3PT Field Goal":
                    key = "Pullup 3PT"
                elif "Step Back" in action_type and shot_type == "2PT Field Goal":
                    key = "Step Back Mid-Range"
                elif "Step Back" in action_type and shot_type == "3PT Field Goal":
                    key = "Step Back 3PT"
                elif "Layup" in action_type:
                    key = "Layup"
                else:
                    key = action_type
            else:
                key, event_type = row[:2]

            # Initialize shot statistics for the current key if not already present in the dictionary.
            if key not in shots_dict or shots_dict[key] == 0:
                keys = ["made", "missed", "attempted", "percent", "frequency"]
                shots_dict[key] = dict.fromkeys(keys, 0)
            
            # Collect made vs. missed shots
            if event_type == "Made Shot":
                shots_dict[key]["made"] += 1
            elif event_type == "Missed Shot":
                shots_dict[key]["missed"] += 1

            # Record attempted shots and shooting percentage
            shots_dict[key]["attempted"]  = shots_dict[key]["made"] + shots_dict[key]["missed"]
            shots_dict[key]["percent"]  = shots_dict[key]["made"] / shots_dict[key]["attempted"]

    def process_column_frequency(self, shots_dict: dict, total_shots: int):
        """Calculate the frequency of each shot type in the given dictionary based on the total number of shots.

        Args:
            shots_dict (dict): A dictionary containing shot type statistics.
            total_shots (int): The total number of shots.
        """
        for key in shots_dict.keys():
            shots_dict[key]["frequency"] = shots_dict[key]["attempted"] / total_shots

    def is_shot_inside_3pt_arc(self, x: float, y: float, start_angle: float, end_angle: float) -> bool:
        """
        Checks if a given point (x, y) lies inside the three-point arc.

        Args:
            x (float): The x-coordinate of the point.
            y (float): The y-coordinate of the point.
            start_angle (float): The starting angle of the three-point arc.
            end_angle (float): The ending angle of the three-point arc.

        Returns:
            bool: True if the point is inside the three-point arc, False otherwise.
        """
        # Calculate the polar radius (r) from the origin (0, 0) to the point (x, y).
        polar_radius = math.sqrt(x * x + y * y)
        
        # Calculate the angle (Angle) from the positive x-axis to the line segment connecting (0, 0) and (x, y).
        if x != 0:
            angle = math.degrees(math.atan(y / x))
            if angle < 0:
                angle = 180 + angle
        else:
            angle = 90
    
        # Check if both conditions are met:
        #   1. The polar radius is less than the radius of the three-point arc.
        #   2. The angle is between the specified start_angle and end_angle.
        if angle >= start_angle and angle <= end_angle and polar_radius < CourtDimensions.RADIUS_3ARC:
            return True
        else:
            return False

