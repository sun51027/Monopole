import FWCore.ParameterSet.Config as cms

process = cms.Process("Mpl")

### standard MessageLoggerConfiguration
process.load("FWCore.MessageService.MessageLogger_cfi")

### Standard Configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

## Fitter-smoother: loosen outlier rejection as for first data-taking with LHC "collisions"
process.KFFittingSmootherWithOutliersRejectionAndRK.BreakTrajWith2ConsecutiveMissing = False
process.KFFittingSmootherWithOutliersRejectionAndRK.EstimateCut = 1000

### Conditions
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_TrancheIV_v6', '')

### Track refitter specific stuff
#from RecoTracker.TrackProducer.TrackRefitters_cff import *
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi")

### unclean EE
process.uncleanEERecovered = cms.EDProducer('UncleanSCRecoveryProducer',

            # input collections:
            cleanBcCollection = cms.InputTag('multi5x5SuperClusters','multi5x5EndcapBasicClusters'),
            cleanScCollection = cms.InputTag('multi5x5SuperClusters','multi5x5EndcapSuperClusters'),
                                    
            uncleanBcCollection = cms.InputTag('multi5x5SuperClusters','uncleanOnlyMulti5x5EndcapBasicClusters'),
            uncleanScCollection = cms.InputTag('multi5x5SuperClusters','uncleanOnlyMulti5x5EndcapSuperClusters'),
            # names of collections to be produced:
            bcCollection = cms.string('uncleanEndcapBasicClusters'),
            scCollection = cms.string('uncleanEndcapSuperClusters'),

            )

process.maxEvents = cms.untracked.PSet(
     input = cms.untracked.int32(2000)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#   'file:/eos/user/m/melsawy/MC_productionmONOPOLE2019/Step2+3/CMSSW_8_0_31/src/step3_RECO.root'
 # '/store/mc/RunIISummer16DR80Premix/Monopole_SpinHalf_M-1000_DY_13TeV_TuneCUETP8M1/GEN-SIM-RECO/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/260000/DC803189-415C-E911-864C-FA163EDB8168.root'
#'file:/afs/cern.ch/user/s/srimanob/public/ForMonopole/Matching/RECO.root'
'/store/mc/RunIISummer16DR80Premix/Monopole_SpinHalf_M-1000_DY_13TeV_TuneCUETP8M1/GEN-SIM-RECO/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/260000/08B5424A-C45B-E911-AB7D-A4BF01287D43.root'
#'file:/afs/cern.ch/user/m/melsawy/Work/public/Monopole_reco/RECO.root'
)
,
    duplicateCheckMode = cms.untracked.string('checkEachRealDataFile') 
)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("MonopoleNtuple1000.root")
)


##-------- Electron events of interest --------
process.HLTEle =cms.EDFilter("HLTHighLevel",
     TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
     HLTPaths = cms.vstring("HLT_Photon200_v*"),     
#HLTPaths = cms.vstring("HLT_Photon175_v*", "HLT_MET200_v*","HLT_Photon165_HE10_v*", "HLT_PFMET170_HBHE_BeamHaloCleaned_v*"),
     eventSetupPathsKey = cms.string(''),
     andOr = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
     throw = cms.bool(False) # throw exception on unknown path names
 )

#if 'hltTrigReport' in process.__dict__:
 #   process.hltTrigReport.HLTriggerResults= cms.InputTag( 'TriggerResults', '', 'TEST' )


process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['TriggerReport_24April.txt']
process.MessageLogger.categories.append('HLTrigReport')
process.MessageLogger.categories.append('L1GtTrigReport')
#process.MessageLogger.categories.append('TriggerSummaryProducerAOD')
process.MessageLogger.categories.append('hltTriggerSummaryAOD')
process.load('L1Trigger.GlobalTriggerAnalyzer.l1GtTrigReport_cfi')
process.l1GtTrigReport.L1GtRecordInputTag= cms.InputTag("simGtDigis")

### Construct combined (clean and uncleanOnly Ecal clusters)
process.load("RecoEcal.EgammaClusterProducers.uncleanSCRecovery_cfi")

import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes

