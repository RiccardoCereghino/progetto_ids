from typing import Iterator, Dict, Any

from iterators import select
from player_statistics import w_d_l_streaks, plt_elo, opening_stats, extract_stats_from_games
from utils import to_pgn, datetime_from_game


def player_statistics(games: Iterator[Dict[str, Any]]):
    try:
        player = input("Player name: ")
    except:
        return

    player_games = list(filter(lambda x: x.get("White") == player or x.get("Black") == player, games))

    games_by_date = sorted(player_games, key=lambda x: datetime_from_game(x))

    if games_by_date:
        w_d_l_streaks(player, games_by_date)

        extract_stats_from_games(player, games_by_date)

        plt_elo(player, games_by_date)

        opening_stats(player, player_games)
    else:
        print("No match found for the selected player")


def print_results(games: Iterator[Dict[str, Any]]):
    i = 0
    for game in games:
        i += 1
        print(to_pgn(game))
        if i == 10:
            break


def query_result(games: Iterator[Dict[str, Any]]):
    print("Write the query in the format: \"Key=value\"")

    keys = ["Event", "Site", "Date", "Round", "White", "Black", "Result", "UTCDate", "UTCTime", "WhiteElo", "BlackElo",
            "WhiteRatingDiff", "BlackRatingDiff", "WhiteTitle", "BlackTitle", "ECO", "Opening", "TimeControl",
            "Termination"]
    print("List of keys: {}".format(keys))

    try:
        inp = input("Query: ")
        a = inp.split("=")
        if a[0] in keys:
            key = a[0]
            value = a[1]
        else:
            print("Query format not supported")
            raise Exception
    except Exception:
        return games

    search_params = {
        "{}__eq".format(key): value,
    }

    return select(games, **search_params)


def save_to_file(games: Iterator[Dict[str, Any]]):
    f = open("result.pgn", "w")
    for game in games:
        f.write(to_pgn(game))
    f.close()

