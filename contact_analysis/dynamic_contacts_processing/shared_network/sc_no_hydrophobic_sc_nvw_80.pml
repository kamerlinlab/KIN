# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 1 and name CA, resid 3 and name CA 
set dash_radius, 0.0094, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 1 and name CA, resid 262 and name CA 
set dash_radius, 0.0141, interaction2 
set dash_color, br5, interaction2 
distance interaction3, resid 23 and name CA, resid 232 and name CA 
set dash_radius, 0.0234, interaction3 
set dash_color, dash, interaction3 
distance interaction4, resid 25 and name CA, resid 28 and name CA 
set dash_radius, 0.0234, interaction4 
set dash_color, br1, interaction4 
distance interaction5, resid 41 and name CA, resid 237 and name CA 
set dash_radius, 0.1688, interaction5 
set dash_color, br5, interaction5 
distance interaction6, resid 48 and name CA, resid 141 and name CA 
set dash_radius, 0.2297, interaction6 
set dash_color, dash, interaction6 
distance interaction7, resid 60 and name CA, resid 175 and name CA 
set dash_radius, 0.0656, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 64 and name CA, resid 68 and name CA 
set dash_radius, 0.0656, interaction8 
set dash_color, dash, interaction8 
distance interaction9, resid 73 and name CA, resid 76 and name CA 
set dash_radius, 0.1594, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 78 and name CA, resid 108 and name CA 
set dash_radius, 0.1359, interaction10 
set dash_color, br1, interaction10 
distance interaction11, resid 79 and name CA, resid 107 and name CA 
set dash_radius, 0.1219, interaction11 
set dash_color, br1, interaction11 
distance interaction12, resid 81 and name CA, resid 108 and name CA 
set dash_radius, 0.1313, interaction12 
set dash_color, br1, interaction12 
distance interaction13, resid 84 and name CA, resid 106 and name CA 
set dash_radius, 0.2859, interaction13 
set dash_color, br1, interaction13 
distance interaction14, resid 106 and name CA, resid 109 and name CA 
set dash_radius, 0.3, interaction14 
set dash_color, br1, interaction14 
distance interaction15, resid 111 and name CA, resid 115 and name CA 
set dash_radius, 0.0328, interaction15 
set dash_color, br1, interaction15 
distance interaction16, resid 111 and name CA, resid 141 and name CA 
set dash_radius, 0.1969, interaction16 
set dash_color, br1, interaction16 
distance interaction17, resid 112 and name CA, resid 116 and name CA 
set dash_radius, 0.0094, interaction17 
set dash_color, br1, interaction17 
distance interaction18, resid 132 and name CA, resid 134 and name CA 
set dash_radius, 0.1734, interaction18 
set dash_color, br1, interaction18 
distance interaction19, resid 132 and name CA, resid 135 and name CA 
set dash_radius, 0.1547, interaction19 
set dash_color, br1, interaction19 
distance interaction20, resid 138 and name CA, resid 154 and name CA 
set dash_radius, 0.2812, interaction20 
set dash_color, br1, interaction20 
distance interaction21, resid 139 and name CA, resid 154 and name CA 
set dash_radius, 0.2719, interaction21 
set dash_color, dash, interaction21 
distance interaction22, resid 141 and name CA, resid 145 and name CA 
set dash_radius, 0.15, interaction22 
set dash_color, br1, interaction22 
distance interaction23, resid 142 and name CA, resid 145 and name CA 
set dash_radius, 0.1172, interaction23 
set dash_color, br1, interaction23 
distance interaction24, resid 151 and name CA, resid 153 and name CA 
set dash_radius, 0.2063, interaction24 
set dash_color, dash, interaction24 
distance interaction25, resid 159 and name CA, resid 163 and name CA 
set dash_radius, 0.0563, interaction25 
set dash_color, br1, interaction25 
distance interaction26, resid 189 and name CA, resid 209 and name CA 
set dash_radius, 0.0094, interaction26 
set dash_color, dash, interaction26 
distance interaction27, resid 189 and name CA, resid 210 and name CA 
set dash_radius, 0.0, interaction27 
set dash_color, br1, interaction27 
distance interaction28, resid 197 and name CA, resid 208 and name CA 
set dash_radius, 0.1781, interaction28 
set dash_color, dash, interaction28 
distance interaction29, resid 214 and name CA, resid 217 and name CA 
set dash_radius, 0.1453, interaction29 
set dash_color, br1, interaction29 
distance interaction30, resid 232 and name CA, resid 263 and name CA 
set dash_radius, 0.0328, interaction30 
set dash_color, brightorange, interaction30 
distance interaction31, resid 243 and name CA, resid 248 and name CA 
set dash_radius, 0.0234, interaction31 
set dash_color, br1, interaction31 
distance interaction32, resid 247 and name CA, resid 250 and name CA 
set dash_radius, 0.0187, interaction32 
set dash_color, dash, interaction32 
distance interaction33, resid 12 and name CA, resid 36 and name CA 
set dash_radius, 0.0281, interaction33 
set dash_color, dash, interaction33 
distance interaction34, resid 72 and name CA, resid 84 and name CA 
set dash_radius, 0.1641, interaction34 
set dash_color, br1, interaction34 
distance interaction35, resid 12 and name CA, resid 19 and name CA 
set dash_radius, 0.0187, interaction35 
set dash_color, br1, interaction35 
distance interaction36, resid 120 and name CA, resid 124 and name CA 
set dash_radius, 0.1078, interaction36 
set dash_color, br1, interaction36 
distance interaction37, resid 4 and name CA, resid 258 and name CA 
set dash_radius, 0.0, interaction37 
set dash_color, br1, interaction37 
distance interaction38, resid 124 and name CA, resid 137 and name CA 
set dash_radius, 0.1734, interaction38 
set dash_color, br1, interaction38 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
