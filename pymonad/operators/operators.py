# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Defines the monad operators.

The MonadOperators class allows users to create a monad alias for
any monad class with the operators __and__, __rmul__, and
__rshift__ defined.

  Example:
    class MaybeOp(MonadOperators, Maybe):
        pass

Nothing extra needs to be implemented to get the correct behaviour
unless the monad has multiple 'constructors' such as Just and
Nothing. In this case, we need to override those constructors as well:

  Example:
    def Just(value):
        return MaybeOp(value, True)
    Nothing = MaybeOp(None, False)
"""
import pymonad.monad

class MonadOperators(pymonad.monad.Monad): # pylint: disable=abstract-method
    """ Defines MonadOperators class.

    MonadOperators is a MonadAlias which is used to add operators for
    map (*), amap (&), and bind (>>) methods to Monad classes.
    """
    def __and__(self, monad_value):
        return self.amap(monad_value)

    def __rmul__(self, function):
        return self.map(function)

    def __rshift__(self, kleisli_function):
        return self.bind(kleisli_function)
