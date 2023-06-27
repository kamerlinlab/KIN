#!/bin/bash
mkdir contacts
cd contacts
cp ../pos_ranking_nostar.dat .

file_path="../structure_names.txt" 
while IFS= read -r line; do
	cp ../contact_analyser_template.py .
        cp ../DY_contact_identification.py .

	structure_name="$line"
	echo "Processing: $structure_name"
	sed  -i "s/SEQ_NAME/${structure_name}/g" contact_analyser_template.py
        pdb_name="${structure_name%%_*}"
        echo $pdb_name	
	sed  -i "s/PDB_NAME/${pdb_name}/g" contact_analyser_template.py

	python contact_analyser_template.py	
done < "$file_path"
