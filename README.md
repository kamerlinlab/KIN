# tools-project
Repo for scripts, analysis and whatnot for the tools project 


Currently divided into several sub folders (which could change as we go through the project) depending on the area. 

### Subfolders: 

1. **protein_prep** - From Xray structure to amber topology files

2. **md_simulations** - Everything to do with running the MD simulations. 

3. **md_analysis** - Any MD simulation analysis to run. This can include:
   * General analysis - e.g. RMSDs to check nothing crazy happening in simulations. 
   * Calculate contacts - Use KIF to calculate and save contact scores - best to run on the cluster as can take time. 

4. **network_analysis** - Main part of the project. 
   * Sequence alignments
   * Interaction network generation and analysis. 
