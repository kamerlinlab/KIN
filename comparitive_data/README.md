This section of the repository houses dataset which can be used for comparing our methods results to.

Each unique dataset is stored in its own folder and briefly described below.


#### tem1_fitness_data
Dataset of per residue fitness scores obtained from the publication:
https://academic.oup.com/mbe/article/31/6/1581/2925654

The original data (raw_experimental_data.xlsx) is included in this repository alongside
the script used to reformat the data (process_tem1_data.py)
and the extracted per residue fitness scores (per_res_fitness_scores.json).


#### coupling_strengths_data
We used the program plmc to determine inferred coupling strengths between all pairs of positions.
plmc is a program written in C available from GitHub at: https://github.com/debbiemarkslab/plmc
The paper describing the software/method is: https://www.nature.com/articles/nbt.3769
