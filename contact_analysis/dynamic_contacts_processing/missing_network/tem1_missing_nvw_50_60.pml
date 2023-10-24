# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 14 and name CA, resid 20 and name CA 
set dash_radius, 0.1714, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 18 and name CA, resid 22 and name CA 
set dash_radius, 0.2762, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 22 and name CA, resid 29 and name CA 
set dash_radius, 0.2524, interaction3 
set dash_color, br1, interaction3 
distance interaction4, resid 22 and name CA, resid 45 and name CA 
set dash_radius, 0.2476, interaction4 
set dash_color, dash, interaction4 
distance interaction5, resid 28 and name CA, resid 48 and name CA 
set dash_radius, 0.1714, interaction5 
set dash_color, dash, interaction5 
distance interaction6, resid 31 and name CA, resid 44 and name CA 
set dash_radius, 0.281, interaction6 
set dash_color, br1, interaction6 
distance interaction7, resid 33 and name CA, resid 42 and name CA 
set dash_radius, 0.2762, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 35 and name CA, resid 37 and name CA 
set dash_radius, 0.1762, interaction8 
set dash_color, br1, interaction8 
distance interaction9, resid 35 and name CA, resid 38 and name CA 
set dash_radius, 0.2048, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 35 and name CA, resid 40 and name CA 
set dash_radius, 0.2143, interaction10 
set dash_color, br1, interaction10 
distance interaction11, resid 55 and name CA, resid 58 and name CA 
set dash_radius, 0.1905, interaction11 
set dash_color, br1, interaction11 
distance interaction12, resid 78 and name CA, resid 110 and name CA 
set dash_radius, 0.2619, interaction12 
set dash_color, br1, interaction12 
distance interaction13, resid 113 and name CA, resid 125 and name CA 
set dash_radius, 0.181, interaction13 
set dash_color, br9, interaction13 
distance interaction14, resid 148 and name CA, resid 155 and name CA 
set dash_radius, 0.1762, interaction14 
set dash_color, br1, interaction14 
distance interaction15, resid 204 and name CA, resid 208 and name CA 
set dash_radius, 0.2762, interaction15 
set dash_color, br1, interaction15 
distance interaction16, resid 205 and name CA, resid 209 and name CA 
set dash_radius, 0.1952, interaction16 
set dash_color, br1, interaction16 
distance interaction17, resid 213 and name CA, resid 216 and name CA 
set dash_radius, 0.181, interaction17 
set dash_color, br1, interaction17 
distance interaction18, resid 221 and name CA, resid 222 and name CA 
set dash_radius, 0.2952, interaction18 
set dash_color, br9, interaction18 
distance interaction19, resid 76 and name CA, resid 111 and name CA 
set dash_radius, 0.2286, interaction19 
set dash_color, br1, interaction19 
distance interaction20, resid 115 and name CA, resid 119 and name CA 
set dash_radius, 0.3, interaction20 
set dash_color, br1, interaction20 
distance interaction21, resid 147 and name CA, resid 152 and name CA 
set dash_radius, 0.2286, interaction21 
set dash_color, br1, interaction21 
distance interaction22, resid 21 and name CA, resid 25 and name CA 
set dash_radius, 0.2571, interaction22 
set dash_color, br1, interaction22 
distance interaction23, resid 22 and name CA, resid 44 and name CA 
set dash_radius, 0.1952, interaction23 
set dash_color, br1, interaction23 
distance interaction24, resid 122 and name CA, resid 126 and name CA 
set dash_radius, 0.2857, interaction24 
set dash_color, br1, interaction24 
distance interaction25, resid 177 and name CA, resid 180 and name CA 
set dash_radius, 0.1667, interaction25 
set dash_color, br1, interaction25 
distance interaction26, resid 225 and name CA, resid 246 and name CA 
set dash_radius, 0.1667, interaction26 
set dash_color, br9, interaction26 
distance interaction27, resid 245 and name CA, resid 247 and name CA 
set dash_radius, 0.1905, interaction27 
set dash_color, br9, interaction27 
distance interaction28, resid 63 and name CA, resid 133 and name CA 
set dash_radius, 0.181, interaction28 
set dash_color, br9, interaction28 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
