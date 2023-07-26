#!/bin/bash

export BASE=/proj/uucompbiochem/users/x_rorcr/TOOLS_Proj/ev_couplings/all_69_structs
export PLMC_DIR=/proj/uucompbiochem/users/x_rorcr/TOOLS_Proj/ev_couplings/Install_parts/plmc-master/bin
cd $BASE

$PLMC_DIR/plmc --couplings couplings.txt bettaLac.ali
