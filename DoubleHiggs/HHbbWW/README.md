Instruction to submit bbWW jobs
 =======
   * Tested locally in CMSSW_8_0_21
   * Grid submission scripts not ready yet
1. cmsRun gridPack_to_miniaod_cfg_py_LHE_GEN_SIM.py
    * Check number of events to be created, pythia must match LHE
    * Pythia step is long, no more than few 1000 per jobs
    * pythia8CP5Settings not available yet in 8_0_21 (I think)
2. cmsRun hh_bbWW_1_cfg.py
    * Check number of events to be created
    * Check PU file (now: Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW)
3. cmsRun hh_bbWW_2_cfg.py
4. cmsRun hh_bbWW_3_cfg.py
