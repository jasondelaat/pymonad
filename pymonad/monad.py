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

# pytype complains if Any isn't imported even though it's not used anywhere.
from typing import Any # pylint: disable=unused-import
from typing import Callable, Generic, TypeVar, Union

S = TypeVar('S') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

class Monad(Generic[T]):
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

    @classmethod
    def apply(cls, function):
        """ Supplies a cleaner interface for applicative functor/amap usage.

        Example:
          @curry(2)
          def add(a, b): return a + b

          x = Just(1)
          y = Just(2)

          (Maybe.apply(add)
                .to_arguments(x, y)
          ) # results in Just(3)

        Args:
          function: A regular function which returns non-monadic values.

        Returns:
          A monad object based on the input class with the wrapped
          function and a new method, 'to_arguments' which will apply
          the function.
        """
        class _Applicative(cls):
            """ An internal class which provides the 'to_arguments' method. """
            amap = cls.amap
            bind = cls.bind
            insert = cls.insert
            map = cls.map
            @staticmethod
            def to_arguments(*args):
                """ Applies arguments to the function wrapped by the call to the apply method.

                Args:
                  *args: a variable number of arguments to be supplied
                     to the function wrapped by a previous call to the
                     'apply method.

                Returns:
                  A monadic value of type 'cls'
                """
                result = cls.insert(function)
                for arg in args:
                    result = result.amap(arg)
                return cls(result.value, result.monoid)

        return _Applicative(None, None) # We don't actually care about the inputs here

    @classmethod
    def insert(cls, value: T) -> 'Monad[T]':
        """ Returns an instance of the Functor with 'value' in a minimum context.  """
        raise NotImplementedError

    def amap(self: 'Monad[Callable[[S], T]]', monad_value: 'Monad[S]') -> 'Monad[T]':
        """ Applies the function stored in the functor to the value inside 'functor_value'
        returning a new functor value.
        """
        return monad_value.map(self.value)

    def bind(self: 'Monad[S]', kleisli_function: Callable[[S], 'Monad[T]']) -> 'Monad[T]':
        """ Applies 'function' to the result of a previous monadic calculation. """
        raise NotImplementedError

    def join(self: 'Monad[Monad[T]]') -> 'Monad[T]':
        """ Unpacks a nested monad instance one level. """
        def _join(value):
            if isinstance(value, Monad): # pylint: disable=no-else-return
                return value
            else:
                raise TypeError(f'Cannot join() \'{self}\'')
        return self.bind(_join)

    def map(self: 'Monad[S]', function: Callable[[S], T]) -> 'Monad[T]':
        """ Applies 'function' to the contents of the functor and returns a new functor value. """
        raise NotImplementedError("'fmap' not defined.")

    def then(
            self: 'Monad[S]', function: Union[Callable[[S], T], Callable[[S], 'Monad[T]']]
    ) -> 'Monad[T]':
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
        result = self.map(function)
        try:
            return result.join()
        except (TypeError, AttributeError):
            return result
