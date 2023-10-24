"""
Run crystal structure contact analysis for all systems.
"""
from tools_proj.contacts.contact_analysis import single_frame_contact_analysis

PARM_FILE = r"/storage/home/hhive1/dyehorova3/data/tools-project/contact_analysis/pbp/2z2l_apo.pdb"
COORD_FILE = r"/storage/home/hhive1/dyehorova3/data/tools-project/contact_analysis/pbp/2z2l_apo.pdb"

result_no_topo = single_frame_contact_analysis(  # topology_file=PARM_FILE,
    coordinates_file=COORD_FILE,
    out_file="2z2l.txt",
    first_res=1,
    last_res=385,
)
