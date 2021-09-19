#!/usr/bin/env python3

import argparse
import collections.abc
import logging
import sys

import shudu

def main(argv: collections.abc.Sequence[str]) -> int:
    """Working harness for shudu."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("--board", metavar='JSON_FILE',
                        dest='json_path', 
                        help="Path to the board JSON setup.")
    parser.add_argument("-v","--verbose",
                        dest='verbose', action="store_true",
                        help="run verbosely")
    args = parser.parse_args(args=argv[1:])

    puzzle = shudu.Board()
    print(puzzle)
    filled = puzzle.solve()
    print(puzzle)

    print("#" * 80)

    puzzle.clear()
    puzzle.from_json(args.json_path)
    print(puzzle)
    if not puzzle.solve():
        print("no solution")
        return 1
    print(puzzle)
    dead_ends = 0
    for key, count in sorted(puzzle.stats()):
        print(key, ": ", count)
        if key.startswith("L"):
            dead_ends += count
    print("dead ends:", dead_ends)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
