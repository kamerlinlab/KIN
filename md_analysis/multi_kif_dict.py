import networkx as nx
import numpy as np 
import pandas as pd 
from varname import nameof
import csv
import statistics
import pickle 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

sd_calc=True

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
# Create a dictionary to count the occurrence of each residue
residue_count = {}
# Count the residues in each structure
for structure in all_contacts.values():
	for residue in structure.keys():
		residue_count[residue] = residue_count.get(residue, 0) + 1

# Filter residues that are present in all structures
filtered_residues = [residue for residue, count in residue_count.items() if count == 6]

# Create a NetworkX graph object
graph = nx.Graph()
# Add nodes for each residue
graph.add_nodes_from(filtered_residues)
		
# Add edges for interacting residues
for protein in all_contacts.values():
	for residue1, interactions1 in protein.items():
		if residue1 in filtered_residues:
			for residue2, interaction_value in interactions1.items():
				if residue2 in filtered_residues and interaction_value == 1:
					graph.add_edge(residue1, residue2)
# Perform k-means clustering on the node positions
positions = nx.spring_layout(graph)  # Calculate node positions
node_positions = [positions[residue] for residue in filtered_residues]  # Extract node positions
#
#k = 5  # Number of clusters
#kmeans = KMeans(n_clusters=k)
#labels = kmeans.fit_predict(node_positions)
#
## Draw the network graph with node clustering
#plt.figure(figsize=(8, 6))
#pos = nx.spring_layout(graph, k=0.3)
#nx.draw_networkx_nodes(graph, pos, node_color=labels, cmap=plt.cm.Set1, node_size=200)
#nx.draw_networkx_edges(graph, pos, edge_color='gray', alpha=0.5)
#nx.draw_networkx_labels(graph, pos, font_size=9, font_color='black')

# Customize the plot
#plt.title('Residue Interaction Network Graph with Node Clustering')
#plt.axis('off')
# Draw the network graph


#nx.draw_networkx(graph, with_labels=True, node_color='lightblue', edge_color='gray')

# Customize the plot
#plt.figure(figsize=(8, 6))
#pos = nx.spring_layout(graph, k=0.3)  # Adjust the value of k for more spread-out nodes
#nx.draw_networkx_nodes(graph, pos, node_color='lightblue', node_size=300)
#nx.draw_networkx_edges(graph, pos, edge_color='gray', alpha=0.5)
#nx.draw_networkx_labels(graph, pos, font_size=10, font_color='black')
#plt.title('Residue Interaction Network Graph')
#plt.axis('off')
#plt.savefig('graph_kmean.png', dpi=600)


# Extract unique residues
residues = sorted(list(set(res1 for protein in all_contacts.values() for res1 in protein.keys())))

# Create an empty interaction matrix
interaction_matrix = np.zeros((len(residues)+1, len(residues)+1))

# Populate the interaction matrix
for protein in all_contacts.values():
	for i, res1 in enumerate(residues):
		if res1 in protein.keys(): 
			for j, res2 in enumerate(residues):
				if res2 in protein[res1].keys():
					if res2 in protein[res1]:
						interaction_matrix[i+1, j+1] += protein[res1][res2]
					elif res1 in protein[res2]:
						interaction_matrix[j+1, i+1] += protein[res1][res2]
# Create the heat map
sns.heatmap(interaction_matrix, xticklabels=False, yticklabels=False, cmap='viridis')
# Customize the plot
plt.title('Residue Interaction Heat Map')
plt.xlabel('Residue')
plt.ylabel('Residue')
plt.savefig('heatmap_symm.png', dpi=600)
quit()
max_interaction={}
for res_1, value_1 in int_strength_counter.items():
	for res_2, interaction in int_strength_counter[res_1].items():
		if interaction==len(sequence_length) and res_1!=res_2:
			if res_1 not in max_interaction:
				max_interaction[res_1]=1
			else:
				max_interaction[res_1]+=1	


sorted_values = sorted(max_interaction.items(), key=lambda item: item[1], reverse=True)

# Identify how many of the interactions are formed in each structures 
# based on the global index

residue_counts = {}
for protein in all_contacts.values():
	for residue1 in protein.keys():
		if residue1 not in residue_counts:
			residue_counts[residue1] = 0
		residue_counts[residue1] += 1

if sd_calc is True:
	filtered_residues = [residue for residue, count in residue_counts.items() if count >= 2]
else:
	filtered_residues = residue_counts
interaction_counts = {residue: [] for residue in filtered_residues}

residue_std_devs = {}
for protein in all_contacts.values():
	for residue1, inner_dict in protein.items():
		if residue1 in filtered_residues:
			interaction_count = sum(inner_dict.values())
			interaction_counts[residue1].append(interaction_count)

with open('int_in_all_struct.pickle', 'wb') as file:
	pickle.dump(interaction_counts, file)

field_names = list(interaction_counts.keys())
csv_file = "int_in_all_struct.csv"
with open(csv_file, "w", newline="") as file:
	writer = csv.DictWriter(file, fieldnames=field_names)
	writer.writeheader()
	writer.writerow(interaction_counts)


#Calculate standard deviation and do data visualization
if sd_calc is True:
	residue_std_devs = {residue: statistics.stdev(counts) for residue, counts in interaction_counts.items()}
	residue_std_devs = dict(sorted(residue_std_devs.items(), key=lambda item: item[0]))
else:
	
	
	quit()
# MSA values 
data = (np.genfromtxt('pos_ranking_nostar.dat', names=True, dtype=None, encoding=None))
scores = data['pos_scr']
res = np.arange(1, data.shape[0]+1)
# Plot SD vs MSA scores
x_values = res
y_values_1 = scores
y_values_2 = [residue_std_devs.get(residue, np.nan) for residue in res]
y_values_2_norm = []
for i in y_values_2: 
	norm_i=i/max(y_values_2)
	y_values_2_norm.append(norm_i)
plt.plot(x_values, y_values_1, label='Scores')
plt.plot(x_values, y_values_2_norm, label='Standard Deviations')
plt.xlabel('Residue')
plt.ylabel('MSA Values')
plt.title('MSA Scores and Standard Deviations of Interactions Over Structures')
plt.legend()
plt.grid(True)
plt.savefig('standard_dev.png', dpi=300)

quit()
