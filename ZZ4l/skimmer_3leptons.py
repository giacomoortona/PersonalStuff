import FWCore.ParameterSet.Config as cms
process = cms.Process("TEST")

### ----------------------------------------------------------------------
### miniAOD skimmer for sync exercise
### ----------------------------------------------------------------------

### ----------------------------------------------------------------------
### Set the GT
### ----------------------------------------------------------------------
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'PHYS14_25_V1::All'#'PLS170_V6AN1::All'
print process.GlobalTag.globaltag

### ----------------------------------------------------------------------
### Standard stuff
### ----------------------------------------------------------------------
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


### ----------------------------------------------------------------------
### Source
### ----------------------------------------------------------------------
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      #'/store/cmst3/user/cmgtools/CMG/GluGluToHToZZTo4L_M-130_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM/V5/PAT_CMG_V5_2_0/patTuple_1.root'
       # 'root://cmsphys05//data/b/botta/V5_4_0/cmgTuple_H126Summer12.root' #Summer12 H126 for FSR synch   
  #'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/0432E62A-7A6C-E411-87BB-002590DB92A8.root'
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/2683B2C5-7C6C-E411-BE0B-002590DB9214.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/0432E62A-7A6C-E411-87BB-002590DB92A8.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/0EAD09A8-7C6C-E411-B903-0025901D493E.root'
  #'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/GluGluToHToZZTo4L_M-125_13TeV-powheg-pythia6/MINIAODSIM/PU20bx25_tsg_PHYS14_25_V1-v1/00000/148E558C-946F-E411-AFA7-7845C4FC3A52.root'
    )
)

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)



### ----------------------------------------------------------------------
### MC Filters and tools
### ----------------------------------------------------------------------

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.drawTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("genParticlesPruned"),
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(True),
                                   printIndex = cms.untracked.bool(False) )


process.printTree = cms.EDAnalyzer("ParticleListDrawer",
                                   maxEventsToPrint = cms.untracked.int32(-1),
                                   printVertex = cms.untracked.bool(False),
                                   src = cms.InputTag("genParticlesPruned")
                                   )


process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                                                   calibratedPatElectrons = cms.PSet(
                                                       initialSeed = cms.untracked.uint32(1),
                                                       engineName = cms.untracked.string('TRandom3')
                                                       ),
                                                   )

# FIXME Add total kinematics filter for MC

process.goodPrimaryVertices = cms.EDFilter("VertexSelector",
  src = cms.InputTag("offlineSlimmedPrimaryVertices"),
  cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2"),
  filter = cms.bool(True),
)



### ----------------------------------------------------------------------
### ----------------------------------------------------------------------
### Loose lepton selection + cleaning + embeddding of user data
### ----------------------------------------------------------------------
### ----------------------------------------------------------------------



#process.muons = cms.EDFilter("PATMuonRefSelector",
#    src = cms.InputTag("slimmedMuons"),
#    cut = cms.string("")
#                             )
#
#process.electrons = cms.EDFilter("PATElectronRefSelector",
#   src = cms.InputTag("slimmedElectrons"),
#   cut = cms.string("")#pt>7 && abs(eta)<2.5 &&" +
#   #                 "gsfTrack.hitPattern().numberOfHits(HitPattern::MISSING_INNER_HITS)<=1"
#   #                 )
#   )

# All leptons, any F/C.
# CAVEAT: merging creates copies of the objects, so that CandViewShallowCloneCombiner is not able to find 
# overlaps between merged collections and the original ones.
#process.softLeptons = cms.EDProducer("CandViewMerger",
#    src = cms.VInputTag(cms.InputTag("muons"), cms.InputTag("electrons"))
#   # src = cms.VInputTag(cms.InputTag("appendPhotons:muons"), cms.InputTag("appendPhotons:electrons"))
#)


### ----------------------------------------------------------------------
### Dileptons (Z->ee, Z->mm)
### ----------------------------------------------------------------------

# l+l- (SFOS, both e and mu)
#process.ZCand = cms.EDProducer("CandViewShallowCloneCombiner",
#process.ZCand = cms.EDProducer("CandViewCombiner",
#    decay = cms.string('softLeptons@+ softLeptons@-'),
#    cut = cms.string('mass > 0 && abs(daughter(0).pdgId())==abs(daughter(1).pdgId())'),
#    checkCharge = cms.bool(True)
#)

#process.ZmuCand =  cms.EDProducer("CandViewShallowCloneCombiner",
#decay = cms.string('muons@+ muons@-'),
#cut = cms.string('mass > 0'),
#checkCharge = cms.bool(True)
#)
#
#process.ZeCand =  cms.EDProducer("CandViewShallowCloneCombiner",
#decay = cms.string('electrons@+ electrons@-'),
#cut = cms.string('mass > 0'),
#checkCharge = cms.bool(True)
#)

process.leptons = cms.EDProducer("CandViewMerger",
 src = cms.VInputTag(cms.InputTag("slimmedMuons"), cms.InputTag("slimmedElectrons"))
)

process.bestleptons = cms.EDFilter("PtMinCandViewSelector",
  src = cms.InputTag("leptons"),
  ptMin = cms.double(4)
)


# The actual filter
process.HzzSkim= cms.EDFilter("CandViewCountFilter",
                                src = cms.InputTag("bestleptons"),
                                minNumber = cms.uint32(3)
                                )

### ----------------------------------------------------------------------
### Paths
### ----------------------------------------------------------------------

process.PVfilter =  cms.Path(process.goodPrimaryVertices)

### ----------------------------------------------------------------------
### Trigger
### ----------------------------------------------------------------------

import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt

TRIGGERLIST = ["HLT_Ele23_Ele12_CaloId_TrackId_Iso_v*","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v*", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v*","HLT_Mu8_TrkIsoVVL_Ele23_Gsf_CaloId_TrackId_Iso_MediumWP_v*","HLT_Mu23_TrkIsoVVL_Ele12_Gsf_CaloId_TrackId_Iso_MediumWP_v*","HLT_Ele17_Ele12_Ele10_CaloId_TrackId_v*"]


process.hltFilter = hlt.hltHighLevel.clone(
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    HLTPaths = TRIGGERLIST,
    andOr = cms.bool(True), # how to deal with multiple triggers: True (OR) accept if ANY is true, False (AND) accept if ALL are true
    throw = cms.bool(False) #if True: throws exception if a trigger path is invalid  
)


# Prepare lepton collections
process.HZZSkimminiAOD = cms.Path(
       process.hltFilter + process.goodPrimaryVertices +
       process.leptons   + process.bestleptons + process.HzzSkim
    )

#process.SkimSequence = cms.Sequence(process.HZZSkimminiAOD)
#process.Skim = cms.Path(process.SkimSequence)

#SkimPaths = cms.vstring('Skim')
#SkimPaths = cms.vstring('PVfilter') #Do not apply skim 
SkimPaths = cms.vstring('HZZSkimminiAOD')

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('testdy.root'),
    outputCommands = cms.untracked.vstring("keep *","drop recoCandidatesOwned_leptons__TEST","drop recoCandidateedmRefToBaseVector_bestleptons__TEST"),#ZZ4lEventContent.outputCommands,
    #SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('HZZSkimminiAOD')
        )
    #)
    )

process.outp = cms.EndPath(process.out)

# process.HF = cms.Path(process.heavyflavorfilter)

# FIXME total kin filter?



