# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import pymonad.tools

id = pymonad.tools.identity
curry = pymonad.tools.curry

@curry(2)
def add(x, y):
    return x + y

@curry(2)
def mul(x, y):
    return x * y

@curry(2)
def sub(x, y):
    return x - y

class FunctorTests:
    def setUp(self):
        raise NotImplementedError('You need to set self._class to the monad class being tested.')

    def test_left_identity(self):
        self.assertEqual(self._class.insert(id(1)), self._class.insert(1))

    def test_rightidentity(self):
        self.assertEqual(id(self._class.insert(1)), self._class.insert(1))

    def test_apply_then_insert(self):
        self.assertEqual(
            self._class.insert(1).map(add(1)),
            self._class.insert(add(1, 1))
        )

    def test_composition(self):
        self.assertEqual(
            self._class.insert(1).map(lambda x: sub(2, add(1, x))),
            self._class.insert(1).map(add(1)).map(sub(2))
        )
