
.. contents::

PyMonad implements data structures typically available in pure
functional or functional first programming languages like Haskell and
F#. Included are Monad and Monoid data types with several common
monads included - such as Maybe and State - as well as some useful
tools such as the @curry decorator for defining curried
functions. PyMonad 2.0.x represents and almost complete re-write of
the library with a simpler, more consistent interface as well as type
annotations to help ensure correct usage.

1 Getting Started
-----------------

These instructions will get you a copy of the project up and running
on your local machine for development and testing purposes.

1.1 Prerequisites
~~~~~~~~~~~~~~~~~

PyMonad requires Python 3.7+. If installing via ``pip`` then you
will also need `Pip <https://pypi.org/project/pip/>`_ and `Wheel <https://pypi.org/project/wheel/>`_ installed. See those projects for
more information on installing them if necessary.

Potential contributors should additionally install `pylint <https://pypi.org/project/pylint/>`_ and
`pytype <https://pypi.org/project/pytype/>`_ to ensure their code adheres to common style conventions.

1.2 Installing
~~~~~~~~~~~~~~

1.2.1 From the Python Package Index (PyPI) with pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From a command line run:

.. code:: bash

    pip install PyMonad

1.2.2 Manual Build from PyPI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download the project files from
`https://pypi.org/project/PyMonad/#files <https://pypi.org/project/PyMonad/#files>`_ and from the project
directory run:

.. code:: bash

    python setup.py install

If that doesn't work you may need to run the following instead.

.. code:: bash

    python3 setup.py install

1.2.3 From github
^^^^^^^^^^^^^^^^^

Clone the project repository:

.. code:: bash

    git clone https://github.com/jasondelaat/pymonad.git

Then from the project directory run ``setup.py`` as for the manual
build instructions above.

1.2.4 Example Usage
^^^^^^^^^^^^^^^^^^^

The following example imports the ``tools`` module and uses the
``curry`` function to define a curried addition function.

.. code:: python

    import pymonad.tools

    @pymonad.tools.curry(2) # Pass the expected number of arguments to the curry function.
    def add(x, y):
        return x + y

    # We can call add with all of it's arguments...
    print(add(2, 3)) # Prints '5'

    # ...or only some of them.
    add2 = add(2)  # Creates a new function expecting a single arguments
    print(add2(3)) # Also prints '5'

1.2.5 Next Steps
^^^^^^^^^^^^^^^^

The PyMonad documentation is a work in progress. For tutorials,
how-to, and more head over to the `PyMonad Documentation Project <https://jasondelaat.github.io/pymonad_docs/>`_.
If you'd like to contribute visit the documentation repository
`here <https://github.com/jasondelaat/pymonad_docs>`_.

1.3 Upgrading from PyMonad 1.3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you've used the 1.x versions of PyMonad you'll notice that
there are a few differences:

1.3.1 Curried functions
^^^^^^^^^^^^^^^^^^^^^^^

Currying functions in PyMonad version 1.x wrapped a function in
an instance of the Reader monad. This is no longer the case and
currying simply produces a new function as one might expect. 

The signature of ``curry`` has changed slightly. The new ``curry``
takes two arguments: the number of arguments which need to be
curried and the function.

.. code:: python

    from pymonad.tools import curry

    def add(x, y):
        return x + y

    curried_add = curry(2, add)
    # add = curry(2, add) # If you don't need access to the uncurried version.

``curry`` is itself a curried function so it can be used more
concisely as a decorator.

.. code:: python

    from pymonad.tools import curry

    @curry(2)
    def add(x, y):
        return x + y

1.3.2 Operators
^^^^^^^^^^^^^^^

Version 2 of PyMonad discourages the use of operators (>>, \\\*, and
&) used in version 1 so old code which uses them will
break. Operators have been removed from the default monad
implementation but are still available for users that still wish
to use them in the ``operators`` package. To use operators:

.. code:: python

    # Instead of this:
    # import pymonad.maybe

    # Do this:
    import pymonad.operators.maybe

While it's unlikely operators will be removed entirely, it is
strongly suggested that users write code that doesn't require
them.

1.3.3 Renamed Methods
^^^^^^^^^^^^^^^^^^^^^

The ``fmap`` method has been renamed to simply ``map`` and ``unit`` is now called ``insert``.

