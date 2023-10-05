# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 195 and name CA, resid 198 and name CA 
set dash_radius, 0.3, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 182 and name CA, resid 186 and name CA 
set dash_radius, 0.294, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 64 and name CA, resid 67 and name CA 
set dash_radius, 0.249, interaction3 
set dash_color, br1, interaction3 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
