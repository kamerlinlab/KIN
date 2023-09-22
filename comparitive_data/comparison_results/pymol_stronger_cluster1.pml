# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 5 and name CA, resid 9 and name CA 
set dash_radius, 0.2415, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 112 and name CA, resid 117 and name CA 
set dash_radius, 0.2415, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 214 and name CA, resid 234 and name CA 
set dash_radius, 0.2488, interaction3 
set dash_color, br1, interaction3 
distance interaction4, resid 218 and name CA, resid 230 and name CA 
set dash_radius, 0.2488, interaction4 
set dash_color, br1, interaction4 
distance interaction5, resid 220 and name CA, resid 228 and name CA 
set dash_radius, 0.2488, interaction5 
set dash_color, br1, interaction5 
distance interaction6, resid 3 and name CA, resid 7 and name CA 
set dash_radius, 0.2561, interaction6 
set dash_color, br1, interaction6 
distance interaction7, resid 4 and name CA, resid 8 and name CA 
set dash_radius, 0.2561, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 115 and name CA, resid 120 and name CA 
set dash_radius, 0.2634, interaction8 
set dash_color, br9, interaction8 
distance interaction9, resid 160 and name CA, resid 229 and name CA 
set dash_radius, 0.2634, interaction9 
set dash_color, br9, interaction9 
distance interaction10, resid 2 and name CA, resid 6 and name CA 
set dash_radius, 0.2707, interaction10 
set dash_color, br1, interaction10 
distance interaction11, resid 118 and name CA, resid 135 and name CA 
set dash_radius, 0.2854, interaction11 
set dash_color, br9, interaction11 
distance interaction12, resid 7 and name CA, resid 18 and name CA 
set dash_radius, 0.3, interaction12 
set dash_color, br9, interaction12 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
