# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 18 and name CA, resid 22 and name CA 
set dash_radius, 0.3, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 21 and name CA, resid 25 and name CA 
set dash_radius, 0.2727, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 21 and name CA, resid 29 and name CA 
set dash_radius, 0.2273, interaction3 
set dash_color, br9, interaction3 
distance interaction4, resid 22 and name CA, resid 29 and name CA 
set dash_radius, 0.2591, interaction4 
set dash_color, br1, interaction4 
distance interaction5, resid 22 and name CA, resid 44 and name CA 
set dash_radius, 0.1909, interaction5 
set dash_color, br1, interaction5 
distance interaction6, resid 22 and name CA, resid 45 and name CA 
set dash_radius, 0.2364, interaction6 
set dash_color, dash, interaction6 
distance interaction7, resid 28 and name CA, resid 48 and name CA 
set dash_radius, 0.2045, interaction7 
set dash_color, dash, interaction7 
distance interaction8, resid 31 and name CA, resid 44 and name CA 
set dash_radius, 0.2682, interaction8 
set dash_color, br1, interaction8 
distance interaction9, resid 33 and name CA, resid 42 and name CA 
set dash_radius, 0.2636, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 35 and name CA, resid 37 and name CA 
set dash_radius, 0.2273, interaction10 
set dash_color, br1, interaction10 
distance interaction11, resid 35 and name CA, resid 40 and name CA 
set dash_radius, 0.2182, interaction11 
set dash_color, br1, interaction11 
distance interaction12, resid 38 and name CA, resid 40 and name CA 
set dash_radius, 0.1864, interaction12 
set dash_color, br1, interaction12 
distance interaction13, resid 52 and name CA, resid 241 and name CA 
set dash_radius, 0.2091, interaction13 
set dash_color, br1, interaction13 
distance interaction14, resid 62 and name CA, resid 188 and name CA 
set dash_radius, 0.1864, interaction14 
set dash_color, br9, interaction14 
distance interaction15, resid 65 and name CA, resid 206 and name CA 
set dash_radius, 0.2045, interaction15 
set dash_color, br9, interaction15 
distance interaction16, resid 116 and name CA, resid 120 and name CA 
set dash_radius, 0.2636, interaction16 
set dash_color, br1, interaction16 
distance interaction17, resid 148 and name CA, resid 152 and name CA 
set dash_radius, 0.1864, interaction17 
set dash_color, br1, interaction17 
distance interaction18, resid 150 and name CA, resid 188 and name CA 
set dash_radius, 0.1727, interaction18 
set dash_color, br9, interaction18 
distance interaction19, resid 186 and name CA, resid 191 and name CA 
set dash_radius, 0.25, interaction19 
set dash_color, br1, interaction19 
distance interaction20, resid 187 and name CA, resid 194 and name CA 
set dash_radius, 0.1864, interaction20 
set dash_color, br1, interaction20 
distance interaction21, resid 195 and name CA, resid 203 and name CA 
set dash_radius, 0.1955, interaction21 
set dash_color, br9, interaction21 
distance interaction22, resid 204 and name CA, resid 208 and name CA 
set dash_radius, 0.2864, interaction22 
set dash_color, br1, interaction22 
distance interaction23, resid 210 and name CA, resid 229 and name CA 
set dash_radius, 0.2273, interaction23 
set dash_color, br1, interaction23 
distance interaction24, resid 217 and name CA, resid 221 and name CA 
set dash_radius, 0.2227, interaction24 
set dash_color, br1, interaction24 
distance interaction25, resid 221 and name CA, resid 246 and name CA 
set dash_radius, 0.2227, interaction25 
set dash_color, br9, interaction25 
distance interaction26, resid 225 and name CA, resid 246 and name CA 
set dash_radius, 0.2318, interaction26 
set dash_color, br9, interaction26 
distance interaction27, resid 245 and name CA, resid 247 and name CA 
set dash_radius, 0.1955, interaction27 
set dash_color, br9, interaction27 
distance interaction28, resid 265 and name CA, resid 268 and name CA 
set dash_radius, 0.1682, interaction28 
set dash_color, br1, interaction28 
distance interaction29, resid 29 and name CA, resid 31 and name CA 
set dash_radius, 0.1591, interaction29 
set dash_color, br9, interaction29 
distance interaction30, resid 51 and name CA, resid 241 and name CA 
set dash_radius, 0.1864, interaction30 
set dash_color, br1, interaction30 
distance interaction31, resid 207 and name CA, resid 210 and name CA 
set dash_radius, 0.2136, interaction31 
set dash_color, br1, interaction31 
distance interaction32, resid 205 and name CA, resid 209 and name CA 
set dash_radius, 0.25, interaction32 
set dash_color, br1, interaction32 
distance interaction33, resid 18 and name CA, resid 31 and name CA 
set dash_radius, 0.2227, interaction33 
set dash_color, br9, interaction33 
distance interaction34, resid 189 and name CA, resid 245 and name CA 
set dash_radius, 0.1636, interaction34 
set dash_color, br9, interaction34 
distance interaction35, resid 35 and name CA, resid 38 and name CA 
set dash_radius, 0.2318, interaction35 
set dash_color, br1, interaction35 
distance interaction36, resid 282 and name CA, resid 286 and name CA 
set dash_radius, 0.1591, interaction36 
set dash_color, br1, interaction36 
distance interaction37, resid 35 and name CA, resid 39 and name CA 
set dash_radius, 0.1818, interaction37 
set dash_color, br1, interaction37 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
