from distutils.core import setup

setup(
    name='PyMonad',
    version='1.0dev',
    author='Jason DeLaat',
    author_email='jason.develops@gmail.com',
    packages=['pymonad', 'pymonad.test'],
    url='http://pypi.python.org/pypi/PyMonad',
    license=open('LICENSE.txt').read(),
    description='Collection of classes and interfaces for programming with monads.',
    long_description=open('README.txt').read(),
)
