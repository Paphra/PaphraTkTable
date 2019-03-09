from distutils.core import setup

setup(
    # Application name:
    name="Python Table By Paphra",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Epaphradito Lugayavu",
    author_email="paphra.me@gmail.com",

    # Packages
    packages=["src"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/PythonTable_v010/",

    #
    license="LICENSE.txt",
    description="Python Table Creation. Best for rows in Dictionaries.",
    long_description=open("README.txt").read(),

)
