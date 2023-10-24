# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 22 and name CA, resid 44 and name CA 
set dash_radius, 0.2333, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 22 and name CA, resid 45 and name CA 
set dash_radius, 0.3, interaction2 
set dash_color, dash, interaction2 
distance interaction3, resid 221 and name CA, resid 222 and name CA 
set dash_radius, 0.2933, interaction3 
set dash_color, br9, interaction3 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
