import numpy as np 
import pandas as pd 
from varname import nameof
import statistics
import pickle 
import matplotlib.pyplot as plt

with open("structure_names.txt", "r") as file:
	names=file.readlines()
names=[line.strip() for line in names]
print(names)
all_contacts={}
max_len_sequance=("NAME", 0)
sequence_length =[]
# load sequences and select the longest one

for structure in names:
	key=f"{structure}"
	with open(f"contacts/{structure}_msa_ind_contacts.pickle", "rb") as file:
		contacts=pickle.load(file)
		if len(contacts)> max_len_sequance[1]:
			 max_len_sequance=(structure, len(contacts))
		name_length = (structure,  len(contacts))
		sequence_length.append(name_length)

	all_contacts[key]=contacts
print("longest sequence is:", max_len_sequance)
print("all lengths:", sequence_length) 

#compare interactions present in all other sequences to the longest one
int_strength_counter = {}
int_presence_counter = {}

for structure, value in all_contacts.items():
	for res_1, value_1 in all_contacts[structure].items():
		if res_1 not in int_presence_counter:
			int_presence_counter[res_1]={}
			int_strength_counter[res_1]={}
		for res_2, interaction in all_contacts[structure][res_1].items():
			if  res_2 not in int_presence_counter[res_1]:
				int_presence_counter[res_1][res_2]=0
			int_presence_counter[res_1][res_2]+=1
			if (res_2 not in int_strength_counter[res_1]
					and interaction == 1):
				int_strength_counter[res_1][res_2]=0
			if interaction == 1:
				int_strength_counter[res_1][res_2]+=1
max_interaction={}
for res_1, value_1 in int_strength_counter.items():
	for res_2, interaction in int_strength_counter[res_1].items():
		if interaction==len(sequence_length) and res_1!=res_2:
			if res_1 not in max_interaction:
				max_interaction[res_1]=1
			else:
				max_interaction[res_1]+=1	

sorted_values = sorted(max_interaction.items(), key=lambda item: item[1], reverse=True)

residue_counts = {}
for protein in all_contacts.values():
	for residue1 in protein.keys():
		if residue1 not in residue_counts:
			residue_counts[residue1] = 0
		residue_counts[residue1] += 1

filtered_residues = [residue for residue, count in residue_counts.items() if count >= 2]
interaction_counts = {residue: [] for residue in filtered_residues}


residue_std_devs = {}
for protein in all_contacts.values():
	for residue1, inner_dict in protein.items():
		if residue1 in filtered_residues:
			interaction_count = sum(inner_dict.values())
			interaction_counts[residue1].append(interaction_count)

residue_std_devs = {residue: statistics.stdev(counts) for residue, counts in interaction_counts.items()}
residue_std_devs = dict(sorted(residue_std_devs.items(), key=lambda item: item[0]))
print(residue_std_devs)

# MSA values 
data = (np.genfromtxt('pos_ranking_nostar.dat', names=True, dtype=None, encoding=None))
scores = data['pos_scr']
res = np.arange(1, data.shape[0]+1)

x_values = res
y_values_1 = scores
print(y_values_1)
print(x_values)
y_values_2 = [residue_std_devs.get(residue, np.nan) for residue in res]
y_values_2_norm = []
for i in y_values_2: 
	norm_i=i/max(y_values_2)
	y_values_2_norm.append(norm_i)
print(np.shape(x_values))
print(np.shape(y_values_1))
print(np.shape(y_values_2_norm))
plt.plot(x_values, y_values_1, label='Scores')
plt.plot(x_values, y_values_2_norm, label='Standard Deviations')
plt.xlabel('Residue')
plt.ylabel('MSA Values')
plt.title('MSA Scores and Standard Deviations of Interactions Over Structures')
plt.legend()
plt.grid(True)
plt.savefig('plot.png', dpi=300)

quit()
