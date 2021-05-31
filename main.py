from choices import print_results, query_result, player_statistics, save_to_file
from pgn_reader import generate_games
from itertools import tee

from utils import number_choice

if __name__ == '__main__':
    it = generate_games("pgns/lichess_db_standard_rated_2013-01.pgn")
    while True:
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
