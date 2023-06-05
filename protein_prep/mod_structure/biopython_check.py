import os
import re
import pandas as pd
from Bio.PDB import PDBList
from Bio import PDB

def parse_validation_report(pdb_id):
	pdb_file = f"{pdb_id}.pdb"
	parser = PDB.PDBParser()
	structure = parser.get_structure(pdb_id, pdb_file)
	report_file = f"{pdb_id}_validation_report.txt"
	structure.header['idCode'] = pdb_id
	structure.header['name'] = pdb_id
	pdb_io = PDB.PDBIO()
	pdb_io.set_structure(structure)
	pdb_io.save(report_file)

	# Parse the validation report
	validation_data={}
	with open(report_file,'r') as f:
		content = f.read()

		# Overall quality score
		match = re.search(r"Overall model quality:\s+(\d+\.\d+)", content)
		if match:
			validation_data['Overall Quality'] = float(match.group(1))
		
		# Extract residue-level information
		residue_data = re.findall(r"RES\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+\.\d+)", content)
		print(residue_data)
		residue_numbers, residue_names, chain_ids, scores = zip(*residue_data)
		validation_data['Residue Number'] = list(map(int, residue_numbers))
		validation_data['Residue Name'] = residue_names
		validation_data['Chain ID'] = chain_ids
		validation_data['Score'] = list(map(float, scores))
	return validation_data

pdb_id = '1HZO_K1'
validation_data = parse_validation_report(pdb_id)
df = pd.DataFrame(validation_data)
print(f"Overall Quality: {df['Overall Quality'].iloc[0]}")
print("\nTop 10 Residues with Lowest Scores:")

print(df.nsmallest(10, 'Score'))

