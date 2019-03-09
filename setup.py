import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # Application name:
    name="paphra-table",
    version="1.0.1",
    author="Epaphradito Lugayavu",
    author_email="paphra.me@gmail.com",
    url="http://github.com/Paphra/PythonTable/",
    license="LICENSE.txt",
    description="Python Table. Best for rows in Dictionaries.",
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

)
