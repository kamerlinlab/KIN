#!/bin/bash

BASE_PROC=/storage/home/hhive1/dyehorova3/data/tools/Simulation_runs
BASE=/storage/home/hhive1/dyehorova3/data/tools/tools-project
CONTACTS_FILE=DYcontact_analyser_new.py
cd Contacts || exit


cat $BASE/file_list.txt | while read -r i || [[ -n $i ]];
do
	structure_name=$(echo "$i"| awk -F. '{print $1}')
	cd ${BASE_PROC}/sys_"${structure_name}"/clean_all_runs || exit 
	if [ -f "clean.${structure_name}_apo.prmtop" ]; then
		cd $BASE/md_analysis/Contacts || exit 
		cp ../$CONTACTS_FILE .
		cp ../DY_contact_identification.py .
		sed -i "s/SEQ_NAME/${structure_name}/g" "$CONTACTS_FILE"
		echo "$structure_name" 
		sed -i "s,SIMPATH,${BASE_PROC},g" "$CONTACTS_FILE"
		python $CONTACTS_FILE
		cd ../
	else
		echo "No topology file for the structure ${structure_name}"
	fi
	cd $BASE/md_analysis/Contacts || exit  
done 
python pickle_to_csv.py
cd ..

