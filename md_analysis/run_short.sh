#!/bin/bash
#SBATCH -J RUN_SYSTEM # Job name
#SBATCH --account=hive-skamerlin3               # Tracking account
#SBATCH -t 12:00:00
#SBATCH -N 1
#SBATCH -p hive-gpu-short                                 # Queue name (where job is submitted)
#SBATCH --gres=gpu:1
#SBATCH -o amber_test.out                               # Combined output and error messages file
#SBATCH --mail-type=BEGIN,END,FAIL              # Mail preferences
#SBATCH --mail-user=dyehorova3@gatech.edu 

module load anaconda3
conda activate Kif

bash auto.sh > contacts.log 

