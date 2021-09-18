#!/usr/bin/env python3

import argparse
import logging
import sys
import typing

import board

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
    b = board.Board()
    b.from_json(args.json_path)
    print(b)
    try:
        solution = solve(b)
    except NoMovesCondition:
        logging.warning("no solution found")
        return 1
    else:
        print(solution)
        return 0

class BoardFullCondition(Exception):
    """Indicates that something was not found."""
    pass

class NoMovesCondition(Exception):
    """Indicates that no moves are available."""
    pass

def solve(b: board.Board) -> board.Board:
    """Finds a solution to the puzzle."""
    try:
        r, c = first_empty(b)
    except BoardFullCondition:
        logging.info("no empty cell")
        return b
    else:
        possibles = possible_symbols(b, r, c)
        logging.warning("(%s, %s) possible: %s", r, c, possibles)
        n = b.clone()
        for p in possibles:
            n[r, c] = p
            try:
                return solve(n)
            except NoMovesCondition:
                n[r, c] = board.Symbol.EMPTY
                logging.info("[%d, %d] = %s failed", r, c, p)
        raise NoMovesCondition(f"no moves at [{r}, {c}]")
            
def first_empty(b: board.Board) -> tuple[int, int]:
    """Returns a row, column tuple for the first empty cell, else None."""
    for r in range(9):
        for c in range(9):
            if not b.get(r, c):
                return (r, c)
    raise BoardFullCondition("no empty cell")

def possible_symbols(b: board.Board, r: int, c: int) -> typing.Iterable[board.Symbol]:
    """Returns an iterable of the possible symbols that can be inserted at (r,c)."""
    if b[r, c]:
        return frozenset()
    row_unused = frozenset(board.Symbol.unused(b.row(r)))
    col_unused = frozenset(board.Symbol.unused(b.col(c)))
    box_unused = frozenset(board.Symbol.unused(b.box(r, c)))
    return row_unused & col_unused & box_unused

if __name__ == "__main__":
    sys.exit(main(sys.argv))
