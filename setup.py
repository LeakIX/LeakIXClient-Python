from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='leakix',
    version='0.1.10',
    description='This lib add support to use the API from leakix.net',
    license='MIT',
    keywords=['python, package, distribution'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Danny Willems',
    url='https://github.com/LeakIX/LeakIXClient-Python',
    packages=['leakix'],
    scripts=['executable/cli.py'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6'
)
