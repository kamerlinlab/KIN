# Dariia's Paths
export BASE_PREP=/storage/home/hhive1/dyehorova3/data/tools/Protein_Prep_V2
export BASE_RUN=/storage/home/hhive1/dyehorova3/data/tools/Simulation_runs
export BASE_PROC=/storage/home/hhive1/dyehorova3/data/tools/Md_processing

CONTACTS_FILE=MOD_contact_analyser_template.py
RUN_FILE=run_contacts.sh

cd Trajectories
for i in sys_*
do
	cd $i
	mkdir no_int_type
	cd no_int_type
	pdb_name=`echo $i| awk -Fs_ '{print $2}'`
	cp  ../../Stripped.${pdb_name}_apo.prmtop ${pdb_name}_apo.prmtop
	cp  ../../${pdb_name}_apo_all_runs.nc .
	echo $pdb_name
	cp $BASE_PROC/$CONTACTS_FILE .
	sed -i "s,PROC_PATH,$BASE_PROC,g" $CONTACTS_FILE
	sed -i "s/SYSTEM/${pdb_name}/g" $CONTACTS_FILE
	
	cp $BASE_PROC/$RUN_FILE .
	sed -i "s/SYSTEM/${pdb_name}/g" $RUN_FILE
	
	sbatch $RUN_FILE
	cd ../../
done
cd ..		

