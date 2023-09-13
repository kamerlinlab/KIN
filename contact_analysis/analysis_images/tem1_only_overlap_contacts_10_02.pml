# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 8 and name CA, resid 12 and name CA 
set dash_radius, 0.1139, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 20 and name CA, resid 237 and name CA 
set dash_radius, 0.1126, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 25 and name CA, resid 30 and name CA 
set dash_radius, 0.1333, interaction3 
set dash_color, br1, interaction3 
distance interaction4, resid 41 and name CA, resid 158 and name CA 
set dash_radius, 0.1211, interaction4 
set dash_color, br9, interaction4 
distance interaction5, resid 50 and name CA, resid 161 and name CA 
set dash_radius, 0.1647, interaction5 
set dash_color, br9, interaction5 
distance interaction6, resid 83 and name CA, resid 86 and name CA 
set dash_radius, 0.1271, interaction6 
set dash_color, br1, interaction6 
distance interaction7, resid 84 and name CA, resid 87 and name CA 
set dash_radius, 0.2781, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 113 and name CA, resid 116 and name CA 
set dash_radius, 0.1748, interaction8 
set dash_color, br1, interaction8 
distance interaction9, resid 114 and name CA, resid 117 and name CA 
set dash_radius, 0.1669, interaction9 
set dash_color, br9, interaction9 
distance interaction10, resid 115 and name CA, resid 118 and name CA 
set dash_radius, 0.3, interaction10 
set dash_color, br1, interaction10 
distance interaction11, resid 122 and name CA, resid 126 and name CA 
set dash_radius, 0.178, interaction11 
set dash_color, br1, interaction11 
distance interaction12, resid 134 and name CA, resid 160 and name CA 
set dash_radius, 0.1323, interaction12 
set dash_color, br9, interaction12 
distance interaction13, resid 139 and name CA, resid 151 and name CA 
set dash_radius, 0.1578, interaction13 
set dash_color, dash, interaction13 
distance interaction14, resid 168 and name CA, resid 173 and name CA 
set dash_radius, 0.2404, interaction14 
set dash_color, br9, interaction14 
distance interaction15, resid 186 and name CA, resid 207 and name CA 
set dash_radius, 0.1493, interaction15 
set dash_color, br9, interaction15 
distance interaction16, resid 187 and name CA, resid 197 and name CA 
set dash_radius, 0.1752, interaction16 
set dash_color, br1, interaction16 
distance interaction17, resid 196 and name CA, resid 220 and name CA 
set dash_radius, 0.1236, interaction17 
set dash_color, br9, interaction17 
distance interaction18, resid 223 and name CA, resid 233 and name CA 
set dash_radius, 0.1329, interaction18 
set dash_color, br9, interaction18 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
