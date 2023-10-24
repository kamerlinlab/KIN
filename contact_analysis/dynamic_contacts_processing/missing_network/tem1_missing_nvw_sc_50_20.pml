# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 110 and name CA, resid 129 and name CA 
set dash_radius, 0.2673, interaction1 
set dash_color, br9, interaction1 
distance interaction2, resid 65 and name CA, resid 206 and name CA 
set dash_radius, 0.2509, interaction2 
set dash_color, br9, interaction2 
distance interaction3, resid 225 and name CA, resid 246 and name CA 
set dash_radius, 0.2891, interaction3 
set dash_color, br9, interaction3 
distance interaction4, resid 18 and name CA, resid 31 and name CA 
set dash_radius, 0.2945, interaction4 
set dash_color, br9, interaction4 
distance interaction5, resid 22 and name CA, resid 44 and name CA 
set dash_radius, 0.2291, interaction5 
set dash_color, br1, interaction5 
distance interaction6, resid 22 and name CA, resid 45 and name CA 
set dash_radius, 0.2836, interaction6 
set dash_color, dash, interaction6 
distance interaction7, resid 190 and name CA, resid 245 and name CA 
set dash_radius, 0.2182, interaction7 
set dash_color, br9, interaction7 
distance interaction8, resid 21 and name CA, resid 29 and name CA 
set dash_radius, 0.3, interaction8 
set dash_color, br9, interaction8 
distance interaction9, resid 29 and name CA, resid 31 and name CA 
set dash_radius, 0.2455, interaction9 
set dash_color, br9, interaction9 
distance interaction10, resid 245 and name CA, resid 247 and name CA 
set dash_radius, 0.2509, interaction10 
set dash_color, br9, interaction10 
distance interaction11, resid 28 and name CA, resid 48 and name CA 
set dash_radius, 0.2727, interaction11 
set dash_color, dash, interaction11 
distance interaction12, resid 28 and name CA, resid 50 and name CA 
set dash_radius, 0.2127, interaction12 
set dash_color, brightorange, interaction12 
distance interaction13, resid 62 and name CA, resid 188 and name CA 
set dash_radius, 0.2291, interaction13 
set dash_color, br9, interaction13 
distance interaction14, resid 59 and name CA, resid 143 and name CA 
set dash_radius, 0.2182, interaction14 
set dash_color, br9, interaction14 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
