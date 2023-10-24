from tools_proj.contacts.contact_analysis import multi_frame_contact_analysis

PARM_FILE = "Stripped.1M40_TEM-1_apo.prmtop"
TRAJ_FILE = "1M40_TEM-1_apo_all_runs.nc" 

if __name__ == '__main__':
	result_no_topo = multi_frame_contact_analysis(topology_file=PARM_FILE,
		        trajectory_file=TRAJ_FILE,
			    out_file="1M40_TEM-1_test.txt",
				        report_time_taken=True,
					)
