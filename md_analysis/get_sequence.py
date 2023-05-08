from modeller import *
code = '3BLM_blaZ_apo_postleap'

e = Environ()
m = Model(e, file=code)
aln = Alignment(e)
aln.append_model(m, align_codes=code)
aln.write(file=code+'.seq')
