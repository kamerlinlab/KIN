# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 1 and name CA, resid 262 and name CA 
set dash_radius, 0.0102, interaction1 
set dash_color, br5, interaction1 
distance interaction2, resid 25 and name CA, resid 28 and name CA 
set dash_radius, 0.0153, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 41 and name CA, resid 42 and name CA 
set dash_radius, 0.1525, interaction3 
set dash_color, br9, interaction3 
distance interaction4, resid 41 and name CA, resid 237 and name CA 
set dash_radius, 0.178, interaction4 
set dash_color, br5, interaction4 
distance interaction5, resid 48 and name CA, resid 141 and name CA 
set dash_radius, 0.2441, interaction5 
set dash_color, dash, interaction5 
distance interaction6, resid 64 and name CA, resid 68 and name CA 
set dash_radius, 0.0661, interaction6 
set dash_color, dash, interaction6 
distance interaction7, resid 81 and name CA, resid 108 and name CA 
set dash_radius, 0.0966, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 84 and name CA, resid 106 and name CA 
set dash_radius, 0.3, interaction8 
set dash_color, br1, interaction8 
distance interaction9, resid 98 and name CA, resid 185 and name CA 
set dash_radius, 0.122, interaction9 
set dash_color, br9, interaction9 
distance interaction10, resid 114 and name CA, resid 140 and name CA 
set dash_radius, 0.0407, interaction10 
set dash_color, br9, interaction10 
distance interaction11, resid 132 and name CA, resid 135 and name CA 
set dash_radius, 0.1271, interaction11 
set dash_color, br1, interaction11 
distance interaction12, resid 139 and name CA, resid 154 and name CA 
set dash_radius, 0.2847, interaction12 
set dash_color, dash, interaction12 
distance interaction13, resid 148 and name CA, resid 149 and name CA 
set dash_radius, 0.0305, interaction13 
set dash_color, br9, interaction13 
distance interaction14, resid 189 and name CA, resid 209 and name CA 
set dash_radius, 0.0102, interaction14 
set dash_color, dash, interaction14 
distance interaction15, resid 197 and name CA, resid 208 and name CA 
set dash_radius, 0.1424, interaction15 
set dash_color, dash, interaction15 
distance interaction16, resid 205 and name CA, resid 230 and name CA 
set dash_radius, 0.0102, interaction16 
set dash_color, br9, interaction16 
distance interaction17, resid 247 and name CA, resid 250 and name CA 
set dash_radius, 0.0203, interaction17 
set dash_color, dash, interaction17 
distance interaction18, resid 157 and name CA, resid 158 and name CA 
set dash_radius, 0.0, interaction18 
set dash_color, br9, interaction18 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
