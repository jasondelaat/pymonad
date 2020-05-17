# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the Monad base class.

The Monad base class is an abstract class which defines the operations
available on all monad instances. To create a new Monad instance,
users should create a class which inherits from Monad and provides
implementations for the methods map, amap, bind, and class method
insert. See the documentation for those methods for more information on
how to implement them properly.
"""

class Monad:
    """
    Represents a "context" in which calculations can be executed.

    You won't create 'Monad' instances directly. Instead, sub-classes implement
    specific contexts. Monads allow you to bind together a series of calculations
    while maintaining the context of that specific monad.

    """
    def __init__(self, value, monoid):
        """ Initializes the internal values of the monad instance.

        All monads can be expressed as a tuple, (a, m). Representing
        all monads internally in this canonical form allows for some
        interesting effects such as easily aliasing existing monads
        instances and, if desired, adding operators. Occasionally it
        also makes implementation of the monad methods itself easier.

        Args:
          value: if we think of monads as storing some data of
            interest plus some 'meta data', then 'value' is the data of
            interest. Exactly what 'value' is/means will depend on the
            specific context of the monad in question.
          monoid: this is the 'meta data' part. While implementers may
            use an instance of the Monoid class here it is not
            required. However, the value passed in here should be a type
            that can be treated as a monoid, such as integers; strings;
            lists; etc., in order to ensure that the monad laws are
            obeyed. This is not enforced but it will result in an
            incorrect implementation.
        """
        self.value = value
        self.monoid = monoid
        self.is_monad_value = True

    def fmap(self, function):
        """ Applies 'function' to the contents of the functor and returns a new functor value. """
        raise NotImplementedError("'fmap' not defined.")

    @classmethod
    def insert(cls, value):
        """ Returns an instance of the Functor with 'value' in a minimum context.  """
        raise NotImplementedError

    def amap(self, functor_value):
        """ Applies the function stored in the functor to the value inside 'functor_value'
        returning a new functor value.

        """
        raise NotImplementedError

    def get_value(self):
        """ Returns the value held by the Container. """
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def bind(self, function):
        """ Applies 'function' to the result of a previous monadic calculation. """
        raise NotImplementedError

    def then(self, function):
        """ Combines the functionality of bind and fmap.

        Instead of worrying about whether to use bind or fmap,
        users can just use the then method to chain function
        calls together. The then method uses attempts to use
        bind first and if that doesn't work, uses fmap
        instead.

        Args:
          function: A python function or lambda expression
            which returns either a build-in type (int, string,
            etc.) or an appropriate monad type (Maybe, Either,
            etc.)

        Returns:
          A monad value of the same type as 'self'
        """

        result = self.bind(function)
        try:
            result.is_monad_value # pylint: disable=pointless-statement
            return result
        except AttributeError:
            return self.map(function)
