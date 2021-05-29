from itertools import tee, groupby
from typing import Iterator, Dict, Any

from iterators import select
from utils import to_pgn, datetime_from_game, match_result, get_elo_for_player
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as tkr

def player_statistics(games: Iterator[Dict[str, Any]]):
    try:
        player = input("Player name: ")
    except:
        return

    player_games = list(filter(lambda x: x.get("White") == player or x.get("Black") == player, games))

    s = sorted(player_games, key=lambda x: datetime_from_game(x))

    # win loss draw streak
    # total win loss draw
    win_streak = draw_streak = loss_streak = []
    n_wins = n_losses = n_draws = 0
    n_games = 0
    score = 0
    for result, group in groupby(s, lambda x: match_result(x, player)):
        group = list(group)
        score += result * len(group)
        n_games += len(group)
        if result == 0:
            if len(group) > len(loss_streak):
                loss_streak = group
                n_losses += len(group)
        elif result == 0.5:
            if len(group) > len(draw_streak):
                draw_streak = group
                n_draws += len(group)
        else:
            if len(group) > len(win_streak):
                win_streak = group
                n_wins += len(group)

    def xfmt(x, pos=None):
        ''' custom date formatting '''
        x = mdates.num2date(x)
        label = x.strftime('%m/%d')
        label = label.lstrip('0')
        return label

    plt.plot([str(datetime_from_game(game)) for game in s], [get_elo_for_player(game, player) for game in s])

    plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=90)
    plt.gca().xaxis.set_major_formatter(tkr.FuncFormatter(xfmt))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=8))
    plt.gca().xaxis.set_minor_locator(mdates.DayLocator())

    plt.show()

    opening_stats = {}
    s = sorted(player_games, key=lambda x: x['Opening'])
    for opening, group in groupby(s, lambda x: x.get("Opening")):
        wins = draws = losses = 0
        for match in group:
            result = match_result(match, player)
            if result == 0:
                losses += 1
            elif result == 0.5:
                draws += 1
            else:
                wins += 1

        n_games = wins + draws + losses

        opening_stats[opening] = {
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "n_games": wins + draws + losses,
            "winning_rate": wins / n_games,
            "losing_rate": losses / n_games,
        }

    best_opening = worst_opening = most_played_opening = {}
    for name, stat in opening_stats.items():
        if best_opening.get("winning_rate") is None or stat.get("winning_rate") > best_opening.get("winning_rate"):
            best_opening["winning_rate"] = stat.get("winning_rate")
            best_opening["opening_name"] = name
        if worst_opening.get("losing_rate") is None or stat.get("losing_rate") > worst_opening.get("losing_rate"):
            worst_opening["losing_rate"] = stat.get("losing_rate")
            worst_opening["opening_name"] = name
        if most_played_opening.get("n_games") is None or stat.get("n_games") > most_played_opening.get("n_games"):
            most_played_opening["n_games"] = stat.get("n_games")
            most_played_opening["opening_name"] = name

    print("{} best opening is: {} with a winning rate of {} losing rate of {}, played {} times".format(
        player, best_opening["opening_name"], best_opening["winning_rate"], best_opening["losing_rate"], best_opening["n_games"]
    ))
    print("{} worst opening is: {} with a winning rate of {} losing rate of {}, played {} times".format(
        player, worst_opening["opening_name"], worst_opening["winning_rate"], worst_opening["losing_rate"], worst_opening["n_games"]
    ))
    print("{} most played opening is: {} with a winning rate of {} losing rate of {}, played {} times".format(
        player, most_played_opening["opening_name"], most_played_opening["winning_rate"], most_played_opening["losing_rate"],
        most_played_opening["n_games"]
    ))

    # best worst victory
    # elo plot


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
