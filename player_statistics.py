from itertools import groupby

from utils import match_result, datetime_from_game, player_elo, opponent_elo, opponent_name, str_match_result, \
    player_rating_diff
from matplotlib import pyplot as plt


def w_d_l_streaks(player, games):
    # win loss draw streak
    # total win loss draw
    win_streak = draw_streak = loss_streak = []
    n_wins = n_losses = n_draws = 0
    n_games = len(games)
    score = 0

    for result, group in groupby(games, lambda x: match_result(x, player)):
        group = list(group)
        score += result * len(group)
        if result == 0:
            n_losses += len(group)
            if len(group) > len(loss_streak):
                loss_streak = group
        elif result == 0.5:
            n_draws += len(group)
            if len(group) > len(draw_streak):
                draw_streak = group
        else:
            n_wins += len(group)
            if len(group) > len(win_streak):
                win_streak = group

    print("{} statistics".format(player))
    print("\tELO: {}".format(player_elo(player, games[-1])))
    print("\tTotal games: {}".format(
        n_games,
    ))
    print("\t\tWins: {} - Losses: {} - Draws: {}".format(n_wins, n_losses, n_draws))
    print("\t\tWin rate: {:.2f}% - Losing rate of {:.2f}% - Draw rate: {:.2f}%".format(
        n_wins / n_games * 100, n_losses / n_games * 100, n_draws / n_games * 100
    ))

    print("\t\tWin streak: {}\n\t\tLoss streak: {}\n\t\tDraw streak: {}".format(
        len(win_streak), len(loss_streak), len(draw_streak)
    ))


def extract_stats_from_games(player, games):
    f_name = opponent_name(player, games[0])
    f_elo = opponent_elo(player, games[0])
    max_elo = min_elo = player_elo(player, games[0])
    best_enemy = worst_enemy = [f_name, f_elo, ""]
    best_victory = [f_name, f_elo]
    best_draw = [f_name, f_elo]
    worst_defeat = [f_name, f_elo]
    mf_enemies = {}

    for game in games:
        p_elo = player_elo(player, game)
        o_elo = opponent_elo(player, game)
        o_name = opponent_name(player, game)
        result = match_result(game, player)

        max_elo = p_elo if p_elo > max_elo else max_elo
        min_elo = p_elo if p_elo < min_elo else min_elo

        if o_elo > best_enemy[1]:
            best_enemy = [o_name, o_elo, str_match_result(player, game)]

        if o_elo < worst_enemy[1]:
            worst_enemy = [o_name, o_elo, str_match_result(player, game)]

        if o_name in mf_enemies:
            mf_enemies[o_name] += 1
        else:
            mf_enemies[o_name] = 1

        if result == 1:
            best_victory = [o_name, o_elo] if o_elo > best_victory[1] else best_victory
        elif result == 0:
            worst_defeat = [o_name, o_elo] if o_elo < worst_defeat[1] else worst_defeat
        else:
            best_draw = [o_name, o_elo] if o_elo > best_draw[1] else best_draw

    mf_enemy = ""
    c = 0
    for k, v in mf_enemies.items():
        if v > c:
            mf_enemy = k
            c = v

    print("\t---------")
    print("\tAdvanced statistics")
    print("\t\tMax elo: {} - Min elo: {}".format(max_elo, min_elo))
    print("\t\tOpponent with highest elo: {} ({}), the match was {}".format(
        best_enemy[0], best_enemy[1], best_enemy[2]
    ))
    print("\t\tOpponent with lowest elo: {} ({}), the match was {}".format(
        worst_enemy[0], worst_enemy[1], worst_enemy[2]
    ))
    print("\t\tBest victory was against {} with ELO {}".format(best_victory[0], best_victory[1]))
    print("\t\tBest draw was against {} with ELO {}".format(best_draw[0], best_draw[1]))
    print("\t\tWorst defeat was against {} with ELO {}".format(worst_defeat[0], worst_defeat[1]))

    print("\t\tMost played opponent is: {} with {} matches".format(mf_enemy, c))


def opening_stats(player, games):
    white_games, black_games = [], []
    for game in games:
        if game.get("White") == player:
            white_games.append(game)
        elif game.get("Black") == player:
            black_games.append(game)

    if len(white_games) > 0:
        opening_stats_per_color(player, white_games, "White")
    if len(black_games) > 0:
        opening_stats_per_color(player, black_games, "Black")


