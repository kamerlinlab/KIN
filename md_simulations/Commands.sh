#!/bin/bash

#Rory's Paths 
#module purge
#source /proj/uucompbiochem/software/amber20/amber20mpi/amber.sh
#conda activate /home/x_rorcr/.conda/envs/Py3_7_Pyemma


# Dariia's Paths
module load anaconda3
conda activate AmberTools22
export BASE_RUN=/storage/home/hhive1/dyehorova3/data/tools/Simulation_runs
export BASE=/storage/home/hhive1/dyehorova3/data/tools/tools-project
export BASE_PREP=/storage/home/hhive1/dyehorova3/data/tools/tools-project/protein_prep

RUN_FILE=run_short.sh
OUTPUT_FILE=prod_md1.out
# choose appropriate production run parameters;
RUN_TIME=50000000 # 100 ns with 2fs timestep, 2h on GT Hive with 1 GPU
TIME_STEP=0.002 # 4fs timestep when running with HMR;

sed -i "s/TIME/${RUN_TIME}/g" $BASE_RUN/md.in
sed -i "s/STEP/${TIME_STEP}/g" $BASE_RUN/md.in
rm $BASE_RUN/file_list.txt

cd $BASE_PREP/1_cleaned_protein || exit
cp $BASE/file_list.txt $BASE_RUN 
#for i in *.pdb ; do echo "$i" >> $BASE_RUN/file_list.txt ; done

# set up all requiered files for the run
cd $BASE_RUN || exit
for i in $(cat $BASE_RUN/file_list.txt)
do 

# make sure equilibration restraints are applied only to the residues 
	pdb_name=$(echo "$i"| awk -F. '{print $1}')
	cp 1min.in $BASE_RUN/1min_"${pdb_name}".in
	cp 2heat.in $BASE_RUN/2heat_"${pdb_name}".in
	cp 3md.in $BASE_RUN/3md_"${pdb_name}".in
	cp 4md.in $BASE_RUN/4md_"${pdb_name}".in
	prelast_line=$(($(wc -l < $BASE_PREP/5_tleap/"${pdb_name}"_apo.pdb)-3))
	total_res=$(awk '(NR=='"$prelast_line"'){print $6}' $BASE_PREP/5_tleap/"${pdb_name}"_apo.pdb)
	echo "$pdb_name"
	echo "$total_res"
    for k in *_"${pdb_name}".in; do sed -i "s/TOTRES/${total_res}/g" "$k"; done

# set up replicas of each system for the runs 	
	mkdir sys_"${pdb_name}" 
	cd sys_"${pdb_name}" || exit
	mkdir run_1 run_2 run_3 run_4 run_5
	cp $BASE_PREP/5_tleap/"${pdb_name}"_apo.prmtop ./.
	cp $BASE_PREP/5_tleap/"${pdb_name}"_apo.inpcrd ./.
# Can add commands in case doing hydrogen mass repartitioning
# Not sure if HMR infulences KIF analysis (like hydrogen bonding etc)
	for j in run_1
	do
		cd "$j" || exit
		cp $BASE_RUN/$RUN_FILE ./.
        	run_number=$(echo $j| awk -F_ '{print $2}')
		sed -i "s/RUN/${run_number}/g" $RUN_FILE
		sed -i "s/SYSTEM/${pdb_name}/g" $RUN_FILE 
		if [ -f "$OUTPUT_FILE" ];  then
			echo "File ${OUTPUT_FILE} for ${pdb_name} exists."
		else
			echo "Running ${pdb_name}"
			sbatch $RUN_FILE
		fi
		cd ..
	done
	cd ..
	
done

	
