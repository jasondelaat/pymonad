# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Adds operators to the Maybe monad. """
import pymonad.monad
import pymonad.maybe
import pymonad.operators.operators

class Maybe(pymonad.operators.operators.MonadOperators, pymonad.maybe.Maybe):
    """ See pymonad.operators.operators and pymonad.maybe. """

def Just(value): # pylint: disable=invalid-name
    """ A Maybe object representing the presence of an optional value. """
    return Maybe(value, True)

# A Maybe object representing the absence of an optional value.
Nothing = Maybe(None, False) # pylint: disable=invalid-name
