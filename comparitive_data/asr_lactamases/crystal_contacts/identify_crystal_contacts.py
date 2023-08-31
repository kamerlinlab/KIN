"""
Quick calculation and save of the crystal structure contacts for the 69 proteins
we are studying.
"""
from tools_proj.contacts.contact_analysis import single_frame_contact_analysis

OUT_FOLDER = r""
PDBS_FOLDER = r"../protein_prep/5_tleap/"
CRYSTAL_STRUCTS = ["3zdj", "4b88", "4c6y", "4c75"]

if __name__ == "__main__":
    for structure in CRYSTAL_STRUCTS:
        topology_file = PDBS_FOLDER + structure + "_apo.prmtop"
        coord_file = PDBS_FOLDER + structure + "_apo.inpcrd"
        out_file = OUT_FOLDER + structure + "_contacts.txt"

        results = single_frame_contact_analysis(
            out_file=out_file, coordinates_file=coord_file, topology_file=topology_file
        )
