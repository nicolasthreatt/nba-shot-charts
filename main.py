# python main.py --player "Player Name" --team_nickname "TeamNickName" --game_date "m/dd/YYYY" --season "XXXX-YY"
from classes.shotchart import ShotChart
from helpers.cli import parse_args
from helpers.plot_utils import display_shot_data
from helpers.shotchart_utils import create_shotchart_df
from helpers.shotchart_utils import find_team
from helpers.shotchart_utils import get_player_info
from helpers.shotchart_utils import process_shot_data

if __name__ == "__main__":
    args = parse_args()

    player = get_player_info(args.player) if args.player else 0
    team = find_team(team_abr=args.team_abr, team_fullname=args.team_fullname, team_nickname=args.team_nickname)

    shotchart_df = create_shotchart_df(args.season, args.season_type, args.game_date, team, player)
    if not shotchart_df.empty:
        shotchart = ShotChart(
            shotchart_df=shotchart_df,
            zones=args.zones, 
            points=args.shot_points,
            shot_type=args.shot_types,
            shot_distances=args.shot_distances,
            shot_periods=args.shot_periods
        )

        processed_data = process_shot_data(shotchart, shotchart_df, args)
        print(processed_data)
        display_shot_data(shotchart, processed_data, args)