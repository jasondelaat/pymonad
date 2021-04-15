# --------------------------------------------------------
# (c) Copyright 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the Promise monad for ordering concurrent computations.

The Promise monad is based on (and named after) Javascript's Promise
objects and function in a similar way. Promises take asynchronous
computations and ensure the ordering of execution. In addition to the
standard operations on monads, Promises also provide a 'catch' method
which allows for recovery from errors.

  Example:
    import asyncio
    from pymonad.promise import Promise
    from pymonad.tools import curry

    @curry(2)
    def add(x, y):
        return x + y

    @curry(2)
    def div(y, x):
        return x / y

    async def long_id(x):
        await asyncio.sleep(1)
        return Promise(lambda resolve, reject: resolve(x))

    async def main():
        x = (Promise.insert(1)
                .then(long_id))
        y = (Promise
                .insert(2)
                .then(long_id)
                .then(div(0))            # Raises an error...
                .catch(lambda error: 2)) # ...which is dealth with here.
        print(
            await Promise.apply(add)
            .to_arguments(x, y)
            .catch(lambda error: 'Recovering...') # This is ignored
                                                  # because the previous
                                                  # catch already dealt
                                                  # with the error.
        )

    asyncio.run(main())

The above example will print the value '3' to the screen. The
'long_id' coroutine is a stand-in for any async operation that may
take some amount of time. When we await the Promise inside the print()
call it waits for both arguments to complete before calling 'add' with
the results. If the first call to 'catch' were removed then the error
would propagate and be caught by the second call. The program would
then print the string 'Recovering...' instead of '3'.

You can also create a Promise by passing a function directly. This
function takes two callbacks as input to signal a successful
computation or a failed one.

  Example:
    import asyncio

    def main():
        print(await Promise(lambda resolve, reject: resolve(2)))

    asyncio.run(main())

The 'resolve' callback can take a value of any type but the 'reject'
callback should always take an Exception as its argument.

  Example:
    import asyncio

    def main():
        print(await Promise(lambda resolve, reject: reject(IndexError())))

    asyncio.run(main())

When run, this program will crash having raised the IndexError without
catching it. Similarly, the catch method takes a function which
accepts an Exception as it's input.

  Example:
    import asyncio

    def main():
        print(await Promise(lambda resolve, reject: reject(IndexError()))
              .catch(lambda error: print(type(error)))
        )

    asyncio.run(main())

This program prints "<type 'IndexError'>" as its output.
"""
from typing import Callable, Generic, TypeVar, Union

import asyncio
import pymonad.monad
import pymonad.tools

S = TypeVar('S') # pylint: disable=invalid-name
T = TypeVar('T') # pylint: disable=invalid-name

ResolveFunction = Callable[[S], T]
RejectFunction = Callable[[Exception], T]
PromiseFunction = Callable[[ResolveFunction, RejectFunction], T]

def _reject(error):
    if not isinstance(error, Exception): # pylint: disable=no-else-raise
        raise Exception(str(error))
    else:
        raise error

class _Promise(pymonad.monad.Monad, Generic[T]):
    def __init__(self, value, monoid):
        super().__init__(value, monoid)
        self._resolve = pymonad.tools.identity

    @classmethod
    def insert(cls, value: T) -> '_Promise[T]':
        """ See Monad.insert. """
        return Promise(lambda resolve, reject: resolve(value))

    def amap(self: '_Promise[Callable[[S], T]]', monad_value: '_Promise[S]') -> '_Promise[T]':
        """ See Monad.amap. """
        async def _awaitable_amap(resolve, reject): # pylint: disable=unused-argument
            function = await self
            value = await monad_value
            return resolve(function(value))
        return self.__class__(_awaitable_amap, None)

    def bind(self: '_Promise[S]', kleisli_function: Callable[[S], '_Promise[T]']) -> '_Promise[T]':
        """ See Monad.bind. """
        if asyncio.iscoroutinefunction(kleisli_function):
            async def _bind(resolve, _):
                return await resolve(await kleisli_function(await self))
        else:
            async def _bind(resolve, _):
                return resolve(await kleisli_function(await self))
        return self.__class__(_bind, None)

    def catch(self: '_Promise[T]', error_handler: Callable[[Exception], T]) -> '_Promise[T]':
        """ Allows users to handle errors caused earlier in the Promise chain.

        The catch method takes an error handling function as input. If
        an earlier computation in the Promise chain has caused an
        error, either by being passed an Exception via the 'reject'
        callback or by an Exception being raised normally, then error
        handler is called with the Exception as an argument. If no
        error was previously raised, the error handler is ignored.

        Arguments:
          error_handler: a function which takes an Exception as input
            and can return any type.

        Returns:
          A new Promise object.
        """
        async def _awaitable_catch(resolve, reject): # pylint: disable=unused-argument
            try:
                value = await self
                return resolve(value)
            except Exception as e: # pylint: disable=invalid-name, broad-except
                return resolve(error_handler(e))

        return self.__class__(_awaitable_catch, None)

    def map(self: '_Promise[S]', function: Callable[[S], T]) -> '_Promise[T]':
        """ See Monad.map. """
        if asyncio.iscoroutinefunction(function):
            async def _map(resolve, _):
                return await resolve(function(await self))
        else:
            async def _map(resolve, _):
                return resolve(function(await self))
        return self.__class__(_map, None)

    def then(
            self: '_Promise[S]', function: Union[Callable[[S], T], Callable[[S], '_Promise[T]']]
    ) -> '_Promise[T]':
        """ See Monad.then. """
        if asyncio.iscoroutinefunction(function):
            async def _then(resolve, _):
                result = await function(await self)
                try:
                    return resolve(await result)
                except TypeError:
                    return resolve(result)
        else:
            async def _then(resolve, _):
                result = function(await self)
                try:
                    return resolve(await result)
                except TypeError:
                    return resolve(result)

        return self.__class__(_then, None)

    def __await__(self):
        return self.value(self._resolve, _reject).__await__()

def Promise(function: PromiseFunction) -> _Promise[T]: # pylint: disable=invalid-name
    """ Constructs a Promise object for ordering concurrent computations.

    Example:
      Promise(lambda resolve, reject: resolve('any value'))

      def some_computation(resolve, reject):
          if True:
              return resolve(10)
          else:
              reject(TypeError('Fake error.')) # doesn't need to be returned
      Promise(some_computation)

    Arguments:
      function: a function taking two callback typically called
        'resolve' and 'reject'. When the computation is successful the
        value should be returned by calling resolve with the result. If
        there is an error, call 'reject' with an instance of the
        Exception class.

    Returns:
      A new Promise object.
    """
    @pymonad.tools.curry(3)
    async def _awaitable(function, resolve, reject):
        return function(resolve, reject)
    return _Promise(_awaitable(function), None) # pylint: disable=no-value-for-parameter

Promise.apply = _Promise.apply
Promise.insert = _Promise.insert
