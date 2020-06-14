# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Adds operators to the Writer monad. """
from typing import TypeVar

import pymonad.monad
import pymonad.operators.operators
import pymonad.writer

M = TypeVar('M') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

class Writer(pymonad.operators.operators.MonadOperators, pymonad.writer.Writer[M, T]):
    """ See pymonad.operators.operators and pymonad.writer. """
