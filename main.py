from choices import print_results, query_result, player_statistics, save_to_file
from pgn_reader import generate_games
from itertools import tee

from utils import number_choice

if __name__ == '__main__':

    """
    it_1, it_2 = tee(games_generator, 2)

    search_params = {
        "White__eq": "BFG9k",
    }

    tournament = select(it_1, **search_params)

    searched = list(search_moves(tournament, ["e4", "e6", "d4", "b6"]))

    openings = {}
    ss = sorted(it_2, key=lambda x: x['Opening'])
    for key, group in groupby(ss, lambda x: x.get("Opening")):
        openings[key] = list(group)

    openings_results = {}
    for opening, matches in openings.items():
        if not openings_results.get(opening):
            openings_results[opening] = {
                "white_wins": 0,
                "draws": 0,
                "black_wins": 0
            }

        for match in matches:
            if match.get("Result") == "1/2-1/2":
                openings_results[opening]["draws"] += 1
            elif match.get("Result") == "1-0":
                openings_results[opening]["white_wins"] += 1
            else:
                openings_results[opening]["black_wins"] += 1
    """
    it = generate_games("pgns/lichess_db_standard_rated_2013-01.pgn")
    while True:
        # "Opening statistics",

        choice = number_choice(
            "Select operation to perform, -1 to exit",
            "Print first 10 results",
            "Query result",
            "Player statistics",
            "Save results to file",
            "Reset search"
        )
        if choice == 1:
            print("\n#########################\n")
            print_results(tee(it, 1)[0])
            print("\n#########################\n")
        elif choice == 2:
            it = query_result(it)
        elif choice == 3:
            print("\n#########################\n")
            player_statistics(tee(it, 1)[0])
            print("\n#########################\n")
        elif choice == 4:
            save_to_file(tee(it, 1)[0])
        elif choice == 5:
            it = generate_games("pgns/lichess_db_standard_rated_2013-01.pgn")
        elif choice == -1:
            print("Bye...")
            break
