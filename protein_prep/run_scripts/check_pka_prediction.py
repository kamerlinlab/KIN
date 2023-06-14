"""
Check the pka prediction summary section generated by propka.
Any non standard values are printed to the console.
"""
from typing import List
import re
import json
# Constant to be updated.
PKA_FILE = "NAME.pka"
OUT_FILE = "propka_check.log"
# histidine is not acidic, but same check performed (looking for high pka values).
ACIDIC_RESIDUES = ("ASP", "GLU", "C-", "HIS")
BASIC_RESIDUES = ("ARG", "LYS", "TYR", "N+")

def parse_pka_file(file_path: str) -> List[list]:
    """Reads in pka file and returns the summary section's contents. """
    relevant_part = False
    summary_section = []
    with open(file_path) as file_in:
        for line in file_in:

            # defines the end of the summary section
            if "--------------------------------------------------------------------------------------------------------" in line:
                relevant_part = False

            if relevant_part:
                summary_section.append(line)

            # defines the start of the summary section
            if "Group      pKa  model-pKa   ligand atom-type" in line:
                relevant_part = True

    return summary_section


def find_non_standard_predictions(summary_section: List[list]) -> List[list]:
    """
    Parse the predictions and find any outlier pkas.
    Store these for printing.
    """
    non_standard_predictions = []
    for line in summary_section:
        line_info = re.split("\s+", line)
        res_name, res_numb, pred_pka = line_info[1], line_info[2], line_info[4],

        if res_name in ACIDIC_RESIDUES:
            if float(pred_pka) >= 8.0: # allow +- 1 wiggle room.
                non_standard_predictions.append([res_name, res_numb, pred_pka])

        elif res_name in BASIC_RESIDUES:
            if float(pred_pka) <= 6.0: # allow +- 1 wiggle room.
                non_standard_predictions.append([res_name, res_numb, pred_pka])

    return non_standard_predictions

def main():
    summary_section = parse_pka_file(file_path=PKA_FILE)
    non_standard_predictions = find_non_standard_predictions(summary_section)
    if non_standard_predictions:
        with open(OUT_FILE, 'a') as file:
            file.write("Non standard pka predictions for file: {PKA_FILE}" + '\n')
            file.write(str(non_standard_predictions) + '\n')
        my_tuple =(PKA_FILE, non_standard_predictions) 
        my_tuple_str=json.dumps(my_tuple)
        #tuple_str=$(IFS='|'; echo "${my_tuple[*]}")
        #print(PKA_FILE)

        print(my_tuple_str)
        #print(f"Non standard pka predictions for file: {PKA_FILE}")
        #print(non_standard_predictions)
        #print("\n")

if __name__ == "__main__":
    main()
