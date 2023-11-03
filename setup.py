from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = "A python package to study conserved protein interaction networks"
LONG_DESCRIPTION = """
This repository contains the work done for the publication titled:
"Key Interaction Networks: Identifying Evolutionarily Conserved Non-Covalent
Interaction Networks Across Protein Families".

In this work, we studied the non-covalent interaction networks of all unique
class A beta-lactamases structures to identify a network of evolutionarily
conserved interactions present throughout the family.
"""

setup(
    name="key-interactions-network",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Dariia Yehorova, Rory Crean",
    author_email="",  # TODO - Add whoever uploads to PyPI here
    # url="", TODO - once name chosen.
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "jupyter",
        "scikit-learn",
        "scipy",
        "numpy",
        "pandas",
        "lxml",
        "MDAnalysis",
        "matplotlib",
        "plotly",
        "kaleido",
    ],
    extras_require={
        "dev": ["pytest", "black"],
    },
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
