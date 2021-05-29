from itertools import tee, groupby
from typing import Iterator, Dict, Any

from iterators import select
from utils import to_pgn, datetime_from_game, match_result


def player_statistics(games: Iterator[Dict[str, Any]]):
    try:
        player = input("Player name: ")
    except:
        return

    player_games = filter(lambda x: x.get("White") == player or x.get("Black") == player, games)

    s = sorted(player_games, key=lambda x: datetime_from_game(x))

    win_streak = draw_streak = loss_streak = []
    n_games = score = 0
    for result, group in groupby(s, lambda x: match_result(x, player)):
        group = list(group)
        score += result * len(group)
        n_games += len(group)
        if result == 0:
            if len(group) > len(loss_streak):
                loss_streak = group
        elif result == 0.5:
            if len(group) > len(draw_streak):
                draw_streak = group
        else:
            if len(group) > len(win_streak):
                win_streak = group


    print("a")
    # win loss draw streak
    # total win loss draw
    # elo plot
    # best worst white opening
    # best worst black opening
    # best worst victory



def print_results(games: Iterator[Dict[str, Any]]):
    i = 0
    for game in games:
        i += 1
        print(to_pgn(game))
        if i == 10:
            break


def query_result(games: Iterator[Dict[str, Any]]):
    print("Write the query in the format: \"Key value\"")

    keys = ["Event", "Site", "Date", "Round", "White", "Black", "Result", "UTCDate", "UTCTime", "WhiteElo", "BlackElo",
            "WhiteRatingDiff", "BlackRatingDiff", "WhiteTitle", "BlackTitle", "ECO", "Opening", "TimeControl",
            "Termination"]
    print("List of keys: {}".format(keys))

    try:
        inp = input("Query: ")
        a = inp.split(" ")
        if a[0] in keys:
            key = a[0]
            value = a[1]
        else:
            raise Exception
    except:
        return

    search_params = {
        "{}__eq".format(key): value,
    }

    return select(games, **search_params)
