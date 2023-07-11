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
export BASE=/storage/home/hhive1/dyehorova3/data/tools/tools-project
export BASE_PREP=/storage/home/hhive1/dyehorova3/data/tools/tools-project/protein_prep
export BASE_ANALYSIS=/storage/home/hhive1/dyehorova3/data/tools/tools-project/md_analysis
export BASE_PROC=/storage/home/hhive1/dyehorova3/data/tools/Simulation_data

SEQ_FILE=get_sequence.py


mkdir Sequences
cd Sequences || exit
rm  all_sequences.seq
touch all_sequences.seq
cat $BASE/file_list.txt | while read -r i || [[ -n $i ]];
do
	pdb_name=$(echo "$i"| awk -F. '{print $1}')
	cp $BASE_ANALYSIS/$SEQ_FILE .
	sed -i "s/SYSTEM/${pdb_name}_apo_postleap/g" $SEQ_FILE
	cp $BASE_PREP/5_tleap/"${pdb_name}"_apo_postleap.pdb .
	sed -i "s/ASH/ASP/g" "${pdb_name}"_apo_postleap.pdb
	sed -i "s/LYN/LYS/g" "${pdb_name}"_apo_postleap.pdb
	sed -i "s/CYM/CYS/g" "${pdb_name}"_apo_postleap.pdb
	sed -i "s/CYX/CYS/g" "${pdb_name}"_apo_postleap.pdb
	sed -i "s/GLH/GLU/g" "${pdb_name}"_apo_postleap.pdb
	sed -i "s/HID/HIS/g" "${pdb_name}"_apo_postleap.pdb
	sed -i "s/HIE/HIS/g" "${pdb_name}"_apo_postleap.pdb
	sed -i "s/HIP/HIS/g" "${pdb_name}"_apo_postleap.pdb
	sed -i "/WAT/d" "${pdb_name}"_apo_postleap.pdb
	sed -i "/Na/d" "${pdb_name}"_apo_postleap.pdb
	sed -i "/Cl/d" "${pdb_name}"_apo_postleap.pdb
	python $SEQ_FILE
	sed -i "s/>P1;${pdb_name}.*$/>P1;${pdb_name}/g" "${pdb_name}"_apo_postleap.seq
	cat  "${pdb_name}"_apo_postleap.seq >> all_sequences.seq
	sed -i "/structureX/d" all_sequences.seq 
done

