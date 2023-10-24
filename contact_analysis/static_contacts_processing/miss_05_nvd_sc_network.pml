# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 21 and name CA, resid 29 and name CA 
set dash_radius, 0.2089, interaction1 
set dash_color, br9, interaction1 
distance interaction2, resid 22 and name CA, resid 45 and name CA 
set dash_radius, 0.3, interaction2 
set dash_color, dash, interaction2 
distance interaction3, resid 32 and name CA, resid 182 and name CA 
set dash_radius, 0.2732, interaction3 
set dash_color, br9, interaction3 
distance interaction4, resid 50 and name CA, resid 260 and name CA 
set dash_radius, 0.1875, interaction4 
set dash_color, br5, interaction4 
distance interaction5, resid 118 and name CA, resid 203 and name CA 
set dash_radius, 0.1875, interaction5 
set dash_color, br9, interaction5 
distance interaction6, resid 208 and name CA, resid 247 and name CA 
set dash_radius, 0.1982, interaction6 
set dash_color, brightorange, interaction6 
distance interaction7, resid 245 and name CA, resid 247 and name CA 
set dash_radius, 0.2357, interaction7 
set dash_color, br9, interaction7 
distance interaction8, resid 28 and name CA, resid 48 and name CA 
set dash_radius, 0.2893, interaction8 
set dash_color, dash, interaction8 
distance interaction9, resid 29 and name CA, resid 31 and name CA 
set dash_radius, 0.2518, interaction9 
set dash_color, br9, interaction9 
distance interaction10, resid 80 and name CA, resid 110 and name CA 
set dash_radius, 0.2893, interaction10 
set dash_color, br9, interaction10 
distance interaction11, resid 18 and name CA, resid 281 and name CA 
set dash_radius, 0.1929, interaction11 
set dash_color, br9, interaction11 
distance interaction12, resid 21 and name CA, resid 274 and name CA 
set dash_radius, 0.1929, interaction12 
set dash_color, br9, interaction12 
distance interaction13, resid 185 and name CA, resid 245 and name CA 
set dash_radius, 0.2464, interaction13 
set dash_color, br9, interaction13 
distance interaction14, resid 219 and name CA, resid 276 and name CA 
set dash_radius, 0.225, interaction14 
set dash_color, br9, interaction14 
distance interaction15, resid 33 and name CA, resid 282 and name CA 
set dash_radius, 0.1875, interaction15 
set dash_color, br9, interaction15 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
