from kin.contacts.contact_analysis import multi_frame_contact_analysis
PARM_FILE = "Stripped.SYSTEM_apo.prmtop"
TRAJ_FILE = "SYSTEM_apo_all_runs.nc"

if __name__ == '__main__':
result_no_topo = multi_frame_contact_analysis(topology_file=PARM_FILE,
                                              trajectory_file=TRAJ_FILE,
                                              out_file="SYSTEM_all_contacts.csv",
                                              report_time_taken=True, 
                                             )
