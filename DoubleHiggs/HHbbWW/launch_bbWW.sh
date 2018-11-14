cmsDriver.py step1 --filein "file:PythiaHH.root" --fileout file:PythiaHH_step1.root  --pileup_input "dbs:/Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW" --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --nThreads 4 --datamix PreMix --era Run2_2016 --python_filename hh_bbWW_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 169 
DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016,ENDJOB

cmsDriver.py step2 --filein file:PythiaHH_step1.root --fileout file:PythiaHH_step2.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO,EI --nThreads 4 --era Run2_2016 --python_filename hh_bbWW_2_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 169

cmsDriver.py step3 --filein "file:PythiaHH_step2.root" --fileout file:HH_bbWW_bblnjj.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step PAT --nThreads 4 --era Run2_2016 --python_filename hh_bbWW_3_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 5760 || exit $? ; 
 
