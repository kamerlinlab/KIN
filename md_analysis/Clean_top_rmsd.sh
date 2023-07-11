#!/bin/bash

#Rory's Paths 
#module purge
#source /proj/uucompbiochem/software/amber20/amber20mpi/amber.sh
#conda activate /home/x_rorcr/.conda/envs/Py3_7_Pyemma
#mkdir /proj/uucompbiochem/users/x_rorcr/TOOLS_Proj/Setup/XXX
#export BASE_PREP=/proj/uucompbiochem/users/x_rorcr/TOOLS_Proj/Setup/Protein_Prep_V2
#export BASE_RUN=/proj/uucompbiochem/users/x_rorcr/TOOLS_Proj/Setup/XXX
#
#SUBMIT_FILE=XXX.sh


# Dariia's Paths
export BASE_PREP=/storage/home/hhive1/dyehorova3/data/tools/tools-project/protein_prep
export BASE_RUN=/storage/home/hhive1/dyehorova3/data/tools/Simulation_runs
export BASE_PROC=/storage/home/hhive1/dyehorova3/data/tools/tools-project/md_analysis

CLEANUP_FILE=equilibration_cleanup.in
RMSD_FILE=protein_rmsd_template.in

# set up all requiered files for the run
cd $BASE_PROC || exit
# Should have a better way to keep all the xray pdbs accessible 
# for the RMSD analysis, for now jsut copying them into 
# the anaysis folder 

cd $BASE_RUN || exit
for i in sys_* 
do 
	cd "$i" || exit
	mkdir clean_all_runs
	pdb_name=$(echo "$i"| awk -Fs_ '{print $2}')
	echo "$pdb_name"
	cp $BASE_PROC/$CLEANUP_FILE .
	rm clean_all_runs/*top
	sed -i "s,RUN_PATH,$BASE_RUN,g" $CLEANUP_FILE
	sed -i "s,OUT_PATH,$BASE_PROC,g" $CLEANUP_FILE
	sed -i "s/SYSTEM/${pdb_name}/g" $CLEANUP_FILE
	echo "Making a joint clean trajectory"
	cpptraj -i $CLEANUP_FILE > clean_traj.log
	
	cp $BASE_PROC/$RMSD_FILE .
	sed -i "s,OUT_PATH,$BASE_PROC,g" $RMSD_FILE
	sed -i "s/SYSTEM/${pdb_name}/g" $RMSD_FILE
	echo "Making rmsd of the joint trajectory"
#	cpptraj -i $RMSD_FILE > rmsd.log
	cd ..
done
cd $BASE_PROC || exit
#python plot_rmsd.py
#Make a plot of all rmsd

