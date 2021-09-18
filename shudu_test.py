#!/usr/bin/env python3

import textwrap
import unittest

import shudu

class TestShudu(unittest.TestCase):
    def test_easy(self):
        data = [
	    0, 0, 6, 0, 1, 0, 0, 0, 0,
	    0, 7, 9, 0, 0, 0, 8, 2, 0,
	    0, 3, 4, 0, 7, 0, 6, 1, 9,
	    0, 0, 0, 6, 2, 1, 0, 0, 0,
	    3, 0, 5, 7, 0, 4, 1, 0, 8,
	    0, 0, 0, 5, 8, 3, 0, 0, 0,
	    4, 9, 3, 0, 5, 0, 2, 8, 0,
	    0, 5, 8, 0, 0, 0, 4, 7, 0,
	    0, 0, 0, 0, 4, 0, 5, 0, 0
        ]
        board = shudu.Board()
        board.ingest(data)
        got = shudu.solve(board)
        want = textwrap.dedent("""\
        -------------
        |286|419|357|
        |179|365|824|
        |534|278|619|
        -------------
        |847|621|935|
        |325|794|168|
        |961|583|742|
        -------------
        |493|157|286|
        |658|932|471|
        |712|846|593|
        -------------""")
        self.assertEqual(str(got), want)

    def test_medium(self):
        data = [
	    0, 9, 0, 0, 0, 4, 0, 0, 0,
	    0, 0, 0, 0, 0, 9, 3, 0, 0,
	    7, 0, 0, 3, 0, 0, 6, 0, 0,
	    2, 0, 0, 8, 9, 0, 5, 0, 0,
	    0, 4, 1, 0, 6, 0, 8, 2, 0,
	    0, 0, 8, 0, 2, 3, 0, 0, 7,
	    0, 0, 7, 0, 0, 8, 0, 0, 3,
	    0, 0, 2, 1, 0, 0, 0, 0, 0,
	    0, 0, 0, 2, 0, 0, 0, 1, 0
        ]
        board = shudu.Board()
        board.ingest(data)
        got = shudu.solve(board)
        want = textwrap.dedent("""\
        -------------
        |693|514|782|
        |825|679|341|
        |714|382|695|
        -------------
        |276|891|534|
        |341|765|829|
        |958|423|167|
        -------------
        |167|948|253|
        |432|156|978|
        |589|237|416|
        -------------""")
        self.assertEqual(str(got), want)

if __name__ == "__main__":
    unittest.main()
