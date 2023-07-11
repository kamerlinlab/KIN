from modeller import *
log.level(1, 0, 1, 1, 1)
env = environ()
aln = alignment(env, file='all_sequences.seq', alignment_format='FASTA')


aln.salign(rr_file='${LIB}/blosum62.sim.mat',
		gap_penalties_1d=(-500, 0), output='',
		align_block=15,   # no. of seqs. in first MSA
		align_what='PROFILE',
		alignment_type='PAIRWISE',
		comparison_type='PSSM',  # or 'MAT' (Caution: Method NOT benchmarked
		                         # for 'MAT')
		similarity_flag=True,    # The score matrix is not rescaled
		substitution=True,       # The BLOSUM62 substitution values are
		                         # multiplied to the corr. coef.
		feature_weights=(1.0, 0.0, 0.0, 0.0, 0.0, 0.0),
		output_weights_file='test.mtx', # optional, to write weight matrix
		smooth_prof_weight=10.0) # For mixing data with priors
aln.write(file='salign.ali', alignment_format='PIR')
aln.write(file='align1d.pap', alignment_format='PAP')
