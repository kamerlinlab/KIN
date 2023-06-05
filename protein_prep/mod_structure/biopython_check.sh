
export BASE=/storage/home/hhive1/dyehorova3/data/tools/tools-project/protein_prep

cd $BASE
mkdir 0_xray_structures 1_cleaned_protein 2_reduce 3_propka 4_pdb4amber 5_tleap

cd $BASE/crystal_structure_selection/pdb_files 
for i in *.pdb
do 
        pdb_name=`echo $i| awk -F. '{print $1}'`
	cp $BASE/no_modeller/biopython_check.py $BASE/1_cleaned_protein/
	sed -i "s/NAME/${pdb_name}/g"  $BASE/1_cleaned_protein/biopython_check.py
	python  $BASE/1_cleaned_protein/biopython_check.py
	
#        reduce -FLIP -BUILD  $i > ${pdb_name}_FH.pdb


