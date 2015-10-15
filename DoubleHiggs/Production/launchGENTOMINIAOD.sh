#!/bin/bash
#source  /afs/cern.ch/cms/cmsset_default.sh

if [ "$#" -ne 2 ]
then
  echo "Usage: ./launchGENtoMINIAOD.sh STEP LAMBDA"
  exit 1
fi


export STEP=$1
export LAMBDA=$2
export SCRAM_ARCH=slc6_amd64_gcc491
export RELEASE="CMSSW_7_4_1_patch1"
export FILENAME="SIMtoMINIAOD74_${STEP}_cfg.py"
export INFOLDER=$(ls /data_CMS/cms/$USER/Lambda${LAMBDA}_74x_step$(($STEP-1)) | tail -n 1)
#ls /data_CMS/cms/$USER/Lambda${LAMBDA}_74x_step$(($STEP-1)) | tail -n 1
if [ $STEP == "0" ]; then
    SCRAM_ARCH=slc6_amd64_gcc481
    RELEASE="CMSSW_7_1_16_patch1"
    FILENAME="GENtoSIM_74x_lambda${LAMBDA}_cfg.py"
fi

export OUTFOLDER="/data_CMS/cms/$USER/Lambda$LAMBDA_74x_step$STEP"

if [ -r $RELEASE/src ] ; then 
 echo release $RELEASE already exists
else
scram p CMSSW $RELEASE
fi
cd $RELEASE/src
eval `scram runtime -sh`
export X509_USER_PROXY=$HOME/private/personal/voms_proxy.cert

cd -
#/data_CMS/cms/salerno/Lambda20_74x_step
if ! [ -f $FILENAME ]; then
    cp /home/llr/cms/ortona/diHiggs/LHEtoMINIAOD/$FILENAME .
    #echo "CACCHIO FILENAME"
fi
if ! [ -f submitOnTier3_LLRHTauTau.py ]; then
    cp /home/llr/cms/ortona/diHiggs/LHEtoMINIAOD/submitOnTier3_LLRHTauTau.py .
    #echo "CACCHIO FILENAME DUE"
fi

echo $STEP $RELEASE $LAMBDA $FILENAME $INFOLDER

#python submitOnTier3_LLRHTauTau.py -o "/data_CMS/cms/salerno/Lambda20_74x_step1/" -s "/data_CMS/cms/salerno/Lambda20_74x_step0/miniAOD__300000Events_0Skipped_1434025821.78/" -t "lambda20_1" -m 300000 -n 300 -c SIMtoMINIAOD74_1_cfg.py

#python submitOnTier3_LLRHTauTau.py -o "/data_CMS/cms/salerno/Lambda20_74x_step2/" -s "/data_CMS/cms/salerno/Lambda20_74x_step1/miniAOD_lambda20_1_300000Events_0Skipped_1434113203.95/" -t "lambda20_2" -m 300000 -n 300 -c SIMtoMINIAOD74_2_cfg.py

python submitOnTier3_LLRHTauTau.py -o $OUTFOLDER -s $INFOLDER -t "lambda${LAMBDA}_${STEP}" -m 300000 -n 300 -c $FILENAME
