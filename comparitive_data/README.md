This section of the repository houses dataset which can be used for comparing our methods results to.

Each unique dataset is stored in its own folder and briefly described below.


#### tem1_fitness_data
Dataset of per residue fitness scores obtained from the publication:
https://academic.oup.com/mbe/article/31/6/1581/2925654

The original data (raw_experimental_data.xlsx) is included in this repository alongside
the script used to reformat the data (process_tem1_data.py)
and the extracted per residue fitness scores (per_res_fitness_scores.json).


#### coupling_strengths_data
We used the ev couplings webserver (https://v2.evcouplings.org/) to determine inferred coupling strengths between residue pairs for the target protein TEM1.

The recommended result was taken forward which had a bitscore of 0.5 and quality score of 10/10.
The file provided by the webserver "couplings/TARGET_b0.5_CouplingScores.csv" was downloaded and is saved here without modification.


#### percentage_id_matrix
The percentage identity matrix for the 69 proteins used in this dataset was generated using the Clustal Omega webserver (https://www.ebi.ac.uk/Tools/msa/clustalo/).
The alingment file provided to the webserver is: "all_sequences.txt".
The default settings were used.
The percent identiy matrix was downloaded as is and is saved as in the file: "percent_identity_matrix.txt"
