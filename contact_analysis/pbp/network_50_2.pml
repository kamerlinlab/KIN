# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 40 and name CA, resid 47 and name CA 
set dash_radius, 0.18, interaction1 
set dash_color, br5, interaction1 
distance interaction2, resid 117 and name CA, resid 121 and name CA 
set dash_radius, 0.18, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 124 and name CA, resid 128 and name CA 
set dash_radius, 0.18, interaction3 
set dash_color, br1, interaction3 
distance interaction4, resid 142 and name CA, resid 145 and name CA 
set dash_radius, 0.18, interaction4 
set dash_color, br9, interaction4 
distance interaction5, resid 158 and name CA, resid 162 and name CA 
set dash_radius, 0.18, interaction5 
set dash_color, br1, interaction5 
distance interaction6, resid 182 and name CA, resid 186 and name CA 
set dash_radius, 0.18, interaction6 
set dash_color, br1, interaction6 
distance interaction7, resid 183 and name CA, resid 187 and name CA 
set dash_radius, 0.3, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 184 and name CA, resid 188 and name CA 
set dash_radius, 0.18, interaction8 
set dash_color, br1, interaction8 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
