#!/usr/bin/env python3
from __future__ import annotations

import copy
import enum
import json
import logging
import typing

from collections.abc import Iterable, Sequence

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
    def cvt(cls, value: typing.Union[int, str]) -> Symbol:
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

    def empty_cells(self) -> tuple[tuple[int, int]]:
        """Returns the cells in the board that are still empty."""
        return tuple((r, c)
                     for r in range(9) for c in range(9)
                     if not self.get(r, c))

    def available_symbols(self, row: int, col: int) -> Iterable[Symbol]:
        """Returns the possible Symbols at [ROW, COL]."""
        if self.get(row, col):
            return frozenset()
        row_unused = frozenset(Symbol.unused(self.row(row)))
        col_unused = frozenset(Symbol.unused(self.col(col)))
        box_unused = frozenset(Symbol.unused(self.box(row, col)))
        return row_unused & col_unused & box_unused

    def fill(self, empties: Sequence[tuple[int, int]]) -> bool:
        """Fills the table, returning True if all empties were filled."""
        if not empties:
            return True
        row, col = empties[0]
        remaining_empties = empties[1:]
        possibles = self.available_symbols(row, col)
        for symbol in possibles:
            self.put(row, col, symbol)
            if self.fill(remaining_empties):
                return True
            else:
                self.put(row, col, Symbol.EMPTY)
        return False

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
