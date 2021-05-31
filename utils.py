from datetime import datetime
from typing import Dict, Any
import matplotlib.dates as mdates


def format_field_for_pgn(match: Dict[str, Any], field: str):
    if match.get(field):
        return "[{} \"{}\"]\n".format(field, match.get(field))
    return ""


def to_pgn(match: Dict[str, Any]):
    pgn = ""

    keys = ["Event", "Site", "Date", "Round", "White", "Black", "Result", "UTCDate", "UTCTime", "WhiteElo", "BlackElo",
            "WhiteRatingDiff", "BlackRatingDiff", "WhiteTitle", "BlackTitle", "ECO", "Opening", "TimeControl",
            "Termination"]
    for key in keys:
        pgn += format_field_for_pgn(match, key)

    pgn_moves = "\n"
    for i in range(len(match.get("moves"))):
        if i % 2 == 0:
            pgn_moves += "{}. ".format(int(i / 2) + 1)
        pgn_moves += "{} ".format(match.get("moves")[i])
    pgn_moves += "{}\n\n".format(match.get("Result"))

    return pgn + pgn_moves


def number_choice(question, *choices, exit_choice=False):
    query_string = ""
    exit_number = -1

    n = 0
    for choice in choices:
        n += 1
        query_string += "\n{}. {}".format(n, choice)

    if exit_choice:
        n += 1
        exit_number = n

        query_string += "\n{}. {}".format(n, "Exit")

    while True:
        try:
            answer = int(input(question + query_string + "\nYour choice: "))
        except:
            answer = 0

        if answer == 0 or answer > len(choices):
            print("Invalid input, please try again.")
        else:
            if answer == exit_number:
                return -1
            return answer

def datetime_from_game(game):
    if game.get("UTCDate") and game.get("UTCTime"):
        dt = game.get("UTCDate") + "|" + game.get("UTCTime")
        return datetime.strptime(dt, '%Y.%m.%d|%H:%M:%S')
    elif game.get("UTCDate"):
        return datetime.strptime(game.get("UTCDate"), '%y.%m.%d')
    else:
        return datetime.strptime("0:0:0", '%H:%M:%S')


def match_result(game, player):
    result = game.get("Result")
    if result == "1/2-1/2":
        return 0.5
    if (game.get("White") == player and result == "1-0") or (game.get("Black") == player and result == "0-1"):
        return 1
    return 0


def xfmt(x, pos=None):
    ''' custom date formatting '''
    x = mdates.num2date(x)
    label = x.strftime('%m/%d/%Y')
    label = label.lstrip('0')
    return label


def player_color(player, game):
    return "White" if game.get("White") == player else "Black"


def opponent_color(player, game):
    return "Black" if game.get("White") == player else "White"


def player_elo(player, game):
    return int(game.get("{}Elo".format(player_color(player, game))))


def opponent_elo(player, game):
    return int(game.get("{}Elo".format(opponent_color(player, game))))


def opponent_name(player, game):
    return game.get(opponent_color(player, game))


def player_rating_diff(player, game):
    return int(game.get("{}RatingDiff".format(player_color(player, game))))


def str_match_result(player, game):
    res = match_result(game, player)
    if res == 1:
        return "won"
    elif res == 0:
        return "lost"
    else:
        return "drawn"
