#!/bin/bash

# Note that when automating, giving each structure its own folder might be a more convienent setup.
# As opposed to a folder for each step. 

#export BASE=/storage/home/hhive1/dyehorova3/data/tools/Protein_Prep_D
export BASE=~/lk_research/tools/tools-project/protein_prep
cd $BASE

# dirs for each step. 
mkdir 0_xray_structures 1_cleaned_protein 2_reduce 3_propka 4_pdb4amber 5_tleap

#module purge
#source /proj/uucompbiochem/software/amber20/amber20mpi/amber.sh
# Step 1 - 0_xray_structures 1_cleaned_protein
# This was done manually for the time being
# all I did was remove the ion and non-needed lines.
cp $BASE/crystal_structure_selection/pdb_files/*.pdb 0_xray_structures

# Step 2 - 1_cleaned_protein 2_reduce 
# Could add in flag "-QUIET" when automating. 
cd $BASE/0_xray_structures 
for i in *.pdb
do 
        cd $BASE/1_cleaned_protein 
        cp $BASE/0_xray_structures/$i .
        pdb_name=`echo $i| awk -F. '{print $1}'`
        #cp $BASE/crystal_structure_selection/pdb_files/cut_fasta/${pdb_name}.fasta fasta_align.seq 
        cp $BASE/run_scripts/get_sequence.py .
        sed  -i '' "s/NAME/${pdb_name}/g" get_sequence.py 
        echo $pdb_name
        python get_sequence.py
        sed -i '' '1,2d' ${pdb_name}.seq
        sed -i '' '1s/^/>/' ${pdb_name}.seq
        cp $BASE/run_scripts/align_example.py .
        cat ${pdb_name}.seq fasta_align.seq >> fasta_align.seq
      #  python align_example.py
      #  awk  '/^>P1/ { count++; if(count == 2) { sub(/;.*/, "; fasta") } } 1' align1d.ali > alignment.ali
      #  sed -i '' '1,3d' alignment.ali
      #  awk 'FNR==1 && NR==FNR { firstLine=$0 } FNR==1 && NR>FNR { print firstLine } NR>FNR' ${pdb_name}.seq alignment.ali > alignment_new.ali
      #  awk 'BEGIN {print ">P1; known"} 1' alignment_new.ali > alignment_${pdb_name}.ali
      #  cp $BASE/run_scripts/seq_complete.py .
      #  sed -i '' "s/NAME/${pdb_name}/g" seq_complete.py
      #  python seq_complete.py
      #  mv fasta.B99990001.pdb ${pdb_name}_new.pdb    
      #  cd $BASE/2_reduce
	
	#echo ${pdb_name}_FH.pdb	
       # reduce -FLIP -BUILD  $BASE/1_cleaned_protein/${pdb_name}_new.pd > ${pdb_name}_FH.pdb

# Step 3 - 2_reduce 3_propka
        #cd $BASE/3_propka
        #cp $BASE/2_reduce/${pdb_name}_FH.pdb ./.
        #conda activate /home/x_rorcr/.conda/envs/Py3_7_Pyemma # contains an install of propka
        #propka3 ${pdb_name}_FH.pdb > ${pdb_name}_propka.log
    done
    python align_example.py
    exit
        # makes a file named 1g68_FH.pka
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








