# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 95 and name CA, resid 98 and name CA 
set dash_radius, 0.3, interaction1 
set dash_color, br5, interaction1 
distance interaction2, resid 106 and name CA, resid 110 and name CA 
set dash_radius, 0.3, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 108 and name CA, resid 111 and name CA 
set dash_radius, 0.3, interaction3 
set dash_color, br1, interaction3 
distance interaction4, resid 126 and name CA, resid 130 and name CA 
set dash_radius, 0.3, interaction4 
set dash_color, br1, interaction4 
distance interaction5, resid 184 and name CA, resid 188 and name CA 
set dash_radius, 0.3, interaction5 
set dash_color, br1, interaction5 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
