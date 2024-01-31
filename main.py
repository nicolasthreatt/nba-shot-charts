# python main.py --player "Player Name" --team_nickname "TeamNickName" --game_date "m/dd/YYYY" --season "XXXX-YY" --plot_type 'shotchart' --shot_points
from classes.shotchart import ShotChart
from helpers.cli import parse_args
from helpers.plot_utils import display_shot_data
from helpers.shotchart_utils import fetch_shotchart_data
from helpers.shotchart_utils import find_team
from helpers.shotchart_utils import get_player_info
from helpers.shotchart_utils import process_shot_data

if __name__ == "__main__":
    args = parse_args()

    player = get_player_info(args.player) if args.player else 0
    team = find_team(team_abr=args.team_abr, team_fullname=args.team_fullname, team_nickname=args.team_nickname)

    shotchart_df = fetch_shotchart_data(args.season, args.season_type, args.game_date, team, player)
    if not shotchart_df.empty:
        shotchart = ShotChart(shotchart_df=shotchart_df)

        shotchart.process(
            zones=args.zones,
            points=args.points,
            shot_type=args.types,
            shot_distances=args.distances,
            shot_periods=args.periods
        )

        # Process and display the shots data based based on cmd args
        # process_shot_data(shotchart, args)
        display_shot_data(shotchart, args)
    else:
        exit("ERROR: Unable to fetch shotchart data.")
