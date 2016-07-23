#!/bin/bash

for itter in {0..39}
  do
  bsub -q 8nh -o lsflog_rvrf_${itter}.txt -e lsferr_rvrf_${itter}.err  submitRVRF.sh $((itter*250)) $((itter*250+249))
done
