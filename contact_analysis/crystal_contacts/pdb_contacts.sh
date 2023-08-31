BASE=/Users/dariiayehorova/lk_research/tools-project
STRUCTURE_PATH=/Users/dariiayehorova/lk_research/tools-project/md_analysis/Sequences
ANALYSIS_FILE=single_frame_analysis.py

cat $BASE/file_list.txt | while read -r i || [[ -n $i ]];
do
    cp ../$ANALYSIS_FILE .
    structure_name=$(echo "$i"| awk -F. '{print $1}')
    echo $structure_name
    sed -i '' '/^TER/d' $STRUCTURE_PATH/"${structure_name}"_apo_postleap.pdb 
    prelast_line=$(($(wc -l < $STRUCTURE_PATH/"${structure_name}"_apo_postleap.pdb)-3))
    total_res=$(awk '(NR=='"$prelast_line"'){print $5}' $STRUCTURE_PATH/"${structure_name}"_apo_postleap.pdb)
    echo $prelast_line 
    echo $total_res
    sed -i '' "s,FILEPATH,${STRUCTURE_PATH},g" "$ANALYSIS_FILE"
    sed -i '' "s,STRUCTURE,${structure_name},g" "$ANALYSIS_FILE"
    sed -i '' "s,LAST_RES,${total_res},g" "$ANALYSIS_FILE"

    python $ANALYSIS_FILE 
done 
cd ..
