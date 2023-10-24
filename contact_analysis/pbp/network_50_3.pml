# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 14 and name CA, resid 15 and name CA 
set dash_radius, 0.15, interaction1 
set dash_color, br9, interaction1 
distance interaction2, resid 25 and name CA, resid 29 and name CA 
set dash_radius, 0.15, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 66 and name CA, resid 70 and name CA 
set dash_radius, 0.15, interaction3 
set dash_color, br1, interaction3 
distance interaction4, resid 69 and name CA, resid 73 and name CA 
set dash_radius, 0.15, interaction4 
set dash_color, br1, interaction4 
distance interaction5, resid 71 and name CA, resid 175 and name CA 
set dash_radius, 0.15, interaction5 
set dash_color, br9, interaction5 
distance interaction6, resid 80 and name CA, resid 83 and name CA 
set dash_radius, 0.15, interaction6 
set dash_color, br1, interaction6 
distance interaction7, resid 95 and name CA, resid 98 and name CA 
set dash_radius, 0.3, interaction7 
set dash_color, br5, interaction7 
distance interaction8, resid 95 and name CA, resid 99 and name CA 
set dash_radius, 0.15, interaction8 
set dash_color, br1, interaction8 
distance interaction9, resid 96 and name CA, resid 100 and name CA 
set dash_radius, 0.15, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 102 and name CA, resid 106 and name CA 
set dash_radius, 0.15, interaction10 
set dash_color, br1, interaction10 
distance interaction11, resid 103 and name CA, resid 107 and name CA 
set dash_radius, 0.15, interaction11 
set dash_color, br1, interaction11 
distance interaction12, resid 106 and name CA, resid 110 and name CA 
set dash_radius, 0.3, interaction12 
set dash_color, br1, interaction12 
distance interaction13, resid 108 and name CA, resid 111 and name CA 
set dash_radius, 0.3, interaction13 
set dash_color, br1, interaction13 
distance interaction14, resid 126 and name CA, resid 130 and name CA 
set dash_radius, 0.3, interaction14 
set dash_color, br1, interaction14 
distance interaction15, resid 127 and name CA, resid 131 and name CA 
set dash_radius, 0.15, interaction15 
set dash_color, br1, interaction15 
distance interaction16, resid 130 and name CA, resid 134 and name CA 
set dash_radius, 0.15, interaction16 
set dash_color, br1, interaction16 
distance interaction17, resid 142 and name CA, resid 145 and name CA 
set dash_radius, 0.15, interaction17 
set dash_color, br9, interaction17 
distance interaction18, resid 142 and name CA, resid 148 and name CA 
set dash_radius, 0.15, interaction18 
set dash_color, br5, interaction18 
distance interaction19, resid 144 and name CA, resid 147 and name CA 
set dash_radius, 0.15, interaction19 
set dash_color, br1, interaction19 
distance interaction20, resid 148 and name CA, resid 149 and name CA 
set dash_radius, 0.15, interaction20 
set dash_color, br5, interaction20 
distance interaction21, resid 162 and name CA, resid 166 and name CA 
set dash_radius, 0.15, interaction21 
set dash_color, br1, interaction21 
distance interaction22, resid 163 and name CA, resid 167 and name CA 
set dash_radius, 0.15, interaction22 
set dash_color, br1, interaction22 
distance interaction23, resid 165 and name CA, resid 169 and name CA 
set dash_radius, 0.15, interaction23 
set dash_color, br1, interaction23 
distance interaction24, resid 166 and name CA, resid 170 and name CA 
set dash_radius, 0.15, interaction24 
set dash_color, br1, interaction24 
distance interaction25, resid 168 and name CA, resid 183 and name CA 
set dash_radius, 0.15, interaction25 
set dash_color, br9, interaction25 
distance interaction26, resid 171 and name CA, resid 174 and name CA 
set dash_radius, 0.15, interaction26 
set dash_color, br1, interaction26 
distance interaction27, resid 176 and name CA, resid 180 and name CA 
set dash_radius, 0.15, interaction27 
set dash_color, br1, interaction27 
distance interaction28, resid 179 and name CA, resid 183 and name CA 
set dash_radius, 0.15, interaction28 
set dash_color, br1, interaction28 
distance interaction29, resid 182 and name CA, resid 186 and name CA 
set dash_radius, 0.15, interaction29 
set dash_color, br1, interaction29 
distance interaction30, resid 183 and name CA, resid 186 and name CA 
set dash_radius, 0.15, interaction30 
set dash_color, br1, interaction30 
distance interaction31, resid 183 and name CA, resid 187 and name CA 
set dash_radius, 0.15, interaction31 
set dash_color, br1, interaction31 
distance interaction32, resid 184 and name CA, resid 188 and name CA 
set dash_radius, 0.3, interaction32 
set dash_color, br1, interaction32 
distance interaction33, resid 185 and name CA, resid 188 and name CA 
set dash_radius, 0.15, interaction33 
set dash_color, dash, interaction33 
distance interaction34, resid 204 and name CA, resid 212 and name CA 
set dash_radius, 0.15, interaction34 
set dash_color, br1, interaction34 
distance interaction35, resid 215 and name CA, resid 244 and name CA 
set dash_radius, 0.15, interaction35 
set dash_color, br9, interaction35 
distance interaction36, resid 221 and name CA, resid 224 and name CA 
set dash_radius, 0.15, interaction36 
set dash_color, br1, interaction36 
distance interaction37, resid 224 and name CA, resid 225 and name CA 
set dash_radius, 0.15, interaction37 
set dash_color, br1, interaction37 
distance interaction38, resid 230 and name CA, resid 232 and name CA 
set dash_radius, 0.15, interaction38 
set dash_color, br9, interaction38 
distance interaction39, resid 250 and name CA, resid 254 and name CA 
set dash_radius, 0.15, interaction39 
set dash_color, br1, interaction39 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
