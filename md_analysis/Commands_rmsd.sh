#!/bin/bash


# Dariia's Paths
export BASE_PREP=/storage/home/hhive1/dyehorova3/data/tools/Protein_Prep_V2
export BASE_RUN=/storage/home/hhive1/dyehorova3/data/tools/Simulation_runs
export BASE_PROC=/storage/home/hhive1/dyehorova3/data/tools/Md_processing

CLEANUP_FILE=trajectory_clean_template.in
RMSD_FILE=protein_rmsd_template.in

# set up all requiered files for the run
cd $BASE_PROC

cp ../protein_prep/5_tleap/*_apo_postleap.pdb .

cd $BASE_RUN
for i in sys_* 
do 
	cd $i
	pdb_name=`echo $i| awk -Fs_ '{print $2}'`
	rm $BASE_PROC/Trajectories/$i/*nc
	rm $BASE_PROC/Trajectories/$i/*prmtop

	echo $pdb_name
	cp $BASE_PROC/$CLEANUP_FILE .
	sed -i "s,RUN_PATH,$BASE_RUN,g" $CLEANUP_FILE
	sed -i "s,OUT_PATH,$BASE_PROC,g" $CLEANUP_FILE
	sed -i "s/SYSTEM/${pdb_name}/g" $CLEANUP_FILE
	echo "Making a joint clean trajectory"
	cpptraj -i $CLEANUP_FILE > clean_traj.log
	
	cp $BASE_PROC/$RMSD_FILE .
	sed -i "s,OUT_PATH,$BASE_PROC,g" $RMSD_FILE
	sed -i "s/SYSTEM/${pdb_name}/g" $RMSD_FILE
	echo "Making rmsd of the joint trajectory"
	cpptraj -i $RMSD_FILE > rmsd.log
	cd ..
done
