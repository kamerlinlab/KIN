# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 24 and name CA, resid 33 and name CA 
set dash_radius, 0.3, interaction1 
set dash_color, teal, interaction1 
distance interaction2, resid 27 and name CA, resid 231 and name CA 
set dash_radius, 0.2766, interaction2 
set dash_color, teal, interaction2 
distance interaction3, resid 100 and name CA, resid 104 and name CA 
set dash_radius, 0.2766, interaction3 
set dash_color, teal, interaction3 
distance interaction4, resid 143 and name CA, resid 146 and name CA 
set dash_radius, 0.2649, interaction4 
set dash_color, teal, interaction4 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
