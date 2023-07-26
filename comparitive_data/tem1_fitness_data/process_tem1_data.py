"""
Python script to process the experimental data provided for tem1
from the paper: https://academic.oup.com/mbe/article/31/6/1581/2925654

The per residue fitness scored are extracted from the dataset provided by the authors.
These are then stored as a json file for reuse.
"""
import json
import pandas as pd

EXP_DATA = r"comparitive_data/tem1_fitness_data/raw_experimental_data.xlsx"
PROCESSED_FILE = r"comparitive_data/tem1_fitness_data/per_res_fitness_scores.json"


def main() -> None:
    """Process tem1 experimental data."""
    fitness_df = pd.read_excel(EXP_DATA, sheet_name="S4 k-star effective # of AA")

    # After comparison, the TEM1 structure we are using starts from residue H24,
    # so those before are removed.
    # The final row is also removed, which is not a residue.
    drop_rows = list(range(0, 23)) + [286]
    fitness_df = fitness_df.drop(drop_rows, axis=0)

    # renumber so residue numbering matches tem1 pdb numbering.
    per_res_fitness = {}
    for res_numb, fitness in enumerate(list(fitness_df["k*"]), 1):
        per_res_fitness[res_numb] = fitness

    # save file
    with open(PROCESSED_FILE, "w", encoding="utf-8") as file_out:
        json.dump(per_res_fitness, file_out)


if __name__ == "__main__":
    main()
