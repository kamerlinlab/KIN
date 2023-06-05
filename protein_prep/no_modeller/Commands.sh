#!/bin/bash

#Rory's Paths 
#module purge
#source /proj/uucompbiochem/software/amber20/amber20mpi/amber.sh
#conda activate /home/x_rorcr/.conda/envs/Py3_7_Pyemma
#export BASE=/proj/uucompbiochem/users/x_rorcr/TOOLS_Proj/Setup/Protein_Prep_V2
#


# Dariia's Paths
module load anaconda3
conda activate AmberTools22
export BASE=/storage/home/hhive1/dyehorova3/data/tools/tools-project/protein_prep/no_modeller

cd $BASE

# dirs for each step. 
mkdir 0_xray_structures 1_cleaned_protein 2_reduce 3_propka 4_pdb4amber 5_tleap

# Step 1 - 1_cleaned_protein
# This was done manually for the time being
# all I did was remove the ion and non-needed lines.
#cd ..
#cp crystal_structure_selection/pdb_files/*pdb $BASE/0_xray_structures

cd $BASE ; rm 1_cleaned_protein/* 2_reduce/* 3_propka/* 4_pdb4amber/* 5_tleap/* 

cp $BASE/0_xray_structures/*pdb $BASE/1_cleaned_protein
cd $BASE/1_cleaned_protein

for i in *.pdb
do
	grep -v "SO4" "$i" > temp_file
	mv temp_file "$i"
done
rm all_sequences.txt
rm all_sequences.seq
touch all_sequences.seq
for i in *.pdb
do 
	pdb_name=`echo $i| awk -F. '{print $1}'`
	cp $BASE/get_sequence.py .
	sed -i "s/NAME/${pdb_name}/g" get_sequence.py
	python get_sequence.py
	cat ${pdb_name}.seq >> all_sequences.seq
done
cp $BASE/align_example.py .
python align_example.py
	#find line number where Atom listing starts 
# if running again, remove old files

# make a list of all prepared files to run through. 
rm file_list.txt
cd $BASE/1_cleaned_protein
for i in *.pdb ; do echo $i >> $BASE/file_list.txt ; done


# Step 2 - 2_reduce 
for i in `cat $BASE/file_list.txt`
do 
        pdb_name=`echo $i| awk -F. '{print $1}'`
        cd $BASE/2_reduce
        cp $BASE/1_cleaned_protein/$i ./.
	
		echo ${pdb_name}_FH.pdb	
        reduce -FLIP -BUILD -QUIET $i > ${pdb_name}_FH.pdb
done

# Step 3 - 3_propka
for i in `cat $BASE/file_list.txt`
do 
		pdb_name=`echo $i| awk -F. '{print $1}'`
        cd $BASE/3_propka
        cp $BASE/2_reduce/${pdb_name}_FH.pdb ./.
        propka3 ${pdb_name}_FH.pdb
		
		# check pka predictions. 
		cp $BASE/check_pka_prediction.py .
		sed -i "s/NAME/${pdb_name}_FH/g" check_pka_prediction.py 
		python check_pka_prediction.py
done

# Makes all changes needed after any suggested propka observations have been confirmed manually. 
cd $BASE ; python update_protonation_states.py


# Step 4 - 4_pdb4amber 
for i in `cat $BASE/file_list.txt`
do 
        pdb_name=`echo $i| awk -F. '{print $1}'`
		cd $BASE/4_pdb4amber
        cp $BASE/3_propka/${pdb_name}_FH.pdb ./. 
        pdb4amber -i ${pdb_name}_FH.pdb -o ${pdb_name}_AMB.pdb
done


# Step 5 - 5_tleap
for i in `cat $BASE/file_list.txt`
do 
        pdb_name=`echo $i| awk -F. '{print $1}'`
		cd $BASE/5_tleap
        cp $BASE/4_pdb4amber/${pdb_name}_AMB.pdb ./.
        mv ${pdb_name}_AMB.pdb ${pdb_name}_apo.pdb # rename output. 
        cp $BASE/tleap.in .
		sed -i "s/NAME/${pdb_name}/g" tleap.in
		tleap -f tleap.in > tleap_${pdb_name}.out
		
		# TODO - add a python file to check each tleap_${pdb_name}.out for certain warnings.
		# Main warning to check for is: "There is a bond of [XXXX] angstroms between C and N atoms:"
		# This would indicate missing residue in pdb file. 
done

