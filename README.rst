=======
PyMonad
=======

    :Author: Jason

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

1.2.3 From BitBucket
^^^^^^^^^^^^^^^^^^^^

Clone the project repository:

.. code:: bash

    git clone https://bitbucket.org/jason_delaat/pymonad.git

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

**Jason DeLaat** - *Primary Author\\/Maintainer* - `https://bitbucket.org/jason_delaat/ <https://bitbucket.org/jason_delaat/>`_

4 License
---------

This project is licensed under the 3-Clause BSD License. See
`LICENSE.rst <./LICENSE.rst>`_ for details.
