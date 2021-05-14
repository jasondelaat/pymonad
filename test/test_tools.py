# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest
from pymonad.tools import monad_from_none_or_value
from pymonad.maybe import Nothing, Some


class MonadFromNoneTests(unittest.TestCase):
    def test_with_none(self):
        option=monad_from_none_or_value(Nothing, Some, None)
        self.assertEqual(option, Nothing)

    def test_with_value(self):
        option=monad_from_none_or_value(Nothing, Some, 42)
        self.assertEqual(option, Some(42))
