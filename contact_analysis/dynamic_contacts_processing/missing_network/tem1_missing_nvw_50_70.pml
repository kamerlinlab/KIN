# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 18 and name CA, resid 22 and name CA 
set dash_radius, 0.2484, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 21 and name CA, resid 25 and name CA 
set dash_radius, 0.2203, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 22 and name CA, resid 44 and name CA 
set dash_radius, 0.1828, interaction3 
set dash_color, br1, interaction3 
distance interaction4, resid 22 and name CA, resid 45 and name CA 
set dash_radius, 0.2344, interaction4 
set dash_color, dash, interaction4 
distance interaction5, resid 31 and name CA, resid 44 and name CA 
set dash_radius, 0.2719, interaction5 
set dash_color, br1, interaction5 
distance interaction6, resid 33 and name CA, resid 42 and name CA 
set dash_radius, 0.2719, interaction6 
set dash_color, br1, interaction6 
distance interaction7, resid 35 and name CA, resid 38 and name CA 
set dash_radius, 0.1875, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 78 and name CA, resid 110 and name CA 
set dash_radius, 0.2297, interaction8 
set dash_color, br1, interaction8 
distance interaction9, resid 115 and name CA, resid 119 and name CA 
set dash_radius, 0.2812, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 122 and name CA, resid 126 and name CA 
set dash_radius, 0.2344, interaction10 
set dash_color, br1, interaction10 
distance interaction11, resid 146 and name CA, resid 150 and name CA 
set dash_radius, 0.1969, interaction11 
set dash_color, br1, interaction11 
distance interaction12, resid 147 and name CA, resid 152 and name CA 
set dash_radius, 0.1875, interaction12 
set dash_color, br1, interaction12 
distance interaction13, resid 186 and name CA, resid 190 and name CA 
set dash_radius, 0.2719, interaction13 
set dash_color, br1, interaction13 
distance interaction14, resid 200 and name CA, resid 204 and name CA 
set dash_radius, 0.3, interaction14 
set dash_color, br1, interaction14 
distance interaction15, resid 202 and name CA, resid 206 and name CA 
set dash_radius, 0.2719, interaction15 
set dash_color, br1, interaction15 
distance interaction16, resid 204 and name CA, resid 208 and name CA 
set dash_radius, 0.2437, interaction16 
set dash_color, br1, interaction16 
distance interaction17, resid 221 and name CA, resid 222 and name CA 
set dash_radius, 0.2672, interaction17 
set dash_color, br9, interaction17 
distance interaction18, resid 52 and name CA, resid 55 and name CA 
set dash_radius, 0.2156, interaction18 
set dash_color, br1, interaction18 
distance interaction19, resid 63 and name CA, resid 67 and name CA 
set dash_radius, 0.2391, interaction19 
set dash_color, br1, interaction19 
distance interaction20, resid 22 and name CA, resid 29 and name CA 
set dash_radius, 0.2344, interaction20 
set dash_color, br1, interaction20 
distance interaction21, resid 35 and name CA, resid 40 and name CA 
set dash_radius, 0.2109, interaction21 
set dash_color, br1, interaction21 
distance interaction22, resid 76 and name CA, resid 111 and name CA 
set dash_radius, 0.1828, interaction22 
set dash_color, br1, interaction22 
distance interaction23, resid 245 and name CA, resid 247 and name CA 
set dash_radius, 0.1828, interaction23 
set dash_color, br9, interaction23 
distance interaction24, resid 276 and name CA, resid 280 and name CA 
set dash_radius, 0.2859, interaction24 
set dash_color, br1, interaction24 
distance interaction25, resid 279 and name CA, resid 283 and name CA 
set dash_radius, 0.2859, interaction25 
set dash_color, br1, interaction25 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
