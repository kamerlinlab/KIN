"""
Run crystal structure contact analysis for all systems.
"""
from tools_proj.contacts.contact_analysis import single_frame_contact_analysis

PARM_FILE = r"FILEPATH/STRUCTURE_apo_postleap.pdb"
COORD_FILE = r"FILEPATH/STRUCTURE_apo_postleap.pdb"

result_no_topo = single_frame_contact_analysis(  # topology_file=PARM_FILE,
    coordinates_file=COORD_FILE,
    out_file="STRUCTURE.txt",
    first_res=1,
    last_res=LAST_RES,
)
