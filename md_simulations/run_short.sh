#!/bin/bash
#SBATCH -J RUN_SYSTEM # Job name
#SBATCH --account=hive-skamerlin3               # Tracking account
#SBATCH -t 00:20:00
#SBATCH -N 1
#SBATCH -p hive-gpu                                 # Queue name (where job is submitted)
#SBATCH --gres=gpu:1
#SBATCH -o amber_test.out                               # Combined output and error messages file
#SBATCH --mail-type=BEGIN,END,FAIL              # Mail preferences
#SBATCH --mail-user=dyehorova3@gatech.edu 

module load gcc/10.3.0-o57x6h
module load intel/20.0.4
module load mvapich2/2.3.6-z2duuy
module load cmake/3.23.1-327dbl
module load cuda/11.6.0-u4jzhg
source /storage/hive/project/chem-kamerlin/shared/amber22_install/amber.sh


$AMBERHOME/bin/pmemd -O -i ../../1min_SYSTEM.in\
            -o 1min.out -p ../SYSTEM_apo.prmtop -c ../SYSTEM_apo.inpcrd -r 1min.rst7\
            -inf 1min.info -ref ../SYSTEM_apo.inpcrd -x mdcrd.1min

$AMBERHOME/bin/pmemd.cuda -O -i ../../2heat_SYSTEM.in\
            -o 2heat.out -p ../SYSTEM_apo.prmtop -c 1min.rst7 -r 2heat.rst7\
            -inf 2heat.info -ref 1min.rst7 -x mdcrd.2heat

