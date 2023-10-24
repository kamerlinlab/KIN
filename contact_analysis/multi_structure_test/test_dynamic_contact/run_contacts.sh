#!/bin/bash
#SBATCH -J 1_1BTL_tem1 # Job name
#SBATCH --account=hive-skamerlin3               # Tracking account
#SBATCH -t 12:00:00
#SBATCH -N1 -n1  
#SBATCH -p hive                                 # Queue name (where job is submitted)
#SBATCH -o amber_test.out                               # Combined output and error messages file
#SBATCH --mail-type=BEGIN,END,FAIL              # Mail preferences
#SBATCH --mail-user=dyehorova3@gatech.edu 

module load anaconda3
conda activate tools_proj_py3_11
python multi_frame_contacts.py > output.txt
