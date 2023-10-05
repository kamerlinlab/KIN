Inside this folder, we compared our results to several existing methods and datasets, as well as studied our dataset in more detail.

The contents of each jupyter notebook and folder is explained below:

### Jupyter Notebooks

1. alternate_contacts_analysis.ipynb

2. comparison_analysis.ipynb

3. MSA_Comparisons.ipynb

4. structural_phylo_analysis.ipynb



TODO - can the others be removed?


###  Folders

#### comparison_results
This folders contains the output files/data generated from the analysis performed herein. This includes things like graphs/figures or scripts to project results onto protein structures.

#### coupling_strengths_data
We used the ev couplings webserver (https://v2.evcouplings.org/) to determine inferred coupling strengths between residue pairs for the target protein TEM1.

The recommended result was taken forward which had a bitscore of 0.5 and quality score of 10/10.
The file provided by the webserver "couplings/TARGET_b0.5_CouplingScores.csv" was downloaded and is saved here without modification.

TODO - check with Dariia if she is using this, if not, it can be removed.

#### msa_scores
TODO

TODO - move msa_scores folder to this section?

#### percentage_id_matrix
The percentage identity matrix for the 69 proteins used in this dataset was generated using the Clustal Omega webserver (https://www.ebi.ac.uk/Tools/msa/clustalo/).
The alignment file provided to the webserver is: "all_sequences.txt".
The default settings were used.
The percent identity matrix was downloaded as is and is saved as in the file: "percent_identity_matrix.txt"

#### tem1_fitness_data
Dataset of per residue fitness scores obtained from the publication:
https://academic.oup.com/mbe/article/31/6/1581/2925654

The original data (raw_experimental_data.xlsx) is included in this repository alongside the script used to reformat the data (process_tem1_data.py) and the extracted per residue fitness scores (per_res_fitness_scores.json).
