from distutils.core import setup

setup(
    name='PyMonad',
    version='1.3',
    author='Jason DeLaat',
    author_email='jason.develops@gmail.com',
    packages=['pymonad', 'pymonad.test'],
    url='https://bitbucket.org/jason_delaat/pymonad',
    license=open('LICENSE.txt').read(),
    description='Collection of classes for programming with functors, applicative functors and monads.',
    long_description=open('README.txt').read() + open("CHANGES.txt").read(),
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