.. code:: python

    from pymonad.maybe import Maybe

    def add2(x):
        return x + 2

    m = (Maybe.insert(1)
         .map(add2)
    )

    print(m) # Just 3

1.3.4 Applicative Syntax
^^^^^^^^^^^^^^^^^^^^^^^^

Previously applicative syntax used the ``&`` operator or the ``amap``
method. ``amap`` still exists but there's now another way to use
applicatives: ``apply().to_arguments()``

.. code:: python

    from pymonad.tools import curry
    from pymonad.maybe import Maybe, Just

    @curry(2)
    def add(x, y):
        return x + y

    a = Just(1)
    b = Just(2)

    c  = Maybe.apply(add).to_arguments(a, b)
    print(c) # Just 3

If the function passed to ``apply`` accepts multiple arguments then
it *must* be a curried function.

1.3.5 New ``then`` method
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``then`` method combines the functionality of both ``map`` and
``bind``. It first tries to ``bind`` the function passed to it and,
if that doesn't work, tries ``map`` instead. It will be slightly
less efficient than using ``map`` and ``bind`` directly but frees
users from having to worry about specifically which functions are
being used where.

.. code:: python

    from pymonad.tools import curry
    from pymonad.maybe import Maybe, Just, Nothing

    @curry(2)
    def add_2(x, y):
        return x + y

    @curry(2)
    def div(y, x):
        if y == 0:
            return Nothing
        else:
            return Just(x / y)

    m = (Maybe.insert(2)
         .then(add(2)) # Uses map
         .then(div(4)) # Uses bind
    )

    print(m) # Just 1.0

1.3.6 Getting values out of ``Maybe`` and ``Either``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Previously, if you need to get a value out of a ``Maybe`` or an
``Either`` after a series of calculations you would have to access
the ``.value`` property directly. By the very nature of these two
monads, ``.value`` may not contain valid data and checking whether
the data is valid or not is the problem these monads are supposed
to solve. As of PyMonad 2.3.0 there are methods -- ``maybe`` and
``either`` -- for properly extracting values from these
monads.

Given a ``Maybe`` value ``m``, the ``maybe`` method takes a default
value, which will be returned if ``m`` is ``Nothing``, and a function
which will be applied to the value inside of a ``Just``.

.. code:: python

    from pymonad.maybe import Just, Nothing

    a = Just(2)
    b = Nothing

    print(a.maybe(0, lambda x: x)) # 2
    print(b.maybe(0, lambda x: x)) # 0

The ``either`` method works essentially the same way but takes two
functions as arguments. The first is applied if the value is a
``Left`` value and the second if it's a ``Right``.

.. code:: python

    from pymonad.either import Left, Right

    a = Right(2)
    b = Left('Invalid')

    print(a.either(lambda x: f'Sorry, {x}', lambda x: x)) # 2
    print(b.either(lambda x: f'Sorry, {x}', lambda x: x)) # Sorry, Invalid

2 Running the tests
-------------------

2.1 Unit Tests
~~~~~~~~~~~~~~

These tests primarily ensure that the defined monads and monoids
obey the required mathematical laws.

On most \*nix systems you should be able to run the automated tests
by typing the following at the command line.

.. code:: bash

    ./run_tests.sh

However, ``run_tests.sh`` is just a convenience. If the above doesn't
work the following should:

.. code:: bash

    python3 -m unittest discover test/

2.2 Style Tests
~~~~~~~~~~~~~~~

Contributors only need to run ``pylint`` and ``pytype`` over their
code and ensure that there are no glaring style or type
errors. PyMonad (mostly) attempts to adhere to the `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`_ 
and includes type hinting according to `PEP 484 <https://www.python.org/dev/peps/pep-0484/>`_.

In general, don't disable ``pylint`` or ``pytype`` errors for the
whole project, instead disable them via comments in the code. See
the existing code for examples of errors which can be disabled.

3 Authors
---------

**Jason DeLaat** - *Primary Author/Maintainer* - `https://github.com/jasondelaat/pymonad <https://github.com/jasondelaat/pymonad>`_

4 License
---------

This project is licensed under the 3-Clause BSD License. See
`LICENSE.rst <./LICENSE.rst>`_ for details.
