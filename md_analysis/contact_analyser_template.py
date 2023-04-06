"""
These would be better submitted as jobs, for the first one give maybe 24 hours
and access to a single node, just to see how long it takes and the others can be adjusted from there.

"""
from key_interactions_finder import contact_identification


# Version 1. We could try this first Dariia, may run out of memory though.
contact_identification.calculate_contacts(
    parm_file=TOPOLOGY_FILE,
    traj_file=TRAJECTORY_FILE,
    out_file=OUT_FILE, # .csv
    report_timings=True  # optional
)


# Version 2. - Determine the interaction network for a subset of residues.
# This can be useful if you have a large system/large number of frames to analyse
# The results generated here can be very easily merged later on.
# E.g. run this for residues 1-50, 51-100, etc... and then combine them later.

# If this is required we could break it up into 4 blocks for example
# For the last block, you don't need to specify "last_res",
# So if most systems have ~400 ish residues could break it up as follows:
# Block1 = last_res=100
# Block2 = first_res=101, last_res=200
# Block3 = first_res=201, last_res=300
# Block4 = first_res=301 # auto calculated to be last residue in system.

contact_identification.calculate_contacts(
    parm_file=TOPOLOGY_FILE,
    traj_file=TRAJECTORY_FILE,
    out_file=OUT_FILE, # .csv
    first_res=1,  # optional parameter
    last_res=50,  # optional
    report_timings=True  # optional
)


