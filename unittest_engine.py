"""Engine tests using Python's stdlib `unittest` -- the closest thing to JUnit.

JUnit parallels (so it feels like home):
  class Foo(unittest.TestCase)   ~ a JUnit test class
  def test_xxx(self)             ~ @Test  (any method named test_* is auto-discovered)
  def setUp(self)                ~ @BeforeEach  (runs before EVERY test_* method)
  self.assertEqual(a, b)         ~ assertEquals(a, b)
  unittest.main()                ~ the JUnit runner

Run it either way:
  python unittest_engine.py
  python -m unittest unittest_engine
No external install -- unittest ships with Python (unlike pytest).
"""

import unittest

from mac import mac
from judge import judge


class TestMac(unittest.TestCase):
    """MAC primitive: two grids -> one score."""

    def setUp(self):
        # Fresh fixtures before each test. Clean 0/1 grids -> results are exact floats.
        self.cross = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
        self.x = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]

    def test_kernel_matches_itself(self):
        # Overlapping all five 1s -> 5.0
        self.assertEqual(mac(self.cross, self.cross), 5.0)
        self.assertEqual(mac(self.x, self.x), 5.0)

    def test_opposite_kernels_score_low(self):
        # Cross vs X overlap only at the center -> 1.0
        self.assertEqual(mac(self.cross, self.x), 1.0)

    def test_mac_is_symmetric(self):
        # mac(a, b) == mac(b, a): position-by-position product doesn't care about order.
        self.assertEqual(mac(self.cross, self.x), mac(self.x, self.cross))


class TestJudge(unittest.TestCase):
    """Judge: two scores -> 'a' / 'b' / 'tied'. (No grids here -- it works on scores.)"""

    def test_clear_winner(self):
        self.assertEqual(judge(5.0, 1.0), "a")  # first arg higher
        self.assertEqual(judge(1.0, 5.0), "b")  # second arg higher

    def test_exact_equal_is_tied(self):
        self.assertEqual(judge(0.9, 0.9), "tied")

    def test_within_epsilon_is_tied(self):
        # ~1e-16 gap (real data.json float noise): far under 1e-9 -> tied
        self.assertEqual(judge(0.9, 0.8999999999999999), "tied")

    def test_real_gap_is_not_tied(self):
        # 0.1 gap: a genuine difference, not noise -> a wins
        self.assertEqual(judge(0.9, 0.8), "a")


if __name__ == "__main__":
    unittest.main()
