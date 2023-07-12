BASE=/Users/dariiayehorova/lk_research/tools/tools-project
PDB_OUTPUT_PATH=/Users/dariiayehorova/lk_research/tools/tools-project/contact_analysis/multi_structure_test/pdb_outputs
ANALYSIS_FILE=msa_indexing.py

cd msa_outputs || exit
cat $BASE/file_list.txt | while read -r i || [[ -n $i ]];
do
	cp ../$ANALYSIS_FILE .
    structure_name=$(echo "$i"| awk -F. '{print $1}')
    echo $structure_name
	sed -i '' "s,INPUTPATH,${PDB_OUTPUT_PATH},g" "$ANALYSIS_FILE"
    sed -i '' "s,STRUCTURE,${structure_name},g" "$ANALYSIS_FILE"

    python $ANALYSIS_FILE 
done 
cd ..

