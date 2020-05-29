# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Provides monad classes with operators.

The operators module overrides all base monad types and their aliases
with versions which support operators.

The defined operators are:
  &  - amap
  >> - bind
  *  - map

  Example:
    from pymonad.operators import Maybe, Just, Nothing
    from pymonad.tools import curry

    @curry(2)
    def add(x, y): return x + y

    @curry(2)
    def div(y, x):
        if y == 0:
            return Nothing
        else:
            return Just(x / y)

    # Equivalent to Maybe.apply(add).to_arguments(Just(1), Just(2))
    print(add * Just(1) & Just(2)) # Just 3

    # Equivalent to Maybe.insert(5).bind(div(2)).bind(div(0))
    print(Just(5) >> div(2) >> div(0)) # Nothing
"""
