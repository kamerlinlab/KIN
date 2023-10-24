# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 1 and name CA, resid 3 and name CA 
set dash_radius, 0.0094, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 1 and name CA, resid 262 and name CA 
set dash_radius, 0.0094, interaction2 
set dash_color, br5, interaction2 
distance interaction3, resid 23 and name CA, resid 232 and name CA 
set dash_radius, 0.0187, interaction3 
set dash_color, dash, interaction3 
distance interaction4, resid 25 and name CA, resid 28 and name CA 
set dash_radius, 0.0187, interaction4 
set dash_color, br1, interaction4 
distance interaction5, resid 41 and name CA, resid 237 and name CA 
set dash_radius, 0.1641, interaction5 
set dash_color, br5, interaction5 
distance interaction6, resid 48 and name CA, resid 141 and name CA 
set dash_radius, 0.225, interaction6 
set dash_color, dash, interaction6 
distance interaction7, resid 64 and name CA, resid 68 and name CA 
set dash_radius, 0.0656, interaction7 
set dash_color, dash, interaction7 
distance interaction8, resid 78 and name CA, resid 108 and name CA 
set dash_radius, 0.0844, interaction8 
set dash_color, br1, interaction8 
distance interaction9, resid 79 and name CA, resid 107 and name CA 
set dash_radius, 0.0891, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 81 and name CA, resid 108 and name CA 
set dash_radius, 0.0938, interaction10 
set dash_color, br1, interaction10 
distance interaction11, resid 84 and name CA, resid 106 and name CA 
set dash_radius, 0.2812, interaction11 
set dash_color, br1, interaction11 
distance interaction12, resid 106 and name CA, resid 109 and name CA 
set dash_radius, 0.3, interaction12 
set dash_color, br1, interaction12 
distance interaction13, resid 111 and name CA, resid 115 and name CA 
set dash_radius, 0.0141, interaction13 
set dash_color, br1, interaction13 
distance interaction14, resid 111 and name CA, resid 141 and name CA 
set dash_radius, 0.1734, interaction14 
set dash_color, br1, interaction14 
distance interaction15, resid 132 and name CA, resid 135 and name CA 
set dash_radius, 0.1313, interaction15 
set dash_color, br1, interaction15 
distance interaction16, resid 138 and name CA, resid 154 and name CA 
set dash_radius, 0.2719, interaction16 
set dash_color, br1, interaction16 
distance interaction17, resid 139 and name CA, resid 154 and name CA 
set dash_radius, 0.2719, interaction17 
set dash_color, dash, interaction17 
distance interaction18, resid 151 and name CA, resid 153 and name CA 
set dash_radius, 0.1688, interaction18 
set dash_color, dash, interaction18 
distance interaction19, resid 189 and name CA, resid 209 and name CA 
set dash_radius, 0.0047, interaction19 
set dash_color, dash, interaction19 
distance interaction20, resid 189 and name CA, resid 210 and name CA 
set dash_radius, 0.0, interaction20 
set dash_color, br1, interaction20 
distance interaction21, resid 197 and name CA, resid 208 and name CA 
set dash_radius, 0.1406, interaction21 
set dash_color, dash, interaction21 
distance interaction22, resid 232 and name CA, resid 263 and name CA 
set dash_radius, 0.0328, interaction22 
set dash_color, dash, interaction22 
distance interaction23, resid 243 and name CA, resid 248 and name CA 
set dash_radius, 0.0094, interaction23 
set dash_color, br1, interaction23 
distance interaction24, resid 247 and name CA, resid 250 and name CA 
set dash_radius, 0.0187, interaction24 
set dash_color, dash, interaction24 
distance interaction25, resid 120 and name CA, resid 124 and name CA 
set dash_radius, 0.0609, interaction25 
set dash_color, br1, interaction25 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
