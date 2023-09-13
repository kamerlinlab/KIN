# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 21 and name CA, resid 35 and name CA 
set dash_radius, 0.097, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 23 and name CA, resid 33 and name CA 
set dash_radius, 0.1479, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 40 and name CA, resid 155 and name CA 
set dash_radius, 0.1358, interaction3 
set dash_color, br1, interaction3 
distance interaction4, resid 51 and name CA, resid 113 and name CA 
set dash_radius, 0.2499, interaction4 
set dash_color, br9, interaction4 
distance interaction5, resid 51 and name CA, resid 114 and name CA 
set dash_radius, 0.1332, interaction5 
set dash_color, br9, interaction5 
distance interaction6, resid 56 and name CA, resid 174 and name CA 
set dash_radius, 0.1744, interaction6 
set dash_color, br9, interaction6 
distance interaction7, resid 57 and name CA, resid 61 and name CA 
set dash_radius, 0.1077, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 83 and name CA, resid 104 and name CA 
set dash_radius, 0.0988, interaction8 
set dash_color, br9, interaction8 
distance interaction9, resid 93 and name CA, resid 96 and name CA 
set dash_radius, 0.2581, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 97 and name CA, resid 112 and name CA 
set dash_radius, 0.1147, interaction10 
set dash_color, br9, interaction10 
distance interaction11, resid 97 and name CA, resid 113 and name CA 
set dash_radius, 0.2093, interaction11 
set dash_color, br9, interaction11 
distance interaction12, resid 100 and name CA, resid 109 and name CA 
set dash_radius, 0.1896, interaction12 
set dash_color, br9, interaction12 
distance interaction13, resid 114 and name CA, resid 140 and name CA 
set dash_radius, 0.1389, interaction13 
set dash_color, br9, interaction13 
distance interaction14, resid 123 and name CA, resid 137 and name CA 
set dash_radius, 0.1861, interaction14 
set dash_color, br9, interaction14 
distance interaction15, resid 128 and name CA, resid 131 and name CA 
set dash_radius, 0.2651, interaction15 
set dash_color, br1, interaction15 
distance interaction16, resid 157 and name CA, resid 160 and name CA 
set dash_radius, 0.1186, interaction16 
set dash_color, br9, interaction16 
distance interaction17, resid 165 and name CA, resid 221 and name CA 
set dash_radius, 0.1945, interaction17 
set dash_color, br9, interaction17 
distance interaction18, resid 167 and name CA, resid 171 and name CA 
set dash_radius, 0.244, interaction18 
set dash_color, br1, interaction18 
distance interaction19, resid 195 and name CA, resid 220 and name CA 
set dash_radius, 0.2334, interaction19 
set dash_color, br9, interaction19 
distance interaction20, resid 196 and name CA, resid 220 and name CA 
set dash_radius, 0.2584, interaction20 
set dash_color, br9, interaction20 
distance interaction21, resid 197 and name CA, resid 200 and name CA 
set dash_radius, 0.3, interaction21 
set dash_color, br1, interaction21 
distance interaction22, resid 206 and name CA, resid 224 and name CA 
set dash_radius, 0.2654, interaction22 
set dash_color, br9, interaction22 
distance interaction23, resid 224 and name CA, resid 234 and name CA 
set dash_radius, 0.1212, interaction23 
set dash_color, br9, interaction23 
distance interaction24, resid 249 and name CA, resid 253 and name CA 
set dash_radius, 0.1676, interaction24 
set dash_color, br1, interaction24 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
