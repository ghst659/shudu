#!/usr/bin/env python3
from __future__ import annotations

import enum

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

    def pp(self) -> str:
        return " " if self == self.EMPTY else str(self.value)

    @classmethod
    def cvt(cls, value: str) -> Symbol:
        if value == " ":
            return cls.EMPTY
        if value == "1":
            return cls.S1
        if value == "2":
            return cls.S2
        if value == "3":
            return cls.S3
        if value == "4":
            return cls.S4
        if value == "5":
            return cls.S5
        if value == "6":
            return cls.S6
        if value == "7":
            return cls.S7
        if value == "8":
            return cls.S8
        if value == "9":
            return cls.S9
        raise ValueError(f"Invalid symbol: {value}")

class Board:
    """Representation of the board."""
    _cell: list[Symbol]

    def __init__(self):
        self._cell = [Symbol.EMPTY] * 81

    @classmethod
    def _i(cls, row: int, col: int) -> int:
        if 0 <= row < 9 and 0 <= col < 9:
            return (9 * row) + col
        raise IndexError(f"invalid cell: ({row}, {col})")

    def get(self, row: int, col: int) -> Symbol:
        """Returns the value at ROW, COLUMN."""
        return self._cell[self._i(row, col)]

    def row(self, r: int) -> list[Symbol]:
        """Returns the list of symbols in ROW."""
        return list(self.get(r, c) for c in range(9))

    def col(self, c: int) -> list[Symbol]:
        """Gets the elements in the given COLUMN."""
        return list(self.get(r, c) for r in range(9))

    def box(self, br: int, bc: int) -> list[Symbol]:
        """Gets the elements in the given box."""
        if not (0 <= br < 3 and 0 <= bc < 3):
            raise IndexError(f"invalid box: ({br}, {bc})")
        return list(self.get(r, c)
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
