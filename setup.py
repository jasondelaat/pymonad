import setuptools

with open('README.rst', 'r') as readme:
    long_description = readme.read()

with open('LICENSE.rst', 'r') as license_file:
    license_text = license_file.read()

setuptools.setup(
    name='PyMonad',
    version='2.0.0',
    author='Jason DeLaat',
    author_email='jason.develops@gmail.com',
    packages=setuptools.find_packages(),
    url='https://bitbucket.org/jason_delaat/pymonad',
    license=license_text,
    description='Data structures and utilities for monadic style functional programming.',
    long_description= long_description,
    long_description_content_type='text/x-rst',
    classifiers=[ "Intended Audience :: Developers"
                  , "License :: OSI Approved :: BSD License"
                  , "Operating System :: OS Independent"
                  , "Programming Language :: Python :: 3"
                  , "Topic :: Software Development"
                  , "Topic :: Software Development :: Libraries"
                  , "Topic :: Utilities"
    ],
    python_requires='>=3.7',
)
