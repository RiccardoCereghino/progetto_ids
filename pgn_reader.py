import re
from typing import Iterator, Dict, List


def file_reader(file_name: str) -> Iterator[str]:
    """Generates an iterator per line from a file encoded in utf8, specified with file_name"""
    for line in open(file_name, "r", encoding="utf8"):
        yield line


def generate_games(file: str) -> Iterator[Dict[str, str]]:
    """
    Iterates through a csv file (path), picks the first line to be used
    as keys for the yielded list of returning dict
    """
    line_gen = file_reader(file)

    game_lines = []
    start_moves = False

    for line in line_gen:
        if line != "\n":
            game_lines.append(line)
        else:
            if start_moves:
                yield convert_pgn(game_lines)
                game_lines = []
                start_moves = False

            else:
                start_moves = True


def convert_pgn(pgn: List[str]):
    key_pattern = "([^\\s]+)"
    value_pattern = r"[\"'][^\"']*[\"']"
    pgn_dict = {
        "moves": []
    }

    for line in pgn:
        if line.startswith("["):
            line = line[1:-1]
            key = re.search(key_pattern, line).group()
            pgn_dict[key] = re.search(value_pattern, line).group()[1:-1]
        else:
            splitted_line = line.split(" ")
            for e in splitted_line[:-1]:
                if not e.endswith(".") and not e == "{" and not e == "}" and not e.startswith("["):
                    if e.endswith("??") or e.endswith("!!") or e.endswith("?!") or e.endswith("!?"):
                        e = e[:-2]
                    if e.endswith("?") or e.endswith("!"):
                        e = e[:-1]
                    pgn_dict["moves"].append(e)

    return pgn_dict
