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
    def div(y, x):
        return x / y

    async def long_id(x):
        await asyncio.sleep(1)
        return await Promise(lambda resolve, reject: resolve(x))

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
import pymonad.monad
import pymonad.tools

async def _awaitable_amap(awaiting_function, awaiting_value):
    try:
        function = await awaiting_function
        value = await awaiting_value
        return function(value)
    except Exception as e: # pylint: disable=invalid-name, broad-except
        return e

async def _awaitable_bind(_value, _function):
    try:
        value = await(_value)
        return await _function(value[0])
    except Exception as e: # pylint: disable=invalid-name, broad-except
        return e

async def _awaitable_catch(_value, _handler):
    try:
        value = await _value
        if isinstance(value, Exception): # pylint: disable=no-else-raise
            raise value
        else:
            return value
    except Exception as e: # pylint: disable=invalid-name, broad-except
        return _handler(e)

async def _awaitable_map(_value, _function):
    try:
        value = await _value
        return _function(value)
    except Exception as e: # pylint: disable=invalid-name, broad-except
        return e

async def _awaitable_then(_value, _function):
    try:
        value = await _value
        return await _function(value)
    except TypeError:
        return _function(value)

class _Promise(pymonad.monad.Monad):
    @classmethod
    def insert(cls, value):
        """ See Monad.insert. """
        return Promise(lambda resolve, reject: resolve(value))

    def amap(self, monad_value):
        """ See Monad.amap. """
        return self.__class__(_awaitable_amap(self, monad_value), None)

    def bind(self, kleisli_function):
        """ See Monad.bind. """
        return self.__class__(_awaitable_bind(self, kleisli_function), None)

    def catch(self, error_handler):
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
        return self.__class__(_awaitable_catch(self, error_handler), None)

    def map(self, function):
        """ See Monad.map. """
        return self.__class__(_awaitable_map(self.value, function), None)

    def then(self, function):
        """ See Monad.then. """
        return self.__class__(_awaitable_then(self, function), None)

    def __await__(self):
        return self.value.__await__()

def _reject(error):
    raise error

def Promise(function): # pylint: disable=invalid-name
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
    async def _awaitable(function):
        return function(pymonad.tools.identity, _reject)
    return _Promise(_awaitable(function), None)

Promise.insert = _Promise.insert
Promise.apply = _Promise.apply
