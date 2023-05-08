#!/bin/bash

# Note that when automating, giving each structure its own folder might be a more convienent setup.
# As opposed to a folder for each step. 

export BASE=/storage/home/hhive1/dyehorova3/data/tools/Protein_Prep_D
cd $BASE

# dirs for each step. 
mkdir 0_xray_structures 1_cleaned_protein 2_reduce 3_propka 4_pdb4amber 5_tleap

#module purge
#source /proj/uucompbiochem/software/amber20/amber20mpi/amber.sh
# Step 1 - 0_xray_structures 1_cleaned_protein
# This was done manually for the time being
# all I did was remove the ion and non-needed lines.


# Step 2 - 1_cleaned_protein 2_reduce 
# Could add in flag "-QUIET" when automating. 
cd $BASE/1_cleaned_protein/ 
for i in *.pdb
do 
        pdb_name=`echo $i| awk -F. '{print $1}'`
        cd $BASE/2_reduce
        cp $BASE/1_cleaned_protein/$i ./.
	
	echo ${pdb_name}_FH.pdb	
        reduce -FLIP -BUILD  $i > ${pdb_name}_FH.pdb

# Step 3 - 2_reduce 3_propka
        cd $BASE/3_propka
        cp $BASE/2_reduce/${pdb_name}_FH.pdb ./.
        #conda activate /home/x_rorcr/.conda/envs/Py3_7_Pyemma # contains an install of propka
        propka3 ${pdb_name}_FH.pdb # makes a file named 1g68_FH.pka
# Looked at section: "SUMMARY OF THIS PREDICTION"
# No out of the ordinary residues, so can proceed to next step. 


# Step 4 - 3_propka 4_pdb4amber 
        cd $BASE/4_pdb4amber
        cp $BASE/2_reduce/${pdb_name}_FH.pdb ./. # as no changes made in prior step. 
        pdb4amber -i ${pdb_name}_FH.pdb -o ${pdb_name}_AMB.pdb
# Output from pdb4amber was fine, so can move on with file: 1g68_AMB.pdb

# Step 5 - 4_pdb4amber 5_tleap
        cd $BASE/5_tleap
        cp $BASE/4_pdb4amber/${pdb_name}_AMB.pdb ./.
        mv ${pdb_name}_AMB.pdb ${pdb_name}_apo.pdb # rename output. 
        cp $BASE/tleap.in .
	sed -i "s/NAME/${pdb_name}/g" tleap.in
	tleap -f tleap.in > tleap.out
done
# Inside the tleap.in file, 1 adjustable command. 
# solvateOct gave 53740 atoms
# solvateBox gave 39749 atoms
# Can use solvateBox throughout project then

# Visual inspection of postleap.pdb file looks good. 








