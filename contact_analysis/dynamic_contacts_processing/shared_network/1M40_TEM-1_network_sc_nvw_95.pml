# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 1 and name CA, resid 3 and name CA 
set dash_radius, 0.0098, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 1 and name CA, resid 262 and name CA 
set dash_radius, 0.0098, interaction2 
set dash_color, br5, interaction2 
distance interaction3, resid 25 and name CA, resid 28 and name CA 
set dash_radius, 0.0148, interaction3 
set dash_color, br1, interaction3 
distance interaction4, resid 41 and name CA, resid 42 and name CA 
set dash_radius, 0.1475, interaction4 
set dash_color, br9, interaction4 
distance interaction5, resid 41 and name CA, resid 237 and name CA 
set dash_radius, 0.1721, interaction5 
set dash_color, br5, interaction5 
distance interaction6, resid 48 and name CA, resid 141 and name CA 
set dash_radius, 0.2311, interaction6 
set dash_color, dash, interaction6 
distance interaction7, resid 64 and name CA, resid 68 and name CA 
set dash_radius, 0.0639, interaction7 
set dash_color, dash, interaction7 
distance interaction8, resid 81 and name CA, resid 108 and name CA 
set dash_radius, 0.0934, interaction8 
set dash_color, br1, interaction8 
distance interaction9, resid 84 and name CA, resid 106 and name CA 
set dash_radius, 0.2902, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 98 and name CA, resid 185 and name CA 
set dash_radius, 0.1082, interaction10 
set dash_color, br9, interaction10 
distance interaction11, resid 106 and name CA, resid 109 and name CA 
set dash_radius, 0.3, interaction11 
set dash_color, br1, interaction11 
distance interaction12, resid 111 and name CA, resid 141 and name CA 
set dash_radius, 0.1475, interaction12 
set dash_color, br1, interaction12 
distance interaction13, resid 114 and name CA, resid 140 and name CA 
set dash_radius, 0.0393, interaction13 
set dash_color, br9, interaction13 
distance interaction14, resid 132 and name CA, resid 135 and name CA 
set dash_radius, 0.123, interaction14 
set dash_color, br1, interaction14 
distance interaction15, resid 138 and name CA, resid 154 and name CA 
set dash_radius, 0.2656, interaction15 
set dash_color, br1, interaction15 
distance interaction16, resid 139 and name CA, resid 154 and name CA 
set dash_radius, 0.2754, interaction16 
set dash_color, dash, interaction16 
distance interaction17, resid 148 and name CA, resid 149 and name CA 
set dash_radius, 0.0295, interaction17 
set dash_color, br9, interaction17 
distance interaction18, resid 189 and name CA, resid 209 and name CA 
set dash_radius, 0.0049, interaction18 
set dash_color, dash, interaction18 
distance interaction19, resid 189 and name CA, resid 210 and name CA 
set dash_radius, 0.0, interaction19 
set dash_color, br1, interaction19 
distance interaction20, resid 197 and name CA, resid 208 and name CA 
set dash_radius, 0.1328, interaction20 
set dash_color, dash, interaction20 
distance interaction21, resid 205 and name CA, resid 230 and name CA 
set dash_radius, 0.0098, interaction21 
set dash_color, br9, interaction21 
distance interaction22, resid 232 and name CA, resid 263 and name CA 
set dash_radius, 0.0295, interaction22 
set dash_color, dash, interaction22 
distance interaction23, resid 247 and name CA, resid 250 and name CA 
set dash_radius, 0.0197, interaction23 
set dash_color, dash, interaction23 
distance interaction24, resid 157 and name CA, resid 158 and name CA 
set dash_radius, 0.0, interaction24 
set dash_color, br9, interaction24 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
