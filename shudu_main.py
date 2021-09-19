#!/usr/bin/env python3

import argparse
import logging
import sys
import typing

import shudu

def main(argv: typing.Sequence[str]) -> int:
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
    puzzle.from_json(args.json_path)
    print(puzzle)
    solution = shudu.solve(puzzle)
    if not solution:
        print("no solution")
        return 1
    print(solution)

    print("#" * 80)
    blank = shudu.Board()
    print(blank)
    filled = shudu.solve(blank)
    print(filled)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
