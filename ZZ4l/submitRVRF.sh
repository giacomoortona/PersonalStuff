#!/bin/bash

First=$1
Last=$2

cd ${LS_SUBCWD}

echo "LSF job running in: " `pwd` with options $First $Last

eval `scram runtime -sh`

combine -M MultiDimFit RvRfworkspace.root --algo=grid --points 10000 -m 125.09 -n RVRF_nLL_scan_${First} --firstPoint $First --lastPoint $Last -v 1 --setPhysicsModelParameterRanges RV=0,5:RF0:5
