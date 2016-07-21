#!/bin/bash

for itter in {0..39}
  do
  bsub -q 8nh -o lsflog_rvrf_${itter}.txt -e lsferr_rvrf_${itter}.err  submitRVRF.sh $((itter*25)) $((itter*25+24))
done
