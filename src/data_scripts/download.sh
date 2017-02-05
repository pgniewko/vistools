#! /bin/bash -x

FILES_PATH=/scratch2/scratchdirs/pawelg/FEM_012417/output

scp pawelg@edison.nersc.gov:$FILES_PATH/Vconst_16_fem_bend_PIDX_2_*.xyz .
scp pawelg@edison.nersc.gov:$FILES_PATH/Vconst_16_fem_bend_PIDX_2_*.out .
scp pawelg@edison.nersc.gov:$FILES_PATH/Vconst_16_fem_bend_PIDX_2_*.top .
