from modeller import *
log.verbose()
env = environ()
env.io.atom_files_directory = './:../atom_files/'
aln = alignment(env, file='all_sequences.seq', alignment_format='FASTA')

for (weights, write_fit, whole) in (((1., 0., 0., 0., 0., 0.), False, True),
				((1., 0., 0., 0., 0., 0.), False, True),	
				((1., 0., 0., 0., 0., 0.), False, True)):	
	aln.salign(rms_cutoff=3.5, normalize_pp_scores=False,
			rr_file='$(LIB)/as1.sim.mat', overhang=30,
			gap_penalties_1d=(-450, -50),
			dendrogram_file='1is3A.tree',
			alignment_type='tree', # If 'progresive', the tree is not
						# computed and all
						# structues will be
						# aligned sequentially
						# to the first
			feature_weights=weights, # For a multiple sequence alignment only
						# the first feature
						# needs to be non-zero
			improve_alignment=True, fit=True, write_fit=write_fit,
			write_whole_pdb=whole) 
	aln.write(file='bettaLac.pap', alignment_format='PAP')
	aln.write(file='bettaLac.ali', alignment_format='PIR')
	

