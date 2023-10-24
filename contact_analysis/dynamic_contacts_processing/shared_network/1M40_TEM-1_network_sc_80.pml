# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 1 and name CA, resid 262 and name CA 
set dash_radius, 0.0148, interaction1 
set dash_color, br5, interaction1 
distance interaction2, resid 8 and name CA, resid 35 and name CA 
set dash_radius, 0.0148, interaction2 
set dash_color, br9, interaction2 
distance interaction3, resid 23 and name CA, resid 232 and name CA 
set dash_radius, 0.0246, interaction3 
set dash_color, dash, interaction3 
distance interaction4, resid 25 and name CA, resid 28 and name CA 
set dash_radius, 0.0246, interaction4 
set dash_color, br1, interaction4 
distance interaction5, resid 41 and name CA, resid 42 and name CA 
set dash_radius, 0.1672, interaction5 
set dash_color, br9, interaction5 
distance interaction6, resid 41 and name CA, resid 237 and name CA 
set dash_radius, 0.177, interaction6 
set dash_color, br5, interaction6 
distance interaction7, resid 48 and name CA, resid 141 and name CA 
set dash_radius, 0.2459, interaction7 
set dash_color, dash, interaction7 
distance interaction8, resid 54 and name CA, resid 126 and name CA 
set dash_radius, 0.2557, interaction8 
set dash_color, br9, interaction8 
distance interaction9, resid 55 and name CA, resid 94 and name CA 
set dash_radius, 0.0984, interaction9 
set dash_color, br9, interaction9 
distance interaction10, resid 64 and name CA, resid 68 and name CA 
set dash_radius, 0.0787, interaction10 
set dash_color, dash, interaction10 
distance interaction11, resid 81 and name CA, resid 108 and name CA 
set dash_radius, 0.1525, interaction11 
set dash_color, br1, interaction11 
distance interaction12, resid 83 and name CA, resid 100 and name CA 
set dash_radius, 0.0787, interaction12 
set dash_color, br9, interaction12 
distance interaction13, resid 83 and name CA, resid 104 and name CA 
set dash_radius, 0.2213, interaction13 
set dash_color, br9, interaction13 
distance interaction14, resid 84 and name CA, resid 106 and name CA 
set dash_radius, 0.3, interaction14 
set dash_color, br1, interaction14 
distance interaction15, resid 92 and name CA, resid 97 and name CA 
set dash_radius, 0.1918, interaction15 
set dash_color, br9, interaction15 
distance interaction16, resid 98 and name CA, resid 185 and name CA 
set dash_radius, 0.2311, interaction16 
set dash_color, br9, interaction16 
distance interaction17, resid 100 and name CA, resid 109 and name CA 
set dash_radius, 0.0148, interaction17 
set dash_color, br9, interaction17 
distance interaction18, resid 114 and name CA, resid 140 and name CA 
set dash_radius, 0.1131, interaction18 
set dash_color, br9, interaction18 
distance interaction19, resid 132 and name CA, resid 135 and name CA 
set dash_radius, 0.1623, interaction19 
set dash_color, br1, interaction19 
distance interaction20, resid 139 and name CA, resid 154 and name CA 
set dash_radius, 0.2852, interaction20 
set dash_color, dash, interaction20 
distance interaction21, resid 141 and name CA, resid 145 and name CA 
set dash_radius, 0.1574, interaction21 
set dash_color, br1, interaction21 
distance interaction22, resid 148 and name CA, resid 149 and name CA 
set dash_radius, 0.1967, interaction22 
set dash_color, br9, interaction22 
distance interaction23, resid 151 and name CA, resid 153 and name CA 
set dash_radius, 0.2164, interaction23 
set dash_color, dash, interaction23 
distance interaction24, resid 189 and name CA, resid 209 and name CA 
set dash_radius, 0.059, interaction24 
set dash_color, dash, interaction24 
distance interaction25, resid 197 and name CA, resid 208 and name CA 
set dash_radius, 0.1918, interaction25 
set dash_color, dash, interaction25 
distance interaction26, resid 200 and name CA, resid 206 and name CA 
set dash_radius, 0.0541, interaction26 
set dash_color, br9, interaction26 
distance interaction27, resid 204 and name CA, resid 226 and name CA 
set dash_radius, 0.1967, interaction27 
set dash_color, br9, interaction27 
distance interaction28, resid 204 and name CA, resid 260 and name CA 
set dash_radius, 0.0049, interaction28 
set dash_color, br9, interaction28 
distance interaction29, resid 205 and name CA, resid 230 and name CA 
set dash_radius, 0.0148, interaction29 
set dash_color, br9, interaction29 
distance interaction30, resid 226 and name CA, resid 263 and name CA 
set dash_radius, 0.0049, interaction30 
set dash_color, br9, interaction30 
distance interaction31, resid 232 and name CA, resid 263 and name CA 
set dash_radius, 0.0738, interaction31 
set dash_color, brightorange, interaction31 
distance interaction32, resid 247 and name CA, resid 250 and name CA 
set dash_radius, 0.0197, interaction32 
set dash_color, dash, interaction32 
distance interaction33, resid 12 and name CA, resid 36 and name CA 
set dash_radius, 0.0295, interaction33 
set dash_color, dash, interaction33 
distance interaction34, resid 157 and name CA, resid 158 and name CA 
set dash_radius, 0.0049, interaction34 
set dash_color, br9, interaction34 
distance interaction35, resid 120 and name CA, resid 140 and name CA 
set dash_radius, 0.0738, interaction35 
set dash_color, br9, interaction35 
distance interaction36, resid 201 and name CA, resid 204 and name CA 
set dash_radius, 0.2852, interaction36 
set dash_color, br9, interaction36 
distance interaction37, resid 4 and name CA, resid 258 and name CA 
set dash_radius, 0.0049, interaction37 
set dash_color, br1, interaction37 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
