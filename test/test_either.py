# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
import unittest

import common_tests
from pymonad.either import Either, Left, Right
from pymonad.either import Error, Result


class EitherTests(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(str(Right(9)), 'Right 9')
        self.assertEqual(str(Left(9)), 'Left 9')

    def test_insert(self):
        self.assertEqual(Either.insert(1), Right(1))

    def test_exceptions_wrapped_in_left_normal_function(self):
        self.assertEqual(
            str(Either.insert(1).then(lambda x: x / 0)),
            str(Left(ZeroDivisionError('division by zero')))
        )

    def test_exceptions_wrapped_in_left_kleisli_function(self):
        self.assertEqual(
            str(Either.insert(1).then(lambda x: Right(x / 0))),
            str(Left(ZeroDivisionError('division by zero')))
        )

    def test_either_extraction_with_Left_value(self):
        self.assertEqual(Left(TypeError()).either(lambda e: 'Left', lambda r: 'Right'), 'Left')

    def test_either_extraction_with_Right_value(self):
        self.assertEqual(Right(1).either(lambda e: 'Left', lambda r: 'Right'), 'Right')

class ErrorTests(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(str(Result(9)), 'Result: 9')
        self.assertEqual(str(Error(9)), 'Error: 9')

    def test_insert(self):
        self.assertEqual(Error.insert(1), Result(1))
        self.assertEqual(str(Error.insert(1)), 'Result: 1')

    def test_either_extraction_with_Left_value(self):
        self.assertEqual(Error(TypeError()).either(lambda e: 'Left', lambda r: 'Right'), 'Left')

    def test_either_extraction_with_Right_value(self):
        self.assertEqual(Result(1).either(lambda e: 'Left', lambda r: 'Right'), 'Right')

class EitherFunctor(common_tests.FunctorTests, unittest.TestCase):
    def setUp(self):
        self._class = Either

    def test_mapping_over_left(self):
        self.assertEqual(
            Left('').map(lambda x: x),
            Left('')
        )

class EitherApplicative(common_tests.ApplicativeTests, unittest.TestCase):
    def setUp(self):
        self._class = Either

    def test_applying_with_left_in_first_arg(self):
        self.assertEqual(
            Either.apply(common_tests.add).to_arguments(Left(''), Right(1)),
            Left('')
        )

    def test_applying_with_left_in_second_arg(self):
        self.assertEqual(
            Either.apply(common_tests.add).to_arguments(Right(1), Left('')),
            Left('')
        )

class EitherMonad(common_tests.MonadTests, unittest.TestCase):
    def setUp(self):
        self._class = Either

    def test_binding_with_left(self):
        self.assertEqual(
            Left('').bind(Either.insert),
            Left('')
        )

class EitherThen(common_tests.ThenTests, unittest.TestCase):
    def setUp(self):
        self._class = Either
