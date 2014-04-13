from distutils.core import setup

setup(
    name='PyMonad',
    version='1.1',
    author='Jason DeLaat',
    author_email='jason.develops@gmail.com',
    packages=['pymonad', 'pymonad.test'],
    url='http://pypi.python.org/pypi/PyMonad',
    license=open('LICENSE.txt').read(),
    description='Collection of classes for programming with functors, applicative functors and monads.',
    long_description=open('README.txt').read(),
	classifiers=[ "Intended Audience :: Developers"
				, "License :: OSI Approved :: BSD License"
				, "Operating System :: OS Independent"
				, "Programming Language :: Python :: 2.7"
				, "Programming Language :: Python :: 3"
				, "Topic :: Software Development"
				, "Topic :: Software Development :: Libraries"
				, "Topic :: Utilities"
				],
)
