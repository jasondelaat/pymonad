from distutils.core import setup

setup(
    name='PyMonad',
    version='1.0',
    author='Jason DeLaat',
    author_email='jason.delaat@gmail.com',
    packages=['pymonad', 'pymonad.test'],
    url='',
    license='LICENSE.txt',
    description='Collection of classes and interfaces for programming with monads.',
    long_description=open('README.txt').read(),
)