def opening_stats_per_color(player, games, color):
    opening_stats = {}
    lll = filter(lambda x: x.get('Opening') is not None, games)
    s = sorted(lll, key=lambda x: x.get('Opening'))
    for opening, group in groupby(s, lambda x: x.get("Opening")):
        wins = draws = losses = rating_diff = 0
        for match in group:
            result = match_result(match, player)
            rating_diff += player_rating_diff(player, match)
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
            "winning_rate": wins / n_games * 100,
            "losing_rate": losses / n_games * 100,
            "drawing_rate": draws / n_games * 100,
            "rating_diff": rating_diff
        }

    best_opening, worst_opening, draw_opening, most_played_opening = {}, {}, {}, {}

    for name, stat in opening_stats.items():
        if best_opening.get("rating_diff") is None or stat.get("rating_diff") > best_opening.get("rating_diff"):
            best_opening = stat
            best_opening["opening_name"] = name
        if worst_opening.get("rating_diff") is None or stat.get("rating_diff") < worst_opening.get("rating_diff"):
            worst_opening = stat
            worst_opening["opening_name"] = name
        if draw_opening.get("drawing_rate") is None or stat.get("drawing_rate") > draw_opening.get("drawing_rate"):
            draw_opening = stat
            draw_opening["opening_name"] = name
        if most_played_opening.get("n_games") is None or stat.get("n_games") > most_played_opening.get("n_games"):
            most_played_opening = stat
            most_played_opening["opening_name"] = name

    print("\t---------")
    print("\tOpening statistics")

    print(
        "\t\t{} best opening with {} is: {} with a winning rate of {:.2f}% losing rate of {:.2f}%, drawing rate of {:.2f}%, played {} times, elo diff: {}".format(
            player, color, best_opening["opening_name"], best_opening["winning_rate"], best_opening["losing_rate"],
            best_opening["drawing_rate"], best_opening["n_games"], best_opening["rating_diff"]
        ))
    print(
        "\t\t{} worst opening with {} is: {} with a winning rate of {:.2f}% losing rate of {:.2f}%,drawing rate of {:.2f}%,  played {} times, elo diff: {}".format(
            player, color, worst_opening["opening_name"], worst_opening["winning_rate"], worst_opening["losing_rate"],
            worst_opening["drawing_rate"], worst_opening["n_games"], worst_opening["rating_diff"]
        ))
    print(
        "\t\t{} most drawable opening with {} is: {} with a winning rate of {:.2f}% losing rate of {:.2f}%,drawing rate of {:.2f}%,  played {} times, elo diff: {}".format(
            player, color, draw_opening["opening_name"], draw_opening["winning_rate"], draw_opening["losing_rate"],
            draw_opening["drawing_rate"], draw_opening["n_games"], draw_opening["rating_diff"]
        ))
    print(
        "\t\t{} most played opening with {} is: {} with a winning rate of {:.2f}% losing rate of {:.2f}%, drawing rate of {:.2f}%, played {} times, elo diff: {}".format(
            player, color, most_played_opening["opening_name"], most_played_opening["winning_rate"],
            most_played_opening["losing_rate"], most_played_opening["drawing_rate"], most_played_opening["n_games"],
            most_played_opening["rating_diff"]
        ))


def plt_elo(player, games):
    import matplotlib.dates as mdates
    s = sorted(games, key=lambda x: x['Event'])
    events = [(event, list(matches)) for event, matches in groupby(s, lambda x: x.get("Event"))]

    i = 0
    for event, matches in events:
        if len(matches) < 10:
            continue
        data = []
        i += 1
        for game in matches:
            data.append((datetime_from_game(game), player_elo(player, game)))

        data = list(sorted(data, key=lambda x: x[0]))
        real_data = []
        for _, d in groupby(data, lambda d: "{}-{}-{}".format(d[0].year, d[0].month, d[0].day)):
            real_data.append(list(sorted(d, key=lambda x: x[0]))[-1])

        real_data = list(sorted(real_data, key=lambda x: x[0]))

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
        plt.plot([d[0] for d in real_data], [d[1] for d in real_data], label=event)
        plt.legend()
        plt.gcf().autofmt_xdate()
        plt.show()
