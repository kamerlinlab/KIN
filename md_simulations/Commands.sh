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
module load anaconda3
conda activate AmberTools22
export BASE_PREP=/storage/home/hhive1/dyehorova3/data/tools/Protein_Prep_V2
export BASE_RUN=/storage/home/hhive1/dyehorova3/data/tools/Simulation_runs

RUN_FILE=run_md_DY.sh

# choose appropriate production run parameters;
RUN_TIME=50000000 # 100 ns with 2fs timestep, 2h on GT Hive with 1 GPU
TIME_STEP=0.002 # 4fs timestep when running with HMR;

sed -i "s/TIME/${RUN_TIME}/g" $BASE_RUN/md.in
sed -i "s/STEP/${TIME_STEP}/g" $BASE_RUN/md.in
rm $BASE_RUN/file_list.txt

cd $BASE_PREP/1_cleaned_protein
for i in *.pdb ; do echo $i >> $BASE_RUN/file_list.txt ; done

# set up all requiered files for the run
cd $BASE_RUN
for i in `cat $BASE_RUN/file_list.txt`
do 

# make sure equilibration restraints are applied only to the residues 
	pdb_name=`echo $i| awk -F. '{print $1}'`
	cp 1min.in 1min_${pdb_name}.in
	cp 2heat.in 2heat_${pdb_name}.in
	cp 3md.in 3md_${pdb_name}.in
	cp 4md.in 4md_${pdb_name}.in
	last_res_line=$(($(wc -l < $BASE_PREP/5_tleap/${pdb_name}_apo.pdb)-3))
	total_res= awk '(NR=='$prelast_line'){print $6}' $BASE_PREP/5_tleap/${pdb_name}_apo.pdb
	echo $pdb_name
	echo $last_res_line
	echo $total_res
        for k in *_${pdb_name}.in; do sed -i "s/TOTRES/${total_res}/g" $k; done

# set up replicas of each system for the runs 	
	mkdir sys_${pdb_name} 
	cd sys_${pdb_name}
	mkdir run_1 run_2 run_3 run_4 run_5
	cp $BASE_PREP/5_tleap/${pdb_name}_apo.prmtop ./.
	cp $BASE_PREP/5_tleap/${pdb_name}_apo.inpcrd ./.
# Can add commands in case doing hydrogen mass repartitioning
# Not sure if HMR infulences KIF analysis (like hydrogen bonding etc)
	for j in run_*
	do
		cd $j
		cp $BASE_RUN/$RUN_FILE ./.
        	run_number=`echo $j| awk -F_ '{print $2}'`
		sed -i "s/RUN/${run_number}/g" $RUN_FILE
		sed -i "s/SYSTEM/${pdb_name}/g" $RUN_FILE 
		#sbatch $RUN_FILE
		cd ..
	done
	cd ..
	
done

sed -i "s/${RUN_TIME}/TIME/g" $BASE_RUN/md.in
sed -i "s/${TIME_STEP}/STEP/g" $BASE_RUN/md.in
	
