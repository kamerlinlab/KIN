# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 22 and name CA, resid 45 and name CA 
set dash_radius, 0.2421, interaction1 
set dash_color, dash, interaction1 
distance interaction2, resid 31 and name CA, resid 44 and name CA 
set dash_radius, 0.2895, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 33 and name CA, resid 42 and name CA 
set dash_radius, 0.3, interaction3 
set dash_color, br1, interaction3 
distance interaction4, resid 35 and name CA, resid 40 and name CA 
set dash_radius, 0.2263, interaction4 
set dash_color, br1, interaction4 
distance interaction5, resid 115 and name CA, resid 119 and name CA 
set dash_radius, 0.1895, interaction5 
set dash_color, br1, interaction5 
distance interaction6, resid 156 and name CA, resid 158 and name CA 
set dash_radius, 0.1947, interaction6 
set dash_color, dash, interaction6 
distance interaction7, resid 185 and name CA, resid 189 and name CA 
set dash_radius, 0.2316, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 199 and name CA, resid 203 and name CA 
set dash_radius, 0.2737, interaction8 
set dash_color, br1, interaction8 
distance interaction9, resid 200 and name CA, resid 204 and name CA 
set dash_radius, 0.2789, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 221 and name CA, resid 222 and name CA 
set dash_radius, 0.2579, interaction10 
set dash_color, br9, interaction10 
distance interaction11, resid 245 and name CA, resid 247 and name CA 
set dash_radius, 0.1842, interaction11 
set dash_color, br9, interaction11 
distance interaction12, resid 273 and name CA, resid 277 and name CA 
set dash_radius, 0.2105, interaction12 
set dash_color, br1, interaction12 
distance interaction13, resid 275 and name CA, resid 279 and name CA 
set dash_radius, 0.2737, interaction13 
set dash_color, br1, interaction13 
distance interaction14, resid 276 and name CA, resid 280 and name CA 
set dash_radius, 0.2105, interaction14 
set dash_color, br1, interaction14 
distance interaction15, resid 279 and name CA, resid 283 and name CA 
set dash_radius, 0.2316, interaction15 
set dash_color, br1, interaction15 
distance interaction16, resid 59 and name CA, resid 63 and name CA 
set dash_radius, 0.2, interaction16 
set dash_color, br1, interaction16 
distance interaction17, resid 22 and name CA, resid 44 and name CA 
set dash_radius, 0.1947, interaction17 
set dash_color, br1, interaction17 
distance interaction18, resid 111 and name CA, resid 115 and name CA 
set dash_radius, 0.1895, interaction18 
set dash_color, br1, interaction18 
distance interaction19, resid 186 and name CA, resid 190 and name CA 
set dash_radius, 0.2053, interaction19 
set dash_color, br1, interaction19 
distance interaction20, resid 204 and name CA, resid 208 and name CA 
set dash_radius, 0.2105, interaction20 
set dash_color, br1, interaction20 
distance interaction21, resid 236 and name CA, resid 239 and name CA 
set dash_radius, 0.1895, interaction21 
set dash_color, br1, interaction21 
distance interaction22, resid 222 and name CA, resid 225 and name CA 
set dash_radius, 0.2211, interaction22 
set dash_color, br9, interaction22 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
