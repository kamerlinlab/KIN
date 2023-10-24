# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 21 and name CA, resid 29 and name CA 
set dash_radius, 0.3, interaction1 
set dash_color, br9, interaction1 
distance interaction2, resid 22 and name CA, resid 44 and name CA 
set dash_radius, 0.2304, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 22 and name CA, resid 45 and name CA 
set dash_radius, 0.2839, interaction3 
set dash_color, dash, interaction3 
distance interaction4, resid 28 and name CA, resid 48 and name CA 
set dash_radius, 0.2839, interaction4 
set dash_color, dash, interaction4 
distance interaction5, resid 208 and name CA, resid 247 and name CA 
set dash_radius, 0.1929, interaction5 
set dash_color, brightorange, interaction5 
distance interaction6, resid 225 and name CA, resid 246 and name CA 
set dash_radius, 0.2946, interaction6 
set dash_color, br9, interaction6 
distance interaction7, resid 245 and name CA, resid 247 and name CA 
set dash_radius, 0.2571, interaction7 
set dash_color, br9, interaction7 
distance interaction8, resid 271 and name CA, resid 273 and name CA 
set dash_radius, 0.1929, interaction8 
set dash_color, dash, interaction8 
distance interaction9, resid 18 and name CA, resid 31 and name CA 
set dash_radius, 0.2946, interaction9 
set dash_color, br9, interaction9 
distance interaction10, resid 190 and name CA, resid 245 and name CA 
set dash_radius, 0.2679, interaction10 
set dash_color, br9, interaction10 
distance interaction11, resid 29 and name CA, resid 31 and name CA 
set dash_radius, 0.2893, interaction11 
set dash_color, br9, interaction11 
distance interaction12, resid 18 and name CA, resid 29 and name CA 
set dash_radius, 0.2143, interaction12 
set dash_color, br9, interaction12 
distance interaction13, resid 59 and name CA, resid 143 and name CA 
set dash_radius, 0.2304, interaction13 
set dash_color, br9, interaction13 
distance interaction14, resid 33 and name CA, resid 42 and name CA 
set dash_radius, 0.2089, interaction14 
set dash_color, br9, interaction14 
distance interaction15, resid 185 and name CA, resid 245 and name CA 
set dash_radius, 0.2089, interaction15 
set dash_color, br9, interaction15 
distance interaction16, resid 64 and name CA, resid 76 and name CA 
set dash_radius, 0.2304, interaction16 
set dash_color, br9, interaction16 
distance interaction17, resid 217 and name CA, resid 221 and name CA 
set dash_radius, 0.2464, interaction17 
set dash_color, br9, interaction17 
distance interaction18, resid 28 and name CA, resid 50 and name CA 
set dash_radius, 0.2304, interaction18 
set dash_color, brightorange, interaction18 
distance interaction19, resid 61 and name CA, resid 206 and name CA 
set dash_radius, 0.1982, interaction19 
set dash_color, br9, interaction19 
distance interaction20, resid 62 and name CA, resid 188 and name CA 
set dash_radius, 0.225, interaction20 
set dash_color, br9, interaction20 
distance interaction21, resid 62 and name CA, resid 203 and name CA 
set dash_radius, 0.2036, interaction21 
set dash_color, br9, interaction21 
distance interaction22, resid 56 and name CA, resid 130 and name CA 
set dash_radius, 0.2089, interaction22 
set dash_color, br9, interaction22 
distance interaction23, resid 252 and name CA, resid 253 and name CA 
set dash_radius, 0.2143, interaction23 
set dash_color, br9, interaction23 
distance interaction24, resid 21 and name CA, resid 274 and name CA 
set dash_radius, 0.1929, interaction24 
set dash_color, br9, interaction24 
distance interaction25, resid 33 and name CA, resid 286 and name CA 
set dash_radius, 0.1875, interaction25 
set dash_color, br9, interaction25 
distance interaction26, resid 33 and name CA, resid 282 and name CA 
set dash_radius, 0.1982, interaction26 
set dash_color, br9, interaction26 
distance interaction27, resid 32 and name CA, resid 178 and name CA 
set dash_radius, 0.1875, interaction27 
set dash_color, br9, interaction27 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
