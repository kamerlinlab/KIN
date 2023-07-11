# Dariia's Paths
export BASE_PREP=/storage/home/hhive1/dyehorova3/data/tools/Protein_Prep_V2
export BASE_RUN=/storage/home/hhive1/dyehorova3/data/tools/Simulation_runs
export BASE_PROC=/storage/home/hhive1/dyehorova3/data/tools/Md_processing
export BASE=/storage/home/hhive1/dyehorova3/data/tools/tools-project

CONTACTS_FILE=MOD_contact_analyser_template.py
RUN_FILE=run_contacts.sh

cd Contacts
cp $BASE/file_list.txt .
cp $BASE/protein_prep/1_cleaned_protein/all_sequences.seq .
python profile_align.py
#cat $BASE/file_list.txt | while read -r i || [[ -n $i ]];
#do
#	cd $i
#	pdb_name=$(echo "$i"| awk -F. '{print $1}')
#	cp  ../../Stripped.${pdb_name}_apo.prmtop ${pdb_name}_apo.prmtop
#	cp  ../../${pdb_name}_apo_all_runs.nc .
#	echo $pdb_name
#	cp $BASE_PROC/$CONTACTS_FILE .
#	sed -i "s,PROC_PATH,$BASE_PROC,g" $CONTACTS_FILE
#	sed -i "s/SYSTEM/${pdb_name}/g" $CONTACTS_FILE
#	
#	cp $BASE_PROC/$RUN_FILE .
#	sed -i "s/SYSTEM/${pdb_name}/g" $RUN_FILE
#	
#	sbatch $RUN_FILE
#	cd ../../
#done
cd ..		

