# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Adds operators to the Writer monad. """
from typing import TypeVar

import pymonad.monad
import pymonad.operators.operators
import pymonad.writer

T = TypeVar('T') # pylint: disable=invalid-name

class Writer(pymonad.operators.operators.MonadOperators, pymonad.writer.Writer[T]): # pylint: disable=abstract-method
    """ See pymonad.operators.operators and pymonad.writer. """
