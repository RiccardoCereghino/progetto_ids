from datetime import datetime
from typing import Dict, Any


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
            pgn_moves += "{}. ".format(i / 2 + 1)
        pgn_moves += "{} ".format(match.get("moves")[i])
    pgn_moves += "{}\n".format(match.get("Result"))

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

        if answer <= 0 or answer > len(choices) + 1:
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

def get_elo_for_player(match, player):
    if match.get("White") == player:
        return int(match.get("WhiteElo"))
    else:
        return int(match.get("BlackElo"))
