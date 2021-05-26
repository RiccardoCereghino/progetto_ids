# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from iterators import select
from pgn_reader import generate_games


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    games_generator = generate_games("pgns/lichess_db_standard_rated_2013-01.pgn")

    search_params = {
        "White__eq": "BFG9k"
    }

    tournament = list(select(games_generator, **search_params))

    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
