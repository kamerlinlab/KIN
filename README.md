# KIN - Key Interactions Network

This repository contains the work done for the publication titled: _"TODO"_


In this work we studied the non-covalent interaction networks of all unique class A $\beta$-lactamases structures to (among other things) identify a network of evolutionarily conserved interactions present throughout the class A $\beta$-lactamase family.

TODO - add nice overview picture here.


## The repository is broken up into several subfolders for different sections of the project:

#### 1. src
   This folder contains the instable portion of the code (Python) which was used during the project. This is made up of two sections:
      - A set of modules that enabled us to determine the non-covalent interactions present in the crystal structures and MD simulations.
      - A set of modules that were used to help us analyse the dataset we generated.

   [How to install this code is described below.](#dependencies-and-install)

#### 2. protein_prep
   In this folder we identify all unique $\beta$-lactamase structures with help of the [$\beta$-lactamase database](http://bldb.eu/). Then each crystal structure is put through a series of steps to clean it for both contact analysis and MD simulations.

   These steps included:
   - Removing ligands, cofactors, crystallisation artefacts etc...
   - Adding missing residues.
   - Adding hydrogens, optimising side chain conformations.
   - Defining protonation states.
   - solvation and neutralisation for MD simulations with [AmberMD](https://ambermd.org/).

#### 3. md_simulations
   This folder contains the input files used to run MD simulations of each $\beta$-lactamase alongside shell scripts used to submit these jobs onto a computing cluster.

#### 4. md_analysis
   TODO.

#### 5. network_analysis
   TODO

#### 6. contact_analysis
   TODO

#### 7. comparitive_data
   Inside this folder, we compared our results to several existing methods and datasets, as well as studied our dataset in more detail.

   [The folder has its own readme with more detailed information](https://github.com/kamerlinlab/tools-project/tree/main/comparitive_data#readme)




TODO folder msa_scores should be moved somewhere else I think.



## Dependencies and Install
The installable portion of this code was written using Python 3.10, and we recommend using the same version of Python or higher, as well as using a new virtual environment.

If you're using [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html), you can create a new virtual enviroment as follows:
```
conda create -n enviroment_name python=3.11
conda activate enviroment_name
```

To install the code you can use either of the following options:

**Option 1: Install with pip**
```
pip install TODO
```

**Option 2: Clone/Download Repo first and then run setup.py :**

```
cd TODO-main
python setup.py install
```

## License and Disclaimer

TODO - add one once decided. Likely same as kif.


## Citing this work
If you make use of this work [please cite our preprint:](TODO add link)

TITLE HERE TODO

Authors: Dariia Yehorova, Rory M. Crean, Peter M. Kasson and Shina Caroline Lynn Kamerlin

DOI: TODO

(once published this section will be updated with the link to the publication instead of the preprint).



## Issues/Questions/Contributions
All welcome. Please feel free to open an issue or submit a pull request as necessary where we can discuss.
You can also reach those of us responsible for maintaining the repository by email instead if you prefer:
- dyehorova3 [at] gatech.edu
- rory.crean [at] kemi.uu.se
