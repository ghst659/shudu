#!/usr/bin/env python3
from __future__ import annotations

import copy
import enum
import json
import logging

from typing import Iterable, Sequence, Union

class Symbol(enum.Enum):
    """Cell values."""
    EMPTY = 0
    S1 = enum.auto()
    S2 = enum.auto()
    S3 = enum.auto()
    S4 = enum.auto()
    S5 = enum.auto()
    S6 = enum.auto()
    S7 = enum.auto()
    S8 = enum.auto()
    S9 = enum.auto()

    def __bool__(self) -> bool:
        return bool(self.value)

    def pp(self) -> str:
        return str(self.value) if self else " "

    @classmethod
    def cvt(cls, value: Union[int, str]) -> Symbol:
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                return cls.EMPTY
        for s in cls:
            if value == s.value:
                return s
        return cls.EMPTY

    @classmethod
    def unused(cls, symbols: Iterable[Symbol]) -> Iterable[Symbol]:
        """Returns a list of enums not in the given symbol set."""
        used_symbols = frozenset(symbols)
        return tuple(s for s in cls if s and s not in used_symbols)


class Board:
    """Representation of the board."""
    _cell: list[Symbol]

    def __init__(self):
        self._cell = [Symbol.EMPTY] * 81

    def clone(self):
        return copy.copy(self)

    @staticmethod
    def _i(row: int, col: int) -> int:
        if 0 <= row < 9 and 0 <= col < 9:
            return (9 * row) + col
        raise IndexError(f"invalid cell: ({row}, {col})")

    def get(self, row: int, col: int) -> Symbol:
        """Returns the value at ROW, COLUMN."""
        return self._cell[self._i(row, col)]

    def row(self, r: int) -> Sequence[Symbol]:
        """Returns the list of symbols in ROW."""
        return tuple(self.get(r, c) for c in range(9))

    def col(self, c: int) -> Sequence[Symbol]:
        """Gets the elements in the given COLUMN."""
        return tuple(self.get(r, c) for r in range(9))

    def box(self, row: int, col: int) -> Sequence[Symbol]:
        """Gets the elements in the box containing (ROW, COL)."""
        if not (0 <= row < 9 and 0 <= col < 9):
            raise IndexError(f"invalid cell: ({row}, {col})")
        br = row // 3
        bc = col // 3
        return tuple(self.get(r, c)
                     for r in range(br * 3, (br + 1) * 3)
                     for c in range(bc * 3, (bc + 1) * 3))

    def __getitem__(self, key: tuple[int, int]) -> Symbol:
        row, col = key
        return self.get(row, col)

    def put(self, row: int, col: int, value: Symbol):
        """Sets the value at ROW, COLUMN."""
        self._cell[self._i(row, col)] = value

    def __setitem__(self, key: tuple[int, int], value: Symbol):
        row, col = key
        self.put(row, col, value)

    def __str__(self) -> str:
        """String representation of the Board."""
        BAR = "-" * 13
        lines = [BAR]
        for row in range(9):
            line = ["|"]
            for col in range(9):
                x = self.get(row, col)
                line.append(x.pp())
                if col % 3 == 2:
                    line.append("|")
            lines.append("".join(line))
            if row % 3 == 2:
                lines.append(BAR)
        return "\n".join(lines)

    def ingest(self, ary: Sequence[int]):
        """Imports an array of values."""
        if len(ary) != 81:
            raise ValueError("wrong array length")
        for r in range(9):
            for c in range(9):
                self.put(r, c, Symbol.cvt(ary[self._i(r, c)]))

    def from_json(self, path: str):
        """Ingests the data at the JSONFILE."""
        with open(path, "r") as json_file:
            data = json.load(json_file)
        self.ingest(data["Board"])

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

def open_moves(b: Board, row: int, col: int) -> Iterable[Symbol]:
    """Returns the possible Symbols for  at [ROW, COL]."""
    if b[row, col]:
        return frozenset()
    row_unused = frozenset(Symbol.unused(b.row(row)))
    col_unused = frozenset(Symbol.unused(b.col(col)))
    box_unused = frozenset(Symbol.unused(b.box(row, col)))
    return row_unused & col_unused & box_unused

