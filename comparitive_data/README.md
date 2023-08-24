This section of the repository houses dataset which can be used for comparing our methods results to.

Each unique dataset is stored in its own folder and briefly described below.

#### asr_lactamases
Ancestral sequence reconstruction (ASR) has been previously been performed on class A beta-lactamses.
Crystal structures of several of these ASR enzymes were created.
In this folder, the asr crystal structures are prepared and analysed using the same process as was
performed for the other beta-lactmases. We then use this dataset to... TODO.


**ASR PDBs are as follows:**
- 4B88, 3ZDJ, from: https://doi.org/10.1021/ja311630a
- 4C6Y, 4C75 from: https://onlinelibrary.wiley.com/doi/epdf/10.1002/prot.24575

Basic idea:
Ancestrally reconstructed proteins.
The key conserved interactions are presereved in these structures...
Think about good metrics for this too...

If strong relationship relative to other proteins in the dataset,
then promising as these are very thermally stable?



#### coupling_strengths_data
We used the ev couplings webserver (https://v2.evcouplings.org/) to determine inferred coupling strengths between residue pairs for the target protein TEM1.

The recommended result was taken forward which had a bitscore of 0.5 and quality score of 10/10.
The file provided by the webserver "couplings/TARGET_b0.5_CouplingScores.csv" was downloaded and is saved here without modification.



#### tem1_fitness_data
Dataset of per residue fitness scores obtained from the publication:
https://academic.oup.com/mbe/article/31/6/1581/2925654

The original data (raw_experimental_data.xlsx) is included in this repository alongside
the script used to reformat the data (process_tem1_data.py)
and the extracted per residue fitness scores (per_res_fitness_scores.json).



#### percentage_id_matrix
The percentage identity matrix for the 69 proteins used in this dataset was generated using the Clustal Omega webserver (https://www.ebi.ac.uk/Tools/msa/clustalo/).
The alingment file provided to the webserver is: "all_sequences.txt".
The default settings were used.
The percent identiy matrix was downloaded as is and is saved as in the file: "percent_identity_matrix.txt"


TODO - move msa_scores folder to this section.