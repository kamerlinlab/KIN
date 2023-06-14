#!/bin/bash

# Note that when automating, giving each structure its own folder might be a more convienent setup.
# As opposed to a folder for each step. 

#Dariia's paths
#Hive
export BASE=/storage/home/hhive1/dyehorova3/data/tools/tools-project
export BASE_PREP=/storage/home/hhive1/dyehorova3/data/tools/tools-project/protein_prep
#Local
#export BASE=~/lk_research/tools/tools-project/protein_prep
#Theta

#----------------------------------------------------------
#Step 1: 0_xray_structures - 1_cleaned_protein 
#This workflow relies on the initial structures being already 
#downloaded;
#This step does intial cleaning, filling in missing residues
#NOTE: Modeller tends to form long unphysical tales if the 
#fasta sequence has a long list of residues in the begining or 
#in the end that exceeds the length of the structural template

#Here the tails were removed manually prior form the fasta sequence

cd $BASE_PREP || exit
if [[ ! -d $BASE_PREP/0_xray_structures && ! -d $BASE_PREP/1_cleaned_protein ]]; then
       # dirs for each step.
        echo "NO PREP DIRECTORIES FOUND"
        echo "starting preparing the structures"
        cd $BASE_PREP || exit 
        mkdir 0_xray_structures 1_cleaned_protein 2_reduce 3_propka 4_pdb4amber 5_tleap
        touch $BASE/file_list.txt
        
        # Step 1 - 0_xray_structures 1_cleaned_protein
        cp $BASE_PREP/crystal_structure_selection/pdb_files/*.pdb 0_xray_structures
        cd $BASE_PREP/0_xray_structures || exit 
        for i in *.pdb 
        do 
                pdb_name=$(echo "$i"| awk -F. '{print $1}')
                echo "$pdb_name" >> $BASE/file_list.txt  
        done 
        cat $BASE/file_list.txt | while read -r i || [[ -n $i ]];
        do 
                
                cd $BASE_PREP/1_cleaned_protein || exit 
                cat "$i" >> $BASE/file_list.txt               
                # Do a sequence alignment for the sequance from pdb and fasta
                # To identify any missing residues or any dimers
                pdb_name=$(echo "$i"| awk -F. '{print $1}')
                cp $BASE_PREP/crystal_structure_selection/pdb_files/cut_fasta/"${pdb_name}".fasta fasta.seq 
                cp $BASE_PREP/run_scripts/get_sequence.py .
                sed  -i '' "s/NAME/${pdb_name}/g" get_sequence.py 
                python get_sequence.py
                sed -i '' '1,2d' "${pdb_name}".seq
                sed -i '' '1s/^/>/' "${pdb_name}".seq
                cp $BASE_PREP/run_scripts/align_example.py .
                cat "${pdb_name}".seq fasta.seq >> fasta_align.seq
                python align_example.py
                
                # format an file with sequence alignment such that it is processable 
                # by modeller and run a modeller script "seq_complete.py"
                awk  '/^>P1/ { count++; if(count == 2) { sub(/;.*/, "; fasta") } } 1' align1d.ali > alignment.ali
                python align_example.py
                awk 'FNR==1 && NR==FNR { firstLine=$0 } FNR==1 && NR>FNR { print firstLine } NR>FNR' "${pdb_name}".seq alignment.ali > alignment_new.ali
                sed -i '' '1,3d' alignment.ali
                awk 'BEGIN {print ">P1; known"} 1' alignment_new.ali > alignment_"${pdb_name}".ali
                cp $BASE_PREP/run_scripts/seq_complete.py .
                sed -i '' "s/NAME/${pdb_name}/g" seq_complete.py
                python seq_complete.py
                mv fasta.B99990001.pdb "${pdb_name}"_new.pdb    
        done
        fi      

echo "Initial strucutres are already cleaned"
if test $BASE/file_list.txt; then echo "File with strucutres is here"; fi
#rm $BASE_PREP/3_propka/propka_check.log
#touch $BASE_PREP/3_propka/propka_check.log
rm $BASE_PREP/4_pdb4amber/amber.log
touch $BASE_PREP/4_pdb4amber/amber.log
cp $BASE_PREP/run_scripts/update_protonation_states.py $BASE_PREP/3_propka
cat $BASE/file_list.txt | while read -r i || [[ -n $i ]];
do
#Step 2 - 1_cleaned_protein 2_reduce 
#Could add in flag "-QUIET" when automating. 
        cd $BASE_PREP/2_reduce || exit
        pdb_name=$(echo "$i"| awk -F. '{print $1}')
        echo "$pdb_name"
        reduce -FLIP -BUILD  $BASE_PREP/1_cleaned_protein/"${pdb_name}"_new.pdb > "${pdb_name}"_FH.pdb
# Step 3 - 2_reduce 3_propka
        cd $BASE_PREP/3_propka || exit
        #conda activate /home/x_rorcr/.conda/envs/Py3_7_Pyemma # contains an install of propka
        cp $BASE_PREP/run_scripts/check_pka_prediction.py .
        sed  -i "s/NAME/${pdb_name}_FH/g" check_pka_prediction.py 

        propka3  $BASE_PREP/2_reduce/"${pdb_name}"_FH.pdb
        problematic_res=$(python check_pka_prediction.py)
        echo "$problematic_res"

        if [ "$problematic_res" != None ]; then
                python update_protonation_states.py "$problematic_res"
        fi

#Should manually inspect propka_check.log for non-standard pka predictions

## Step 4 - 3_propka 4_pdb4amber 
        cd $BASE_PREP/4_pdb4amber || exit
        pdb4amber -i $BASE_PREP/2_reduce/"${pdb_name}"_FH.pdb -o "${pdb_name}"_AMB.pdb >> amber.log
## Output from pdb4amber was fine, so can move on with file: 1g68_AMB.pdb
#
## Step 5 - 4_pdb4amber 5_tleap
        cd $BASE_PREP/5_tleap || exit
        cp $BASE_PREP/4_pdb4amber/"${pdb_name}"_AMB.pdb ./.
        mv "${pdb_name}"_AMB.pdb "${pdb_name}"_apo.pdb # rename output. 
        cp $BASE/tleap.in .
	sed -i "s/NAME/${pdb_name}/g" tleap.in
	tleap -f tleap.in > tleap.out
done

# Inside the tleap.in file, 1 adjustable command. 
# solvateOct gave 53740 atoms
# solvateBox gave 39749 atoms
# Can use solvateBox throughout project then

# Visual inspection of postleap.pdb file looks good. 








