from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = "Python package to study conserved protein interactions"
LONG_DESCRIPTION = """TODO"""

setup(
    name="tools_proj",  # TODO - update name.
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Dariia Yehorova, Rory Crean",
    author_email="",  # TODO - Add whoever uploads to PyPI here
    # license="MIT", TODO - select.
    # url="", TODO - once name chosen.
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        "plotly",  # TODO - maybe remove, only for making figures.
        # TODO - add more.
    ],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
