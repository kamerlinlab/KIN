from modeller import *
from modeller.automodel import *    # Load the AutoModel class

log.verbose()
env = Environ()

# directories for input atom files
env.io.atom_files_directory = ['.', '../atom_files']

#class MyModel(AutoModel):
#    def select_atoms(self):
#        return Selection(self.residue_range('50:A', '300:A'))

a = LoopModel(env, alnfile = 'alignment_NAME.ali',
              knowns = 'known', sequence = 'fasta')

a.starting_model= 1
a.ending_model  = 1
a.loop.starting_model = 1
a.loop.ending_model   = 2
a.loop.md_level       = refine.fast

a.make()
