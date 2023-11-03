"""
Python script to process the experimental data provided for tem1
from the paper: https://academic.oup.com/mbe/article/31/6/1581/2925654

The per residue fitness scored are extracted from the dataset provided by the authors.
These are then stored as a json file for reuse.
"""
import json
import pandas as pd

EXP_DATA = "raw_experimental_data.xlsx"
PER_RES_FITNESS_FILE = "per_res_fitness_scores.json"
PER_MUTATION_FITNESS_FILE = "per_mutation_fitness.csv"


def main() -> None:
    """Process tem1 experimental data."""
    # per res fitness data workup.
    per_res_fitness_df = pd.read_excel(
        EXP_DATA, sheet_name="S4 k-star effective # of AA"
    )
    # After comparison, the TEM1 structure we are using starts from residue H24,
    # so those before are removed.
    # The final row is also removed, which is not a residue.
    drop_rows = list(range(0, 23)) + [286]
    per_res_fitness_df = per_res_fitness_df.drop(drop_rows, axis=0)

    # renumber so residue numbering matches tem1 pdb numbering.
    per_res_fitness = {}
    for res_numb, fitness in enumerate(list(per_res_fitness_df["k*"]), 1):
        per_res_fitness[res_numb] = fitness

    with open(PER_RES_FITNESS_FILE, "w", encoding="utf-8") as file_out:
        json.dump(per_res_fitness, file_out)

    # per mutation data workup
    per_mutation_fitness_df = pd.read_excel(
        EXP_DATA, sheet_name="S2 Missense mutation fitnesses"
    )
    drop_list = [
        "Sequencing Counts for each sub-library",
        "Unnamed: 4",
        "Unnamed: 5",
        "Unnamed: 6",
        "Unnamed: 7",
        "Unnamed: 8",
        "Unnamed: 9",
        "Unnamed: 10",
        "Unnamed: 11",
        "Unnamed: 12",
        "Unnamed: 13",
        "Unnamed: 14",
        "Unnamed: 15",
        "Total Counts",
        "Estimated error in fitness",
        "Ambler Position",
    ]
    per_mutation_fitness_df = per_mutation_fitness_df.drop(drop_list, axis=1)

    # drop residues not in pdb and summary results at end of file.
    drop_rows = list(range(0, 461)) + list(range(5721, 5741))
    per_mutation_fitness_df = per_mutation_fitness_df.drop(drop_rows, axis=0)

    # Add a column for residue numbering that matches pdb file numbering
    res_numbers = [item for item in list(range(1, 263 + 1)) for i in range(1, 20 + 1)]
    per_mutation_fitness_df.insert(loc=0, column="Residue Number", value=res_numbers)

    # drop columns with WT AA = mutant AA...
    per_mutation_fitness_df = per_mutation_fitness_df[
        per_mutation_fitness_df["WT AA"] != per_mutation_fitness_df["Mutant AA"]
    ]

    per_mutation_fitness_df.to_csv(PER_MUTATION_FITNESS_FILE, index=False)


if __name__ == "__main__":
    main()
