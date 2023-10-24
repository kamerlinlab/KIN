
#Order of commands to be run to go from generating contacts to the pymol projection onto TEM1

bash pdb_contacts.sh
bash msa_contacts.sh
python msa_network.py
python basic_pymol_projection.py
