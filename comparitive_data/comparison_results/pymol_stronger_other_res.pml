# You can run me in several ways, perhaps the easiest way is to:
# 1. Load the PDB file of your system in PyMOL.
# 2. Type: @[FILE_NAME.py] in the command line.
# 3. Make sure the .py files are in the same directory as the pdb.
distance interaction1, resid 103 and name CA, resid 190 and name CA 
set dash_radius, 0.252, interaction1 
set dash_color, br1, interaction1 
distance interaction2, resid 74 and name CA, resid 77 and name CA 
set dash_radius, 0.252, interaction2 
set dash_color, br1, interaction2 
distance interaction3, resid 151 and name CA, resid 153 and name CA 
set dash_radius, 0.258, interaction3 
set dash_color, dash, interaction3 
distance interaction4, resid 205 and name CA, resid 225 and name CA 
set dash_radius, 0.264, interaction4 
set dash_color, br1, interaction4 
distance interaction5, resid 66 and name CA, resid 95 and name CA 
set dash_radius, 0.267, interaction5 
set dash_color, br1, interaction5 
distance interaction6, resid 186 and name CA, resid 208 and name CA 
set dash_radius, 0.273, interaction6 
set dash_color, br1, interaction6 
distance interaction7, resid 70 and name CA, resid 92 and name CA 
set dash_radius, 0.273, interaction7 
set dash_color, br1, interaction7 
distance interaction8, resid 48 and name CA, resid 141 and name CA 
set dash_radius, 0.282, interaction8 
set dash_color, dash, interaction8 
distance interaction9, resid 183 and name CA, resid 187 and name CA 
set dash_radius, 0.282, interaction9 
set dash_color, br1, interaction9 
distance interaction10, resid 184 and name CA, resid 188 and name CA 
set dash_radius, 0.282, interaction10 
set dash_color, br1, interaction10 
distance interaction11, resid 83 and name CA, resid 100 and name CA 
set dash_radius, 0.282, interaction11 
set dash_color, br9, interaction11 
distance interaction12, resid 140 and name CA, resid 144 and name CA 
set dash_radius, 0.285, interaction12 
set dash_color, br1, interaction12 
distance interaction13, resid 80 and name CA, resid 107 and name CA 
set dash_radius, 0.285, interaction13 
set dash_color, br1, interaction13 
distance interaction14, resid 142 and name CA, resid 145 and name CA 
set dash_radius, 0.291, interaction14 
set dash_color, br1, interaction14 
distance interaction15, resid 207 and name CA, resid 223 and name CA 
set dash_radius, 0.291, interaction15 
set dash_color, br1, interaction15 
distance interaction16, resid 209 and name CA, resid 221 and name CA 
set dash_radius, 0.291, interaction16 
set dash_color, br1, interaction16 
distance interaction17, resid 211 and name CA, resid 219 and name CA 
set dash_radius, 0.291, interaction17 
set dash_color, br1, interaction17 
distance interaction18, resid 111 and name CA, resid 141 and name CA 
set dash_radius, 0.294, interaction18 
set dash_color, br1, interaction18 
distance interaction19, resid 132 and name CA, resid 135 and name CA 
set dash_radius, 0.294, interaction19 
set dash_color, br1, interaction19 
distance interaction20, resid 201 and name CA, resid 204 and name CA 
set dash_radius, 0.294, interaction20 
set dash_color, br1, interaction20 
distance interaction21, resid 181 and name CA, resid 185 and name CA 
set dash_radius, 0.3, interaction21 
set dash_color, br1, interaction21 
distance interaction22, resid 182 and name CA, resid 186 and name CA 
set dash_radius, 0.3, interaction22 
set dash_color, br1, interaction22 
group All_Interactions, interaction* 
set dash_gap, 0.00, All_Interactions 
set dash_round_ends, on, All_Interactions 
hide labels 