process.Monopoler = cms.EDAnalyzer('MonoNtupleDumper'
  ,isData = cms.bool(False)
  ,Output = cms.string("MonopoleNtuple1000_2017_20evt.root")
#  ,bits = cms.InputTag("TriggerResults","","HLT")
  ,TriggerResults = cms.InputTag("TriggerResults","","HLT")
  ,TriggerEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT")
  ,GeneratorTag = cms.InputTag("generatorSmeared","")
  ,PrimaryVertices = cms.InputTag("offlinePrimaryVertices","")                                 
  ,EcalEBRecHits = cms.InputTag("ecalRecHit","EcalRecHitsEB") 
  ,EcalEERecHits = cms.InputTag("ecalRecHit","EcalRecHitsEE") 
  ,HBHERecHits = cms.InputTag("hbhereco","")
  ,JetTag = cms.InputTag("ak4PFJets","")
  ,ElectronTag = cms.InputTag("gedGsfElectrons","")
  ,PhotonTag = cms.InputTag("photons","")
  ,METTag = cms.InputTag("pfMet","")
  ,bcClusterTag = cms.InputTag("hybridSuperClusters","uncleanOnlyHybridBarrelBasicClusters") 
  ,ccClusterTag = cms.InputTag("hybridSuperClusters","hybridBarrelBasicClusters")
  ,combClusterTag = cms.InputTag("uncleanSCRecovered","uncleanHybridBarrelBasicClusters") 
  ,eeCleanTag = cms.InputTag("multi5x5SuperClusters","multi5x5EndcapBasicClusters")
  ,eeUncleanTag = cms.InputTag("multi5x5SuperClusters","uncleanOnlyMulti5x5EndcapBasicClusters") 
  ,eeCombTag = cms.InputTag("uncleanEERecovered","uncleanEndcapBasicClusters")
  ,StripSeedLength = cms.uint32(3)
  ,ClusterLength = cms.uint32(5)
  ,SeedThreshold = cms.double(50.)
  ,TrackTag=cms.InputTag("TrackRefitter")                                 
  ,TrackSource=cms.string("TrackRefitter")
  ,TrackChi2Cut=cms.untracked.double(7.5)
  ,TrackPtCut=cms.untracked.double(3.0)
  ,TrackDeDxCut=cms.untracked.double(0)
  ,TrackDefaultError=cms.untracked.double(0.05)
  ,TrackErrorFudge=cms.untracked.double(0.02)
  ,TrackHitOutput=cms.untracked.bool(True)
)

#process.ecalCombine_step = cms.Path(process.uncleanSCRecovered)
#process.ecalCombineEE_step = cms.Path(process.uncleanEERecovered)
#process.refit_step = cms.Path(process.TrackRefitter)
#process.refit_step = cms.Path(process.MeasurementTrackerEvent * process.TrackRefitter)
#process.mpl_step = cms.Path(process.Monopoler)
#process.HLT_step = cms.Path(process.HLTEle)

process.options = cms.untracked.PSet(     wantSummary = cms.untracked.bool(True) )


#process.p1 = cms.Schedule(process.ecalCombine_step
#                          ,process.ecalCombineEE_step
#                          ,process.refit_step
#                          ,process.mpl_step
#                          ,process.HLT_step
#)
#process.outpath = cms.EndPath(process.TRACKS)

#process.hltTrigReport = cms.EDAnalyzer( 'HLTrigReport',
#    HLTriggerResults = cms.InputTag( 'TriggerResults','','HLT'),
#    reportBy         = cms.untracked.string("job"),
#    resetBy          = cms.untracked.string("never"),
#   serviceBy        = cms.untracked.string("never")
#)

#process.load('L1Trigger.GlobalTriggerAnalyzer.l1GtTrigReport_cfi')
#process.l1GtTrigReport.L1GtRecordInputTag = cms.InputTag ('simDigis')

#process.HLTAnalyzerEndpath = cms.EndPath( process.l1GtTrigReport + process.hltTrigReport )
#process.load('L1Trigger.GlobalTriggerAnalyzer.l1GtTrigReport_cfi')
#process.l1GtTrigReport.L1GtRecordInputTag= cms.InputTag("simGtDigis")
#process.L1AnalyzerEndpath = cms.EndPath( process.l1GtTrigReport + process.hltTrigReport )

process.load("RecoEcal.EgammaClusterProducers.uncleanSCRecovery_cfi")


process.p = cms.Path(process.uncleanSCRecovered* 
			process.uncleanEERecovered*
			process.MeasurementTrackerEvent * process.TrackRefitter*
			process.Monopoler)
