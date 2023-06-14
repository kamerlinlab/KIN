from modeller import *

log.verbose()
env = environ()
env.io.atom_files_directory = "./"

aln = alignment(env, file="fasta_align.seq", alignment_format="FASTA")
aln.salign(
    rr_file="$(LIB)/as1.sim.mat",  # Substitution matrix used
    output="",
    max_gap_length=20,
    gap_function=False,  # If False then align2d not done
    feature_weights=(1.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    gap_penalties_1d=(-100, 0),
    output_weights_file="saligni1d.mtx",
    similarity_flag=True,
)  # Ensuring that the dynamic programming
# matrix is not scaled to a
# difference matrix
aln.write(file="align1d.ali", alignment_format="PIR")
aln.write(file="align1d.pap", alignment_format="PAP")
