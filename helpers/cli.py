import argparse
from helpers.shotchart_utils import CURRENT_SEASON
from helpers.shotchart_utils import get_game_date


def parse_args():
    parser = argparse.ArgumentParser(description='Shotchart Command Line Interface')

    parser.add_argument('--season', dest='season', type=str, metavar='', required=False,
                         default=CURRENT_SEASON,
                         help="Season which game was played")

    parser.add_argument('--season_type', dest='season_type', nargs='+', type=str, metavar='', required=False,
                         choices=('Pre Season','Regular Season', 'All Star','Playoffs'),
                         default='Regular Season',
                         help="Teams' Season for Salary Cap Infomation")

    parser.add_argument('--game_date', dest='game_date', type=str, metavar='', required=False,
                         default=get_game_date(),
                         help="Date Game Played")

    parser.add_argument('--player', dest='player', type=str, metavar='', required=False,
                         help="Player's Full Name")

    parser.add_argument('--team_abr', dest='team_abr', type=str, metavar='', required=False,
                         default=None,
                         help="Team Abbreviation")

    parser.add_argument('--team_fullname', dest='team_fullname', type=str, metavar='', required=False,
                         default=None,
                         help="Team Full Name")

    parser.add_argument('--team_nickname', dest='team_nickname', type=str, metavar='', required=False,
                         default=None,
                         help="Team Nick Name")

    parser.add_argument('--plot_data', dest='plot_data', type=str, nargs='+', metavar='', required=False,
                         choices=('made', 'missed', 'attempted', 'percent', 'frequency'),
                         help='Columns to plot')
    
    parser.add_argument('--plot_type', dest='plot_type', type=str, metavar='', required=False,
                         choices=('shotchart', 'bar', 'pie', 'line'),
                         help="Plot Type")

    parser.add_argument('--zones', dest='zones', action='store_true', required=False,
                         help='Include Zones') 

    parser.add_argument('--shot_points', dest='shot_points', action='store_true', required=False,
                         help='')

    parser.add_argument('--shot_types', dest='shot_types', action='store_true', required=False,
                         help='')

    parser.add_argument('--shot_breakdown', dest='shot_breakdown', action='store_true', required=False,
                         help='')

    parser.add_argument('--shot_distances', dest='shot_distances', action='store_true', required=False,
                         help='') 

    parser.add_argument('--shot_periods', dest='shot_periods', action='store_true', required=False,
                         help='') 

    return parser.parse_args()
