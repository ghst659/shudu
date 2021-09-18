#!/usr/bin/env python3

import argparse
import logging
import sys
import typing

from board import Board, Symbol

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
    puzzle = Board()
    puzzle.from_json(args.json_path)
    print(puzzle)
    try:
        solution = solve(puzzle)
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

def solve(current: Board) -> Board:
    """Finds a solution to the puzzle."""
    try:
        row, col = first_empty(current)
    except BoardFullCondition:
        logging.info("board is full")
        return current
    else:
        possibles = open_moves(current, row, col)
        logging.info("[%s, %s] possible: %s", row, col, possibles)
        candidate = current.clone()
        for symbol in possibles:
            candidate[row, col] = symbol
            try:
                return solve(candidate)
            except NoMovesCondition:
                candidate[row, col] = Symbol.EMPTY
                logging.info("[%d, %d] = %s failed", row, col, symbol)
        raise NoMovesCondition(f"no moves at [{row}, {col}]")
            
def first_empty(current: Board) -> tuple[int, int]:
    """Returns a row, column tuple for the first empty cell."""
    for row in range(9):
        for col in range(9):
            if not current.get(row, col):
                return (row, col)
    raise BoardFullCondition("no empty cell")

def open_moves(b: Board, row: int, col: int) -> typing.Iterable[Symbol]:
    """Returns the possible Symbols for  at [ROW, COL]."""
    if b[row, col]:
        return frozenset()
    row_unused = frozenset(Symbol.unused(b.row(row)))
    col_unused = frozenset(Symbol.unused(b.col(col)))
    box_unused = frozenset(Symbol.unused(b.box(row, col)))
    return row_unused & col_unused & box_unused

if __name__ == "__main__":
    sys.exit(main(sys.argv))
