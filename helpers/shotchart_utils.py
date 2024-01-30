import argparse
import pandas as pd
from classes.shotchart import ShotChart
from datetime import datetime, timedelta
from nba_api.stats.endpoints import commonteamroster, shotchartdetail
from nba_api.stats.static import players, teams

CURRENT_SEASON = "2020-21"


def create_shotchart_df(season: str, season_type: str, game_date: str, team: dict, player: dict) -> pd.DataFrame:
    """Create a DataFrame containing shot chart data for a specific player or team.

    Args:
        season (str): The season in which the game was played.
        season_type (str): The type of season ('Pre Season', 'Regular Season', 'All Star', 'Playoffs').
        game_date (str): The date on which the game was played in the format 'mm/dd/yyyy'.
        team (dict): A dictionary containing information about the team.
        player (dict): A dictionary containing information about the player.

    Returns:
        pandas.DataFrame: DataFrame containing shot chart data.

    Raises:
        SystemExit: If no shot chart data is found for the specified team and date.
    """
    # Define ShotChart Dataframe Columns
    shotchart_columns = ['GRID_TYPE', 'GAME_ID', 'GAME_EVENT_ID', 'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_NAME', 'PERIOD',
                        'MINUTES_REMAINING', 'SECONDS_REMAINING', 'EVENT_TYPE', 'ACTION_TYPE', 'SHOT_TYPE', 'SHOT_ZONE_BASIC',
                        'SHOT_ZONE_AREA', 'HOT_ZONE_RANGE', 'SHOT_DISTANCE', 'LOC_X', 'LOC_Y', 'SHOT_ATTEMPTED_FLAG', 'SHOT_MADE_FLAG',
                        'GAME_DATE', 'HTM', 'VTM']

    # Create ShotChart Dataframe with Specified Columns
    shotchart_df = pd.DataFrame(columns=shotchart_columns)

    # Call ShotChartDetail API Endpoint
    player_id = player['id'] if player else 0
    shotchart_endpoint = shotchartdetail.ShotChartDetail(player_id=player_id, team_id=team['id'],
                                                         season_type_all_star=season_type, season_nullable=season,
                                                         context_measure_simple='FGA',
                                                         date_from_nullable=game_date)

    # Convert ShotChartDetail Endpoint to Dataframe
    endpoint_df = shotchart_endpoint.get_data_frames()[0]

    # Return the dataframe shotchart endpoint if found. Else, exit.
    if not endpoint_df.empty:
        shotchart_df = shotchart_df.append(endpoint_df)
        return shotchart_df
    else:
        exit("No shot chart found for {} on {}.".format(team['full_name'], game_date))


def get_player_info(player: str) -> dict:
    """Get information about an NBA player by full name.

    This function retrieves player information using the NBA API based on the provided player's full name.

    Parameters:
        player (str): Full name of the NBA player.

    Returns:
        dict: A dictionary containing the player's information if found.

    Raises:
        SystemExit: If the player information is not found, the script exits with an error message.
    """
    player_info = {}

    # Retrieve player information from the NBA API
    for data in players.find_players_by_full_name(player):
        player_info.update(data)
    
    # Return the player if found. Else, exit.
    if player_info:
        return player_info
    else:
        exit("Unable to find player. Please try again.")


def get_team_info_dataframe(team_id: int, season: str=CURRENT_SEASON) -> pd.DataFrame:
    """Get information about an NBA team as a Pandas DataFrame.

    This function retrieves team information using the NBA API based on the provided team ID and season.
    The information is returned as a Pandas DataFrame.

    Parameters:
        team_id (int): The unique identifier of the NBA team.
        season (str, optional): The season for which the information is desired. Defaults to CURRENT_SEASON.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the team's information.

    Raises:
        ValueError: If the provided team_id is invalid or if no data is available for the specified team and season.
    """
    try:
        # Retrieve team information from the NBA API
        team_info = commonteamroster.CommonTeamRoster(team_id=team_id, season=season)

        # Extract the data frame containing team information
        dfTeam = team_info.get_data_frames()[0]

        return dfTeam

    except ValueError as ve:
        # Raise an error if the team_id is invalid or no data is available
        raise ValueError(f"Error retrieving team information: {ve}")


def find_team(team_abr: str=None, team_fullname: str=None, team_nickname: str=None) -> dict:
    """Find information about an NBA team based on various criteria.

    This function searches for information about an NBA team based on the provided criteria:
        Team abbreviation (team_abr)
        Full team name (team_fullname)
        Team nickname (team_nickname)

    Parameters:
        team_abr (str, optional): The abbreviation of the NBA team.
        team_fullname (str, optional): The full name of the NBA team.
        team_nickname (str, optional): The nickname of the NBA team.

    Returns:
        dict: A dictionary containing information about the NBA team if found.

    Raises:
        SystemExit: If no team information is found based on the provided criteria, the script exits with an error message.
    """
    team = {}

    if team_abr:  # Find team by abbreviation
        data = teams.find_team_by_abbreviation(team_abr)
        team.update(data)
    elif team_fullname:  # Find team by full name
        for data in teams.find_teams_by_full_name(team_fullname):
            team.update(data)
    elif team_nickname:  # Find team by nickname
        for data in teams.find_teams_by_nickname(team_nickname):
            team.update(data)
    else:  # Exit if no team criteria is provided
        exit("No team submitted. Please try again.")

    # Return the team if found. Else, exit.
    if team:
        return team
    else:
        exit("Unable to find team. Please try again.")


def get_game_date() -> str:
    """Get the date of the previous day.

    This function calculates the date of the previous day and returns it in the format 'MM/DD/YYYY'.

    Returns:
        str: The date of the previous day in the format 'MM/DD/YYYY'.
    """
    # Calculate yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%m/%d/%Y')

    return yesterday_str


def process_shot_data(shotchart: ShotChart, shotchart_df: pd.DataFrame, args: argparse.Namespace):
    """Process shot data based on the provided ShotChart object, DataFrame, and arguments.

    Args:
        shotchart (ShotChart): An instance of the ShotChart class.
        shotchart_df (pd.DataFrame): DataFrame containing shot chart data.
        args (argparse.Namespace): Arguments controlling the processing (from argparse).
    """
    if args.shot_points:
        return shotchart.process_shots_by_points(shotchart_df)
    elif args.shot_types:
        return shotchart.process_shots_by_type(shotchart_df)
    elif args.shot_distances:
        return shotchart.process_shots_by_distance(shotchart_df)
    elif args.shot_periods:
        return shotchart.process_shots_by_period(shotchart_df)
    elif args.shot_breakdown:
        return shotchart.process_shots_by_breakdown(shotchart_df)
    elif args.zones:
        return shotchart.process_shots_by_zones(shotchart_df)
    else:
        return None
