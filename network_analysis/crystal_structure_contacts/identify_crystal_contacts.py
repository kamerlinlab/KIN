"""
Quick calculation and save of the crystal structure contacts for the 69 proteins
we are studying.
"""
from tools_proj.contacts.contact_analysis import single_frame_contact_analysis

OUT_FOLDER = r"raw_contacts/"
PDBS_FOLDER = r"../../protein_prep/5_tleap/"
CRYSTAL_STRUCTS = r"../../file_list.txt"

if __name__ == "__main__":
    with open(CRYSTAL_STRUCTS, "r", encoding="utf-8") as file:
        crystal_structures = file.read().splitlines()

    for structure in crystal_structures:
        topology_file = PDBS_FOLDER + structure + "_apo.prmtop"
        coord_file = PDBS_FOLDER + structure + "_apo.inpcrd"
        out_file = OUT_FOLDER + structure + "_contacts.txt"

        results = single_frame_contact_analysis(
            out_file=out_file, coordinates_file=coord_file, topology_file=topology_file
        )
