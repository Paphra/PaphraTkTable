import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # Application name:
    name="paphra-tktable",
    version="1.0.4",
    author="Epaphradito Lugayavu",
    author_email="paphra.me@gmail.com",
    url="http://github.com/Paphra/PaphraTkTable/",
    license="LICENSE.txt",
    description="Python Tkinter Table. Designed to give the user the control over tables in Python",
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

)
