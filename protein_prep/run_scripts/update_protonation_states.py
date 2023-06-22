"""
Script to rename pdb file residue name in a case where a protonation state is incorrect.
To use, simply add a new tuple to the list called: FIXES_REQUIRED.
"""
from typing import List
import re
import sys
import ast
import json
# This is the editable part of the script. Every change that needs to be made becomes a new list member here.
# tuple contents are: pdb_file_path, residue name and residue number (as a string).
FIXES_REQUIRED = []

problematic_res=(sys.argv[1])
my_tuple = json.loads(problematic_res)
structure_name = my_tuple[0].split(".")[0]
print(structure_name)
if structure_name=="4EWF_SPH-1_FH":
    res_1[1]=209


for res_1 in my_tuple[1]:
    res_name = res_1[0]
    res_indx = res_1[1]
    print("in prot.fix file:", structure_name, res_name, res_indx) 
    FIXES_REQUIRED.append((structure_name, str(res_name), str(res_indx))) 
	

# Non-adjustable parameters below.
# possible protontation state changes.
ALLOWED_CHANGES = {"ASP": "ASH", "GLU": "GLH", "HIS": "HIP", "LYS": "LYN"}
def edit_pdb_file(pdb_file:str, target_res_name:str, target_res_numb: str) -> List[list]:
    """Find the residue name to change, edit it and then store as a list to write out."""
    exchange_made = False # prints as warning if no exchange found...
    new_pdb_file = []

    with open(pdb_file) as file_in:
        for line in file_in:
            line_info = re.split("\s+", line)

            if "ATOM" in line:
                line_info = re.split("\s+", line)

                if (line_info[3] == target_res_name) and (line_info[5] == target_res_numb):
                    new_line = line.replace(target_res_name, ALLOWED_CHANGES[target_res_name])
                    new_pdb_file.append(new_line)
                    exchange_made = True
                else:
                    new_pdb_file.append(line)

            else:
                new_pdb_file.append(line)

    if not exchange_made:
        print(f"""Warning, no change was made for the file and params:
            {pdb_file, target_res_name, target_res_numb} """)

    return new_pdb_file

def main():
    for fix_item in FIXES_REQUIRED:
        file_path = "../2_reduce/"+fix_item[0]+".pdb"
        new_pdb_file = edit_pdb_file(pdb_file=file_path,
                                     target_res_name=fix_item[1],
                                     target_res_numb=fix_item[2])

        # Overwrite current file.
        with open(file_path, "w") as writer:
            for line in new_pdb_file:
                writer.write(line)

if __name__ == "__main__":
    main()
