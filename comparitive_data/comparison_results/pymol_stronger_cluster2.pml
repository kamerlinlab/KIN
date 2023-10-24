# To use this script you can:
# 1. Load the PDB file of your system in PyMOL.
# 2. Run this file with:'@[FILE_NAME]' in the command line.
# 3. Make sure this file is in the same directory as the pdb.
distance interaction1, resid 37 and name CA, resid 159 and name CA 
set dash_radius, 0.3, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 41 and name CA, resid 156 and name CA 
set dash_radius, 0.3, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 56 and name CA, resid 185 and name CA 
set dash_radius, 0.3, interaction3 
set dash_color, br9, interaction3 
distance interaction4, resid 43 and name CA, resid 154 and name CA 
set dash_radius, 0.288, interaction4 
set dash_color, br1, interaction4 
distance interaction5, resid 19 and name CA, resid 240 and name CA 
set dash_radius, 0.264, interaction5 
set dash_color, br1, interaction5 
distance interaction6, resid 21 and name CA, resid 238 and name CA 
set dash_radius, 0.264, interaction6 
set dash_color, br1, interaction6 
distance interaction7, resid 23 and name CA, resid 236 and name CA 
set dash_radius, 0.264, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 41 and name CA, resid 238 and name CA 
set dash_radius, 0.264, interaction8 
set dash_color, br5, interaction8 
distance interaction9, resid 219 and name CA, resid 239 and name CA 
set dash_radius, 0.264, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 70 and name CA, resid 94 and name CA 
set dash_radius, 0.264, interaction10 
set dash_color, br9, interaction10 
distance interaction11, resid 25 and name CA, resid 234 and name CA 
set dash_radius, 0.258, interaction11 
set dash_color, br1, interaction11 
distance interaction12, resid 9 and name CA, resid 259 and name CA 
set dash_radius, 0.252, interaction12 
set dash_color, br9, interaction12 
distance interaction13, resid 157 and name CA, resid 160 and name CA 
set dash_radius, 0.246, interaction13 
set dash_color, br1, interaction13 
distance interaction14, resid 27 and name CA, resid 232 and name CA 
set dash_radius, 0.246, interaction14 
set dash_color, br1, interaction14 
distance interaction15, resid 139 and name CA, resid 154 and name CA 
set dash_radius, 0.24, interaction15 
set dash_color, dash, interaction15 
distance interaction16, resid 43 and name CA, resid 220 and name CA 
set dash_radius, 0.234, interaction16 
set dash_color, br1, interaction16 
distance interaction17, resid 139 and name CA, resid 146 and name CA 
set dash_radius, 0.234, interaction17 
set dash_color, br1, interaction17 
distance interaction18, resid 105 and name CA, resid 209 and name CA 
set dash_radius, 0.222, interaction18 
set dash_color, br1, interaction18 
distance interaction19, resid 139 and name CA, resid 151 and name CA 
set dash_radius, 0.222, interaction19 
set dash_color, dash, interaction19 
distance interaction20, resid 136 and name CA, resid 155 and name CA 
set dash_radius, 0.216, interaction20 
set dash_color, br1, interaction20 
distance interaction21, resid 12 and name CA, resid 252 and name CA 
set dash_radius, 0.216, interaction21 
set dash_color, br9, interaction21 
distance interaction22, resid 24 and name CA, resid 260 and name CA 
set dash_radius, 0.216, interaction22 
set dash_color, br9, interaction22 
distance interaction23, resid 70 and name CA, resid 92 and name CA 
set dash_radius, 0.216, interaction23 
set dash_color, br1, interaction23 
distance interaction24, resid 40 and name CA, resid 155 and name CA 
set dash_radius, 0.216, interaction24 
set dash_color, br1, interaction24 
distance interaction25, resid 56 and name CA, resid 182 and name CA 
set dash_radius, 0.216, interaction25 
set dash_color, br9, interaction25 
distance interaction26, resid 51 and name CA, resid 114 and name CA 
set dash_radius, 0.204, interaction26 
set dash_color, br9, interaction26 
distance interaction27, resid 66 and name CA, resid 95 and name CA 
set dash_radius, 0.204, interaction27 
set dash_color, br1, interaction27 
distance interaction28, resid 152 and name CA, resid 155 and name CA 
set dash_radius, 0.204, interaction28 
set dash_color, br1, interaction28 
distance interaction29, resid 221 and name CA, resid 237 and name CA 
set dash_radius, 0.204, interaction29 
set dash_color, br1, interaction29 
distance interaction30, resid 223 and name CA, resid 235 and name CA 
set dash_radius, 0.204, interaction30 
set dash_color, br1, interaction30 
distance interaction31, resid 225 and name CA, resid 233 and name CA 
set dash_radius, 0.204, interaction31 
set dash_color, br1, interaction31 
distance interaction32, resid 24 and name CA, resid 235 and name CA 
set dash_radius, 0.198, interaction32 
set dash_color, br9, interaction32 
distance interaction33, resid 41 and name CA, resid 158 and name CA 
set dash_radius, 0.192, interaction33 
set dash_color, br9, interaction33 
distance interaction34, resid 200 and name CA, resid 206 and name CA 
set dash_radius, 0.192, interaction34 
set dash_color, br9, interaction34 
distance interaction35, resid 26 and name CA, resid 30 and name CA 
set dash_radius, 0.186, interaction35 
set dash_color, br1, interaction35 
distance interaction36, resid 52 and name CA, resid 185 and name CA 
set dash_radius, 0.186, interaction36 
set dash_color, br9, interaction36 
distance interaction37, resid 226 and name CA, resid 232 and name CA 
set dash_radius, 0.186, interaction37 
set dash_color, br9, interaction37 
distance interaction38, resid 54 and name CA, resid 123 and name CA 
set dash_radius, 0.186, interaction38 
set dash_color, br9, interaction38 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
