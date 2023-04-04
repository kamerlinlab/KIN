#!/bin/bash
#SBATCH -J RUN_SYSTEM # Job name
#SBATCH --account=hive-skamerlin3               # Tracking account
#SBATCH -t 12:00:00
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

$AMBERHOME/bin/pmemd.cuda -O -i ../../3md_SYSTEM.in\
            -o 3md.out -p ../SYSTEM_apo.prmtop -c 2heat.rst7 -r 3md.rst7\
            -inf 3md.info -ref 2heat.rst7 -x mdcrd.3md

$AMBERHOME/bin/pmemd.cuda -O -i ../../4md_SYSTEM.in\
            -o 4md.out -p ../SYSTEM_apo.prmtop -c 3md.rst7 -r 4md.rst7\
            -inf 4md.info -ref 3md.rst7 -x mdcrd.4md

$AMBERHOME/bin/pmemd -O -i ../../5min.in\
            -o 5min.out -p ../SYSTEM_apo.prmtop -c 4md.rst7 -r 5min.rst7\
            -inf 5min.info -ref 4md.rst7 -x mdcrd.5min

$AMBERHOME/bin/pmemd.cuda -O -i ../../6md.in\
            -o 6md.out -p ../SYSTEM_apo.prmtop -c 5min.rst7 -r 6md.rst7\
            -inf 6md.info -ref 5min.rst7 -x mdcrd.6md

$AMBERHOME/bin/pmemd.cuda -O -i ../../7md.in\
            -o 7md.out -p ../SYSTEM_apo.prmtop -c 6md.rst7 -r 7md.rst7\
            -inf 7md.info -ref 6md.rst7 -x mdcrd.7md

$AMBERHOME/bin/pmemd.cuda -O -i ../../8md.in\
            -o 8md.out -p ../SYSTEM_apo.prmtop -c 7md.rst7 -r 8md.rst7\
            -inf 8md.info -ref 7md.rst7 -x mdcrd.8md

$AMBERHOME/bin/pmemd.cuda -O -i ../../9md.in\
            -o 9md.out -p ../SYSTEM_apo.prmtop -c 8md.rst7 -r 9md.rst7\
            -inf 9md.info -ref 8md.rst7 -x mdcrd.9md

$AMBERHOME/bin/pmemd.cuda -O -i ../../md.in\
 -p ../SYSTEM_apo.top -c 9md.rst7 -o prod_md1.out -r prod_md1.rst7 -x prod_md1.nc

