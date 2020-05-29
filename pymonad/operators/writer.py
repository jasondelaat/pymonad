# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Adds operators to the Writer monad. """
import pymonad.monad
import pymonad.writer
import pymonad.operators.operators

class Writer(pymonad.operators.operators.MonadOperators, pymonad.writer.Writer):
    """ See pymonad.operators.operators and pymonad.writer. """
