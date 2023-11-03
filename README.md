# KIN - Key Interaction Networks

This repository provides the tool Key Interaction Networks (KIN) for analyzing conserved interaction networks across families of protein structures.  It is described in the publication "Key Interaction Networks: Identifying Evolutionarily Conserved Non-Covalent Interaction Networks Across Protein Families".

This document both describes how to install and use the tool and provides data to reproduce the calculations performed in the accompanying paper.

In this work, we studied the non-covalent interaction networks of all unique class A $\beta$-lactamases structures to identify a network of evolutionarily conserved interactions present throughout the family.
![Presentation2_equaltext](https://github.com/kamerlinlab/KIN/assets/66267331/d08b7e2e-b7c4-4fcc-b569-75077b1b652e)

## Dependencies and Install
The installable portion of this code was written using Python 3.10, and we recommend using the same version of Python or higher, as well as using a new virtual environment.

If you're using [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html), you can create a new virtual environment as follows:
```
conda create -n environment_name python=3.11
conda activate environment_name
```

To install the code you can use either of the following options:

**Option 1: Install with pip**
```
pip install key-interactions-network
```

**Option 2: Clone/Download Repo first and then run setup.py :**

```
cd KIN-main
python setup.py install
```

## The repository is broken up into several subfolders for different sections of the project:

#### 1. src
   This folder contains the installable portion of the code (Python) which was used during the project. This is made up of two sections:
      - A set of modules that enabled us to determine the non-covalent interactions present in the crystal structures and MD simulations.
      - A set of modules that were used to help us analyse the dataset we generated.

   [How to install this code is described above.](#dependencies-and-install)

#### 2. protein_prep
   In this folder, we identify all unique $\beta$-lactamase structures with help of the [$\beta$-lactamase database](http://bldb.eu/). Then each crystal structure is put through a series of steps to clean it for both contact analysis and MD simulations.

   These steps included:
   - Removing ligands, cofactors, crystallisation artefacts etc...
   - Adding missing residues.
   - Adding hydrogens, optimising side chain conformations.
   - Defining protonation states.
   - solvation and neutralization for MD simulations with [AmberMD](https://ambermd.org/).
     
The automated workflow can be found in the protein_prep/run_files where Commands.sh is the connecting script for all preparation steps. 

#### 3. md_simulations
   This folder contains the input files used to run MD simulations of each $\beta$-lactamase alongside example shell scripts used to submit these jobs onto a computing cluster.
   
#### 4. md_analysis
   This folder contains the files used for a basic evaluation of the MD simulations that include measurments such as the RMSD and RMSF. 
   
#### 5. contact_analysis
   This folder contains contacts obtained from the crystal structure and MD runs of all structures. It also contains example scripts for the formation and analysis of shared interaction networks from static and MD contacts. This folder also provides an example of a workflow that outputs the network of evolutionary preserved interactions that are missing in the protein of interest. 

#### 6. comparative_data
   Inside this folder, we compared our results to several existing methods and datasets, as well as studied our dataset in more detail.

   [The folder has its own readme with more detailed information](https://github.com/kamerlinlab/tools-project/tree/main/comparative_data#readme)


## License and Disclaimer

This software is published under a GNU General Public License v2.0.

As this software was made in part by people employed by Georgia Tech University we must also clarify: “The software is provided “as is.” Neither the Georgia Institute of Technology nor any of its units or its employees, nor the software developers of KIN or any other person affiliated with the creation, implementation, and upkeep of the software’s code base, knowledge base, and servers (collectively, the “Entities”) shall be held liable for your use of the platform or any data that you enter. The Entities do not warrant or make any representations of any kind or nature with respect to the System, and the Entities do not assume or have any responsibility or liability for any claims, damages, or losses resulting from your use of the platform. None of the Entities shall have any liability to you for use charges related to any device that you use to access the platform or use and receive the platform, including, without limitation, charges for Internet data packages and Personal Computers. THE ENTITIES DISCLAIM ALL WARRANTIES WITH REGARD TO THE SERVICE,INCLUDING WARRANTIES OF MERCHANTABILITY, NON-INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE TO THE FULLEST EXTENT ALLOWED BY LAW.”


## Citing this work
If you make use of this work [please cite our preprint:](TODO add link)

Key Interaction Networks: Identifying Evolutionarily Conserved Non-Covalent Interaction Networks Across Protein Families

Authors: Dariia Yehorova, Rory M. Crean, Peter M. Kasson and Shina Caroline Lynn Kamerlin

DOI: TODO



## Issues/Questions/Contributions
All welcome. Please feel free to open an issue or submit a pull request as necessary where we can discuss.
You can also reach those of us responsible for maintaining the repository by email instead if you prefer:
- dyehorova3 [at] gatech.edu
- rory.crean [at] kemi.uu.se
