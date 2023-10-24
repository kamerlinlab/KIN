# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 22 and name CA, resid 44 and name CA 
set dash_radius, 0.1944, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 31 and name CA, resid 44 and name CA 
set dash_radius, 0.3, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 33 and name CA, resid 42 and name CA 
set dash_radius, 0.2667, interaction3 
set dash_color, br1, interaction3 
distance interaction4, resid 35 and name CA, resid 40 and name CA 
set dash_radius, 0.2333, interaction4 
set dash_color, br1, interaction4 
distance interaction5, resid 182 and name CA, resid 186 and name CA 
set dash_radius, 0.2222, interaction5 
set dash_color, br1, interaction5 
distance interaction6, resid 196 and name CA, resid 200 and name CA 
set dash_radius, 0.2778, interaction6 
set dash_color, br1, interaction6 
distance interaction7, resid 200 and name CA, resid 204 and name CA 
set dash_radius, 0.2222, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 22 and name CA, resid 45 and name CA 
set dash_radius, 0.25, interaction8 
set dash_color, dash, interaction8 
distance interaction9, resid 181 and name CA, resid 185 and name CA 
set dash_radius, 0.2611, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 199 and name CA, resid 203 and name CA 
set dash_radius, 0.1944, interaction10 
set dash_color, br1, interaction10 
distance interaction11, resid 221 and name CA, resid 222 and name CA 
set dash_radius, 0.2444, interaction11 
set dash_color, br9, interaction11 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
